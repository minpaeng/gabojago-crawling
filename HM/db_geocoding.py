import json
import urllib
from urllib.request import Request, urlopen
from HM.dataset.db_connection import get_db_connection


def get_location(loc, idx):
    client_id = '아이디'
    client_secret = '비번'
    url = f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query=" \
          + urllib.parse.quote(loc)

    # 주소 변환
    request = urllib.request.Request(url)
    request.add_header('X-NCP-APIGW-API-KEY-ID', client_id)
    request.add_header('X-NCP-APIGW-API-KEY', client_secret)
    response = urlopen(request)
    res = response.getcode()                                # 응답이 정상적으로 완료되면 200을 리턴

    if res == 200:
        response_body = response.read().decode('utf-8')
        response_body = json.loads(response_body)
        # print(response_body)

        # 주소가 존재할 경우 total count == 1
        if response_body['meta']['totalCount'] == 1:
            lat = response_body['addresses'][0]['y']        # 위도
            lon = response_body['addresses'][0]['x']        # 경도
            # print(lon, lat)
            val = [lat, lon, idx]
            cursor.execute(insert_spot_xy, tuple(val))
        else:
            print('location not exist')
            cursor.execute(insert_spot_xy_null, tuple([idx]))

    else:
        print('ERROR')
        cursor.execute(insert_spot_xy_null, tuple([idx]))


get_count_spot = 'SELECT count(spot_id) FROM spot'

# 주소 조회 쿼리문
get_spot_id = 'SELECT spot_id, address FROM spot WHERE spot_id=%s'
# 위도/경도 좌표 삽입 쿼리문
insert_spot_xy = 'UPDATE spot SET spot_x=%s, spot_y=%s where spot_id=%s'
insert_spot_xy_null = 'UPDATE spot SET spot_x=null, spot_y=null where spot_id=%s'

db, cursor = get_db_connection()

cursor.execute(get_count_spot)
db_count = cursor.fetchall()
print(db_count[0][0])                                       # 4801

for idx in range(1, db_count[0][0]+1):
    val1 = (idx,)
    cursor.execute(get_spot_id, val1)
    result = cursor.fetchall()
    spot_id = result[0][0]
    spot_address = result[0][1]
    print(f'spot_address: {spot_address}, spot_id: {spot_id}')

    #  함수 적용
    get_location(spot_address, idx)

db.commit()
db.close()


