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
        keyword.append(dong_list[i] + ' ' + name_list[i])

    # print(dong_list[:10])

    df = df.assign(keyword=keyword)
    # print(df.iloc[0])
    total = df.shape[0] - 1

    return df, keyword, total
