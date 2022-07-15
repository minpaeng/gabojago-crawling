import pandas as pd
from get_dataframe import dataframe
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from get_data import *
import time


# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경


df, keyword, total = dataframe('Busan')

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

    # 진행률
    print(f'{count}/{total} 진행중: {k}')
    count += 1

    # 쿼리 보내기
    search.click()
    search.send_keys(k)
    time.sleep(1)
    search.send_keys(Keys.ENTER)
    time.sleep(1)
    driver.implicitly_wait(0)

    try:
        # searchIframe으로 이동
        driver.switch_to.frame('searchIframe')

        items = driver.find_elements_by_css_selector('.OXiLu')
        print(f'항목 길이: {len(items)}')

        # case 1: 리스트 결과일 때
        if len(items) > 0:
            items[0].click()
            sleep(2)
        # case 2: 리스트 결과가 없거나 상세조회일 때
        else:
            print(f'가게명 {k}에 대한 리스트 결과 없음.')

        switch_frame('entryIframe')
        print(f'가게명 {k}에 상세조회 성공.')
        # ----가게 이름 가져오기----
        na = get_store_name(driver)

        # ----주소 가져오기----
        ad = get_address(driver)

        # ----카테고리 가져오기----
        ca = get_category(driver)

        # -----별점 및 리뷰 수 가져오기-----
        st, vi, bl = get_star_and_review_cnt(driver)

        # ----전화번호 가져오기----
        te = get_tel(driver)

        # ----설명 가져오기----
        de = get_detail(driver)

    # case 3: 결과가 없을 떼
    except:
        print(f'Error: 가게명 {k}에 대한 결과가 존재하지 않음.')

    print(f'- 가게 이름: {na}    - 전화번호: {te}    - 카테고리: {ca}')
    print(f'- 주소: {ad}    - 별점: {st}    - 주문자 리뷰 수: {vi}    - 블로그 리뷰 수: {bl}')
    print(f'설명: {de}')

    store_name.append(na)
    address.append(ad)
    tel.append(te)
    category.append(ca)
    star.append(st)
    visit_review.append(vi)
    blog_review.append(bl)
    detail.append(de)

    print('-' * 80)
    if count == 5000:
        break

    driver.switch_to.default_content()
    search.clear()

driver.close()

df2 = pd.DataFrame({'store_name': store_name, 'address': address, 'tel': tel,
                    'category': category, 'star': star, 'detail': detail,
                    'visit_review': visit_review, 'blog_review': blog_review})
df2.to_csv("new_result.csv")

# df.assign(store_name=store_name, tel=tel, category=category, star=star,
#           detail=detail, visit_review=visit_review, blog_review=blog_review)
# df.to_csv("result.csv")
