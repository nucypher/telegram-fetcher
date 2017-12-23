#!/usr/bin/env python3

from telethon import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import json
import config

LIMIT = 100
output_file = '%s.json' % config.channel

client = TelegramClient('fetcher-session', config.api_id, config.api_hash)
client.connect()

client.sign_in(phone=config.phone)
me = client.sign_in(code=int(input('Enter code: ')))

channel = client(ResolveUsernameRequest(config.channel)).chats[0]

offset = 0
output = []
while True:
    participants = client(GetParticipantsRequest(
        channel, ChannelParticipantsSearch(''), offset, LIMIT, hash=0))
    if not participants.users:
        break
    for user in participants.users:
        user_dict = user.to_dict()
        if user_dict and 'status' in user_dict\
           and user_dict['status'] and 'was_online' in user_dict['status']:
            # Convert datetime objects
            user_dict['status']['was_online'] = str(user_dict['status']['was_online'])
        output.append(user_dict)
    offset += len(participants.users)

print('Fetched %s users' % len(output))
with open(output_file, 'w') as f:
    json.dump(output, f)
