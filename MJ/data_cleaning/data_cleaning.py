import pandas as pd


def to_int(n):
    if n == 'None':
        return 0
    res = n.replace(',', '')
    res = int(res)
    return res


def to_float(n):
    if n == 'None':
        return 0
    res = n.replace(',', '')
    res = float(res)
    return res


df = pd.read_csv('../dataset/Seoul/Seoul_new_result.csv', sep=',', index_col=0)
# df = df.drop([2569], axis=0)

# store_name이 'None'인 행 제거
idx = df[df['store_name'] == 'None'].index
df = df.drop(idx)
# print(df)

# 불용 데이터 제거
idx = df[df['store_name'].str.contains('다이소')].index
df = df.drop(idx)
idx = df[df['store_name'].str.contains('마트')].index
df = df.drop(idx)
idx = df[df['category'].str.contains('마트', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('슈퍼', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('외과', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('내과', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('산부인과', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('예식장', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('피부과', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('이비인후과', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('치과', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('병원', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('수리', na=False)].index
df = df.drop(idx)
idx = df[df['category'].str.contains('한의원', na=False)].index
df = df.drop(idx)
idx = df[df['store_name'].str.contains('빌라')].index
df = df.drop(idx)
idx = df[df['store_name'].str.contains('컴퍼니')].index
df = df.drop(idx)
idx = df[df['store_name'].str.contains('회사')].index
df = df.drop(idx)
# df.to_csv('../dataset/Seoul/Seoul_new_result.csv')

# 숫자에서 콤마 제거
visit_review_int = df.visit_review.apply(to_int)
df.visit_review = visit_review_int

blog_review_int = df.blog_review.apply(to_int)
df.blog_review = blog_review_int

star_float = df.star.apply(to_float)
df.star = star_float

review_sum = df['visit_review'] + df['blog_review']
df = df.assign(review_sum=review_sum)


# 리뷰 많은 순으로 정렬
df = df.sort_values(by=['review_sum', 'star'], ascending=False)
# print(df)

df = df.iloc[:300]
print(df)

df.to_csv('../dataset/cleaning/Seoul.csv')
