import pandas as pd
from db_connection import get_db_connection

# db 커넥션 가져오기
db, cursor = get_db_connection()

# 정제된 데이터 읽어오기
df = pd.read_csv(f'dataset/cleaning/Incheon.csv', sep=',')
df = df[['store_name', 'address', 'detail', 'tel', 'image']]
df = df.where((pd.notnull(df)), None)
df.columns = ['spot_name',  # 장소명: 0
              'address',    # 주소: 1
              'detail',     # 상세내용: 2
              'tel',        # 전화번호: 3
              'spot_image'  # 가게사진: 4
              ]

# 쿼리 날리기
sql = 'INSERT INTO spot(region, spot_name, address, detail, tel, spot_image) VALUES(%s, %s, %s, %s, %s, %s)'
for idx in range(len(df)):
    val = ['인천']
    data = df.values[idx]
    for i in range(5):
        val.append(data[i])

    cursor.execute(sql, tuple(val))

db.commit()
db.close()
