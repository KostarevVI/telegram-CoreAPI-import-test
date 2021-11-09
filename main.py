import telethon
import configparser
import json
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch


config = configparser.ConfigParser()
config.read('config.ini')

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash)

client.start()

group_url = 'https://t.me/joinchat/k-b1fZW60vE0ZmZi'
import_file = 'Chat_WhatsApp_s_Sonya_i_Indigo_PMEF.txt'


async def dump_all_participants(channel):
    offset_user = 0
    limit_user = 100

    all_participants = []
    filter_user = ChannelParticipantsSearch('')

    while True:
        participants = await client(GetParticipantsRequest(channel,
                                                           filter_user, offset_user, limit_user, hash=0))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset_user += len(participants.users)

    all_users_details = []

    for participant in all_participants:
        all_users_details.append({"id": participant.id,
                                  "first_name": participant.first_name,
                                  "last_name": participant.last_name,
                                  "user": participant.username,
                                  "phone": participant.phone,
                                  "is_bot": participant.bot})

    with open('channel_users.json', 'w', encoding='utf8') as outfile:
        json.dump(all_users_details, outfile, ensure_ascii=False)


async def main():
    my_channel = await client.get_entity(group_url)
    await dump_all_participants(my_channel)


with client:
    client.loop.run_until_complete(main())


with client:
    result = client(telethon.functions.messages.CheckHistoryImportRequest(
        import_head=open(import_file).read()
    ))
    print(result.stringify())

    result = client(telethon.functions.messages.CheckHistoryImportPeerRequest(
        peer=group_url
    ))
    print(result.stringify())

    result = client(telethon.functions.messages.InitHistoryImportRequest(
        peer=group_url,
        file=client.upload_file(import_file),
        media_count=0
    ))
    result_id = result.__getattribute__('id')
    print(result.stringify())

    result = client(telethon.functions.messages.StartHistoryImportRequest(
        peer=group_url,
        import_id=result_id
    ))
    print(result)

    # result = client(telethon.functions.messages.InitHistoryImportRequest(
    #     peer=client.get_peer_id(my_channel),
    #     file=client.upload_file('Chat_WhatsApp_s_Sonya_i_Indigo_PMEF.txt'),
    #     media_count=0
    # ))
    # print(result.stringify())
