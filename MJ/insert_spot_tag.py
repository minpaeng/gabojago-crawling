from MJ.util.get_dataframe import get_spot_tag_dataframe
from MJ.util.db_connection import get_db_connection

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

db, cursor = get_db_connection()

# 지역 이름 설정
df = get_spot_tag_dataframe('Ulsan')

# 스팟 아이디를 조회하기 위한 쿼리문
get_spot_id = 'SELECT spot_id FROM spot WHERE spot_name=%s and address=%s'

# spot_tag에 데이터 삽입을 위한 쿼리문
insert_spot_tag = 'INSERT INTO spot_tag(spot_id, tag_id) VALUES(%s, %s)'

for idx in range(len(df)):
    data = df.values[idx]
    val1 = [data[0], data[1]]
    print(f'spot_name: {val1[0]}, address: {val1[1]}')

    cursor.execute(get_spot_id, tuple(val1))
    result = cursor.fetchall()
    spot_id = result[0][0]
    print(f'spot_id: {spot_id}')

    tag = data[2]
    print(f'tag: {tag}')
    tag_list = tag.split(', ')

    for tmp in tag_list:
        val2 = [spot_id, tag_dict[tmp]]
        print(tuple(val2))
        cursor.execute(insert_spot_tag, val2)
    print('-'*80)

# db.commit()
db.close()
