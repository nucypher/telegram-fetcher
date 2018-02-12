#!/usr/bin/env python3

from telethon import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors.rpc_error_list import UserNotParticipantError
from telethon.tl import types
import socket
import json
import config
import os
from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


LIMIT = 500
early_file = 'nucypher_telegram_early.json'
output_file = 'nucypher_telegram.json'
patch_files = ['users_admin_log.json']
users = []
cursor = None


def check_participant(client, channel, u):
    try:
        participant = client(GetParticipantRequest(channel, u)).participant
        return not isinstance(participant, types.ChannelParticipantBanned)
    except UserNotParticipantError:
        return False


def get_tg():
        client = TelegramClient('fetcher-session', config.api_id, config.api_hash)
        client.connect()

        if not client.is_user_authorized():
            client.sign_in(phone=config.phone)
            client.sign_in(code=int(input('Enter code: ')))

        channel = client(ResolveUsernameRequest(config.channel)).chats[0]

        return client, channel


if __name__ == '__main__':
    if os.path.exists(early_file):
        print('Checking early users...')
        early_date = datetime.fromtimestamp(os.path.getmtime(early_file))
        client, channel = get_tg()
        with open(early_file) as f:
            ctr = 0
            for user in json.load(f):
                u_id = user['id']
                user = client.get_entity(u_id)
                if check_participant(client, channel, user):
                    users.append((early_date, user.to_dict()))
                    ctr += 1
            print('Added {} early users'.format(ctr))

    for fname in patch_files:
        with open(fname) as f:
            users += json.load(f)
    if patch_files:
        print('Added more from patch')

    while True:
        try:
            client, channel = get_tg()

            total, messages, senders = client.get_message_history(
                    channel, limit=1, offset_id=0)
            if cursor is None:
                cursor = messages[0].id + 1

            while True:
                total, messages, senders = client.get_message_history(
                        channel, limit=LIMIT, offset_id=cursor)
                if not messages:
                    break

                for m, s in zip(messages, senders):
                    if isinstance(m, types.MessageService):
                        if isinstance(m.action, types.MessageActionChatJoinedByLink):
                            if check_participant(client, channel, s):
                                users.append((m.date, s.to_dict()))
                        elif isinstance(m.action, types.MessageActionChatAddUser):
                            for u_id in m.action.users:
                                if u_id == s.id:
                                    user = s
                                else:
                                    user = client.get_entity(u_id)
                                if check_participant(client, channel, user):
                                    users.append((m.date, user.to_dict()))

                cursor = messages[-1].id
                print(cursor)
                if cursor <= 1:
                    break

            break
        except (ConnectionAbortedError, socket.timeout, ValueError, BufferError):
            print('Connection was aborted')

    # forward in time
    # + filter repetitions
    users_dates = {}
    users_id = {}
    in_users = users[::-1]
    users = []
    for d, u in in_users:
        users_id[u['id']] = u
        users_dates[u['id']] = min(u.get(u['id'], d), d)

    for uid, d in users_dates.items():
        users.append((d, users_id[uid]))

    print('Fetched %s users' % len(users))
    with open(output_file, 'w') as f:
        json.dump(users, f, default=json_serial, indent=4)
