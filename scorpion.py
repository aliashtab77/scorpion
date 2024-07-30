from telethon.sync import TelegramClient
from config import API_ID, API_HASH, LOCS, GAP, DATABASE_NAME, DATABASE_USER, DATABASE_HOST, DATABASE_PASSWORD, DATABASE_NAME_SPIDER
from telethon import functions, types
from telethon.errors.rpcerrorlist import FloodWaitError
import mysql.connector


accounts = []
with mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST, password=DATABASE_PASSWORD,
                             database=DATABASE_NAME_SPIDER) as connection:
    with connection.cursor() as cursor:
        sql = f"SELECT number FROM accs"
        cursor.execute(sql)
        for i in cursor:
            accounts.append(i[0])
    connection.commit()

client = TelegramClient(accounts[0], api_id=API_ID, api_hash=API_HASH)
client.start()

mm = 0

for makan in LOCS:
    makan = LOCS[mm]
    makan_name = makan
    print(f"start extraxt {makan_name}")
    this_makan = LOCS[makan]
    lat,long = this_makan['lat2'], this_makan['long1']
    f_lat , f_long = this_makan['lat1'], this_makan['long2']
    while lat <= f_lat:
        while long <= f_long:
            #TODO
            print(lat, long)
            try:
                result = client(functions.contacts.GetLocatedRequest(
                    geo_point=types.InputGeoPoint(
                        lat=lat,
                        long=long
                    ),
                    self_expires=42
                ))
            except FloodWaitError:
                mm += 1
                if mm == len(accounts):
                    mm = 0
                    client.disconnect()
                    client = TelegramClient(accounts[mm], api_id=API_ID, api_hash=API_HASH)
                    client.start()
                    continue

            for user in result.users:
                id = user.id
                access_hash = user.access_hash
                first_name = user.first_name
                last_name = user.last_name
                username = user.username
                phone = user.phone
                try:
                    with mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST, password=DATABASE_PASSWORD, database=DATABASE_NAME) as connection:
                        with connection.cursor() as cursor:
                            sql = f"INSERT INTO {makan_name} (id, access_hash, first_name, last_name, username, phone) values ('{id}', '{access_hash}', '{first_name}', '{last_name}', '{username}', '{phone}')"
                            cursor.execute(sql)
                        connection.commit()
                except:
                    continue
            for chat in result.chats:
                id = chat.id
                title = chat.title
                access_hash = chat.access_hash
                username = chat.username
                participants_count = chat.participants_count
                try:
                    with mysql.connector.connect(user=DATABASE_USER, host=DATABASE_HOST, password=DATABASE_PASSWORD, database=DATABASE_NAME) as connection:
                        with connection.cursor() as cursor:
                            sql = f"INSERT INTO {makan_name}_G (id, title, access_hash, username, participants_count) values ('{id}', '{title}', '{access_hash}', '{username}', '{participants_count}')"
                            cursor.execute(sql)
                        connection.commit()
                except:
                    continue

            #TODO
            long += GAP
        long = this_makan['long1']
        lat += GAP








# result = client(functions.contacts.GetLocatedRequest(
            #     geo_point=types.InputGeoPoint(
            #         lat=lat,
            #         long=long
            #     ),
            #     self_expires=42
            # ))
            # res = result.stringify()
            # print(res)