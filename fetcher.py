#!/usr/bin/env python3

from telethon import TelegramClient
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import json
import config
from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


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
        output.append(user.to_dict())
    offset += len(participants.users)

print('Fetched %s users' % len(output))
with open(output_file, 'w') as f:
    json.dump(output, f, default=json_serial)
