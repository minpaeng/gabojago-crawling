from get_dataframe import get_spot_dataframe
from db_connection import get_db_connection

# db 커넥션 가져오기
db, cursor = get_db_connection()

df = get_spot_dataframe('Incheon')

# 쿼리 날리기
sql = 'INSERT INTO spot(region, spot_name, address, detail, tel, spot_image) VALUES(%s, %s, %s, %s, %s, %s)'
for idx in range(len(df)):
    # 지역 반드시!!! 설정 후 코드 실행하기
    val = ['인천']
    data = df.values[idx]
    for i in range(5):
        val.append(data[i])

    cursor.execute(sql, tuple(val))

db.commit()
db.close()
