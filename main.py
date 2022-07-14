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

category = []
star = []
visit_review = []
blog_review = []

# 검색창 입력
count = 1
for k in keyword:
    print(f'{count}/{total} 진행중: {k}')
    count += 1
    search.click()
    search.send_keys(k)
    time.sleep(1)
    search.send_keys(Keys.ENTER)
    time.sleep(1)
    driver.implicitly_wait(0)

    # case 1: 리스트 결과일 때
    try:
        # iframe 안으로 들어가기
        driver.switch_to.frame('searchIframe')

        # iframe 안쪽을 한번 클릭하기
        driver.find_element_by_css_selector('#_pcmap_list_scroll_container').click()

        page = driver.find_elements_by_css_selector('.OXiLu')
        page[0].click()
        sleep(1)
        switch_frame('entryIframe')

        # ----카테고리 가져오기----
        ca = get_category(driver)

        # -----별점 및 리뷰 수 가져오기-----
        st, vi, bl = get_star_and_review_cnt(driver)

        # ----설명 가져오기----
        de = get_detail(driver)

    # case 2: 리스트 결과가 없을 떼
    except:
        print(f'가게명 {k}에 대한 리스트 결과 없음.')
        try:
            print(f'가게명 {k}에 대한 리다이렉트 성공.')
            switch_frame('entryIframe')

            # ----카테고리 가져오기----
            ca = get_category(driver)

            # -----별점 및 리뷰 수 가져오기-----
            st, vi, bl = get_star_and_review_cnt(driver)

            # ----설명 가져오기----
            de = get_detail(driver)

        # case 3: 결과가 없을 때
        except:
            print(f'Error: 가게명 {k}에 대한 결과가 존재하지 않음.')

    print(f'카테고리: {ca}')
    print(f'별점: {st}\n주문자 리뷰 수: {vi}\n블로그 리뷰 수: {bl}')
    print(f'설명: {de}')

    category.append(ca)
    star.append(st)
    visit_review.append(vi)
    blog_review.append(bl)
    print('-'*80)

    driver.switch_to.default_content()
    search.clear()

driver.close()

df.assign(category=category, star=star, visit_review=visit_review, blog_review=blog_review)
df.to_csv("result.csv")
