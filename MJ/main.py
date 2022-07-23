import pandas as pd
from MJ.util.get_dataframe import dataframe
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from MJ.util.get_data import get_required_data
from time import sleep


# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경


def start_crawling(name):
    # searchIframe으로 이동
    driver.switch_to.frame('searchIframe')

    items = driver.find_elements_by_css_selector(name)
    print(f'항목 길이: {len(items)}')

    # case 1: 리스트 결과일 때
    if len(items) > 0:
        items[0].click()
        sleep(1)
    # case 2: 리스트 결과가 없거나 상세조회일 때
    else:
        print(f'가게명 {k}에 대한 리스트 결과 없음.')

    switch_frame('entryIframe')
    print(f'가게명 {k}에 상세조회 성공.')


# 파일명을 변경하여 사용
df, keyword, total = dataframe('Daegu')

driver = webdriver.Chrome()
driver.get('https://map.naver.com/v5/search')
driver.implicitly_wait(10)
driver.maximize_window()

sleep(1)

search = driver.find_element_by_css_selector('input.input_search')

store_name = []
address = []
tel = []
category = []
star = []
visit_review = []
blog_review = []
detail = []
image = []

# 검색창 입력
count = 1
for k in keyword:
    # 반복마다 변수 초기화
    na = "None"
    ad = "None"
    te = "None"
    ca = "None"
    st = "None"
    vi = "None"
    bl = "None"
    de = "None"
    im = "None"

    # 진행률
    print(f'{count}/{total} 진행중: {k}')
    count += 1

    # 쿼리 보내기
    search.click()
    search.send_keys(k)
    sleep(1)
    search.send_keys(Keys.ENTER)
    sleep(1)
    driver.implicitly_wait(0)

    try:
        start_crawling('.OXiLu')
        na, ad, ca, st, vi, bl, te, de, im = get_required_data(driver)

    # case 3: 결과가 없을 떼
    except:
        try:
            start_crawling('._3Apve')
            na, ad, ca, st, vi, bl, te, de, im = get_required_data(driver)

        except:
            print(f'Error: 가게명 {k}에 대한 결과가 존재하지 않음.')

    print(f'- 가게 이름: {na}    - 전화번호: {te}    - 카테고리: {ca}')
    print(f'- 주소: {ad}    - 별점: {st}    - 주문자 리뷰 수: {vi}    - 블로그 리뷰 수: {bl}')
    print(f'설명: {de}')
    print(f'이미지: {im}')
    print('-' * 80)
    store_name.append(na)
    address.append(ad)
    tel.append(te)
    category.append(ca)
    star.append(st)
    visit_review.append(vi)
    blog_review.append(bl)
    detail.append(de)
    image.append(im)

    driver.switch_to.default_content()
    search.clear()

    # 데이터셋 일부만 크롤링(3000개). 필요에 따라 수정하여 사용
    # if count == 3000:
    #     break

driver.close()

df2 = pd.DataFrame({'store_name': store_name, 'address': address, 'tel': tel,
                    'category': category, 'star': star, 'detail': detail,
                    'visit_review': visit_review, 'blog_review': blog_review, 'image': image})
df2.to_csv("Daejeon_new_result.csv")

# 데이터셋 일부만 크롤링 할 시 주석처리하기. 전체를 크롤링 한다면 주석 해제해주세요
# df = df.assign(store_name=store_name, address=address, tel=tel,
#                category=category, star=star, detail=detail,
#                visit_review=visit_review, blog_review=blog_review, image=image)
# df.to_csv("Daejeon_result.csv")
