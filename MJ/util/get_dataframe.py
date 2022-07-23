import pandas as pd


def dataframe(file_name):
    df = pd.read_csv(f'spot/{file_name}.csv', sep=',')
    df = df.loc[df['상권업종대분류명'] == '음식']
    df = df[['상호명', '상권업종중분류명', '상권업종소분류명', '표준산업분류명', '시도명', '법정동명']]

    df.columns = ['name',  # 상호명
                  'cate_1',  # 중분류명
                  'cate_2',  # 소분류명
                  'cate_3',  # 표준산업분류명
                  'city',  # 시도명
                  'dong',  # 법정동명
                  ]

    # print(df.iloc[1])

    dong_list = list(df['dong'])
    name_list = list(df['name'])

    keyword = []
    for i in range(len(name_list)):
        keyword.append(str(dong_list[i]) + ' ' + str(name_list[i]))

    # print(dong_list[:10])

    df = df.assign(keyword=keyword)
    # print(df.iloc[0])
    total = df.shape[0] - 1

    return df, keyword, total


def get_spot_dataframe(file_name):
    df = pd.read_csv(f'dataset/cleaning/{file_name}.csv', sep=',')
    df = df[['store_name', 'address', 'detail', 'tel', 'image']]
    df = df.where((pd.notnull(df)), None)
    df.columns = ['spot_name',  # 장소명: 0
                  'address',  # 주소: 1
                  'detail',  # 상세내용: 2
                  'tel',  # 전화번호: 3
                  'spot_image'  # 가게사진: 4
                  ]
    return df


def get_spot_tag_dataframe(file_name):
    df = pd.read_csv(f'dataset/cleaning/{file_name}.csv', sep=',')
    df = df[['store_name', 'address', 'tag']]
    df.columns = ['spot_name',  # 장소명: 0
                  'address',    # 주소: 1
                  'tag'         # 태그: 2
                  ]
    return df
