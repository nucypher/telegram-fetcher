#!/usr/bin/env python3

"""
Fetching admin events from logs
"""
# from telethon.tl import types
from telethon.tl.functions.channels import GetAdminLogRequest
from fetcher_ng import get_tg, check_participant, types, json_serial
import json

LIMIT = 100
output_file = 'users_admin_log.json'


def log_iter(client, channel):
    cursor = 0
    while True:
        log = client(GetAdminLogRequest(
            channel, q='', max_id=cursor, min_id=0, limit=LIMIT))
        if not log.events:
            break
        for ev in log.events:
            cursor = ev.id
            yield ev


if __name__ == '__main__':
    users = []

    client, channel = get_tg()

    for ev in log_iter(client, channel):
        if isinstance(ev.action, types.ChannelAdminLogEventActionDeleteMessage):
            m = ev.action.message
            if isinstance(getattr(m, 'action', None), types.MessageActionChatJoinedByLink):
                user = client.get_entity(m.from_id)
                if check_participant(client, channel, user):
                    users.append((m.date, user.to_dict()))
            elif isinstance(getattr(m, 'action', None), types.MessageActionChatAddUser):
                for u_id in m.action.users:
                    user = client.get_entity(u_id)
                    if check_participant(client, channel, user):
                        users.append((m.date, user.to_dict()))

    print('Last date', ev.date)
    print('Fetched %s users' % len(users))
    with open(output_file, 'w') as f:
        json.dump(users, f, default=json_serial, indent=4)
