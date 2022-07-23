import pandas as pd
from db_connection import get_db_connection

"""
# 1. txt 파일 -> csv 파일
df = pd.read_csv('./Busan/부산 여행.txt', sep='|', header=0,
                 names=['name', 'star', 'visit_review', 'blog_review', 'category', 'addr', 'tele', 'detail', 'tag', 'image'])

# 열 이름 바꾸기
df.columns = ['spot_name', 'star', 'visit_review', 'blog_review', 'category', 'address', 'tel', 'detail', 'tag', 'spot_image']

# region 열 추가
regions = []
for row in df['spot_name']:
    regions.append('부산')
df['region'] = regions  # region열에 순차대로 원소를 대입

# spot 테이블 형식으로 변환
df2 = df[['spot_name', 'address', 'region', 'detail', 'tel', 'spot_image', 'tag', 'star', 'visit_review', 'blog_review', 'category']]
address = './csv_dataset/' #기본 경로 설정해줌(코딩이 길어지므로)
df2.to_csv(path_or_buf=address+'busan_place.csv', sep=',')

"""
# 2. csv 파일 -> mysql
db, cursor = get_db_connection()

# csv 파일 mysql 에 넘기기
# spot 에 넘긴 지역들 : 대전, 대구 ,부산, 광주, 인천, 제주, 서울, 울산 ----------------------------------------------------
#df2 = pd.read_csv('./csv_dataset/ulsan_place.csv', sep=',', header=0)
#df2 = df2[['spot_name', 'address', 'region', 'detail', 'tel', 'spot_image']]
#df2 = df2.where((pd.notnull(df2)), None)

# 쿼리 날리기
#sql = 'INSERT INTO spot(spot_name, address, region, detail, tel, spot_image) VALUES(%s, %s, %s, %s, %s, %s)'
#for idx in range(len(df2)):
#    data = df2.values[idx]
#    cursor.execute(sql, tuple(data))

# spot 에 넘긴 지역들 :

# 제주
df2 = pd.read_csv('./csv_dataset/jeju_place.csv', sep=',', header=0)
# sql select까지 문제 없는 도시: 부산, 대구, 대전, 광주, 인천, 울산, 서울
df2 = df2[['spot_name', 'address', 'tag']]
df2 = df2.where((pd.notnull(df2)), None)

# 쿼리 날리기
tag_dict = {
    '야경': 1,
    '이색체험': 2,
    '피크닉': 3,
    '데이트': 4,
    '커피 맛집': 5,
    '디저트 맛집': 6,
    '분위기 있는': 7,
    '든든한': 8,
    '신나는': 9,
    '파릇파릇한': 10,
    '기분 전환': 11
}

# 스팟 아이디를 조회하기 위한 쿼리문
get_spot_id = 'SELECT spot_id FROM spot WHERE spot_name=%s and address=%s'
# spot_tag에 데이터 삽입을 위한 쿼리문
insert_spot_tag = 'INSERT INTO spot_tag(spot_id, tag_id) VALUES(%s, %s)'

#sql = 'INSERT INTO spot(spot_name, address, region, detail, tel, spot_image) VALUES(%s, %s, %s, %s, %s, %s)'
#sql2 = 'INSERT INTO spot(spot_id, tag_id) VALUES(%s, %s)'
sql_select = 'SELECT spot_id FROM spot WHERE spot_name=%s AND address= %s'
#sql_update='UPDATE spot SET address="서울 강서구 방화대로 94",detail="계절별로 색다른 경치를 만끽하고 가슴깊이 심호흡을 하며 거닐고 싶은 아름다운 숲속에 자연과 사람이 하나가 될 수 있는 메이필드호텔입니다. 자연과의 조화를 생각해 절제된 품격으로 지어진 메이필드호텔은 유럽의 감성이 고스란히 살아 있습니다. 아울러 김포공항까지 5분, 인천공항까지는 30분거리에 위치하고 있어 도심과 공항을 연결하는 최적의 요지로 평가받고 있습니다.", tel="02-2660-9000",spot_image="https://search.pstatic.net/common/?autoRotate=true&type=w560_sharpen&src=https%3A%2F%2Fldb-phinf.pstatic.net%2F20160223_298%2F14561944136366k68I_JPEG%2F_01_06_.jpg" WHERE spot_id = 4302'


for idx in range(len(df2)):
    data = df2.values[idx]
    val1 = [data[0], data[1]]
    cursor.execute(get_spot_id, tuple(val1))
    result = cursor.fetchall()
    spot_id = result[0][0]
    print(spot_id)
    print(f'spot_id: {result[0][0]}, spot_name: {val1[0]}, address: {val1[1]}')

    #print(data[2]) # 야경,분위기 있는,데이트
    #print(data[2][0])  # 야

    tag = data[2]
    print(f'tag: {tag}')
    tag_list = tag.split(',')
    for tmp in tag_list:
        val2 = [spot_id, tag_dict[tmp]]
        print(tuple(val2))
        #cursor.execute(insert_spot_tag, val2)


"""
    for tag_one in data[2].split(','):
        #print(tag_one)
        if tag_one == '야경':
            tag_id_num = 1
        elif tag_one == '이색체험':
            tag_id_num = 2
        elif tag_one == '피크닉':
            tag_id_num = 3
        elif tag_one == '데이트':
            tag_id_num = 4
        elif tag_one == '커피 맛집':
            tag_id_num = 5
        elif tag_one == '디저트 맛집':
            tag_id_num = 6
        elif tag_one == '분위기 있는':
            tag_id_num = 7
        elif tag_one == '든든한':
            tag_id_num = 8
        elif tag_one == '신나는':
            tag_id_num = 9
        elif tag_one == '파릇파릇한':
            tag_id_num = 10
        elif tag_one == '기분 전환':
            tag_id_num = 11
        #cursor.execute('INSERT INTO spot(spot_id, tag_id) VALUES(%d, '+tag_id_num+')', tuple(result))
"""

# update 코드
#sql_update='UPDATE spot SET address="제주 서귀포시 대정읍 에듀시티로 178",detail="주소 : 제주특별자치도 서귀포시 대정읍 에듀시티로 178 대중교통(버스) 이용 시 : 시외버스 755번(공항-영어교육도시-모슬포) 이용 자가(렌터카) 이용 시 : 영어교육도시 내 삼정APT 옆 위치", tel="064-792-6047",spot_image="https://search.pstatic.net/common/?autoRotate=true&quality=95&type=w750&src=https%3A%2F%2Fapis.naver.com%2Fplace%2Fpanorama%2Fthumbnail%2F19648880%2F0%3Fwidth%3D800%26height%3D400%26msgpad%3D1658329588575%26md%3Dkb5CYkWK9GkTslSDSc8XawnXazQ%253D" WHERE spot_id = 4001'
#cursor.execute(sql_update)
#cursor.execute('SELECT * FROM spot WHERE spot_id=4001')
#result = cursor.fetchall()
#spot_id = result[0][0]
#print(spot_id)
#print(result)

#db.commit()
db.close()
