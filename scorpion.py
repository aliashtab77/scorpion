from telethon.sync import TelegramClient
from config import API_ID, API_HASH, LOCS, GAP, DATABASE_NAME, DATABASE_USER, DATABASE_HOST, DATABASE_PASSWORD
from telethon import functions, types
import mysql.connector

client = TelegramClient("test", api_id=API_ID, api_hash=API_HASH)
client.start()

for makan in LOCS:
    makan_name = makan
    print(f"start extraxt {makan_name}")
    this_makan = LOCS[makan]
    lat,long = this_makan['lat2'], this_makan['long1']
    f_lat , f_long = this_makan['lat1'], this_makan['long2']
    while lat <= f_lat:
        while long <= f_long:
            #TODO
            result = client(functions.contacts.GetLocatedRequest(
                geo_point=types.InputGeoPoint(
                    lat=lat,
                    long=long
                ),
                self_expires=42
            ))
            for user in result.users:
                id = user.id
                access_hash = user.access_hash
                first_name = user.first_name
                last_name = user.last_name
                username = user.username
                phone = user.phone
                try:
                    with mysql.connector.connect() as connection:
                        with connection.cursor() as cursor:
                            sql = f""
                            cursor.execute(sql)
                        connection.commit()

                except:
                    continue
            #TODO
            print((lat , long))
            long += GAP
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