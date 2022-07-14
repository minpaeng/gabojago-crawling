import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
from time import sleep

df = pd.read_csv('spot/Busan.csv', sep=',')
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


# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경


# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait


driver = webdriver.Chrome()
driver.get("https://map.naver.com/v5/search")

driver.implicitly_wait(10)
driver.maximize_window()


sleep(1)
search = driver.find_element_by_css_selector("input.input_search")

category = []
star = []
visit_review = []
blog_review = []

# 검색창 입력
for k in keyword:
    print("검색중인 가게: " + k)
    search.click()
    search.send_keys(k)
    time.sleep(1)
    search.send_keys(Keys.ENTER)
    time.sleep(1)
    driver.implicitly_wait(0)
    ca = "None"
    st = "None"
    vi = "None"
    bl = "None"
    try:
        # iframe 안으로 들어가기
        driver.switch_to.frame("searchIframe")

        # iframe 안쪽을 한번 클릭하기
        driver.find_element_by_css_selector("#_pcmap_list_scroll_container").click()

        # 로딩된 데이터 개수 확인
        # lis = driver.find_elements_by_id("li._1EKsQ _12tNp")
        # before_len = len(lis)

        page = driver.find_elements_by_css_selector('.OXiLu')
        page[0].click()
        sleep(1)
        switch_frame("entryIframe")

        # ----카테고리 가져오기----
        try:
            ca = driver.find_element_by_css_selector('span._3ocDE').text
            sleep(1)
            print("카테고리: " + ca)
        except:
            print("카테고리 가져오기 실패")

        # -----별점 및 리뷰 수 가져오기-----
        idx = 0
        try:
            cnt_list = driver.find_elements_by_css_selector('span._1Y6hi')
            # print(len(cnt_list))
            st = cnt_list[0].find_element_by_tag_name('em').text
            idx += 1
            vi = cnt_list[1].find_element_by_tag_name('em').text
            idx += 1
            bl = cnt_list[2].find_element_by_tag_name('em').text
            idx += 1
        except:
            print(f"idx:{idx} 리뷰 수 가져오기 실패")
            print(f'별점: {ca}\n방문자 리뷰 수: {vi}\n블로그 리뷰 수: {bl}')

    except:
        print("가게명 " + k + " 에 대한 리스트 결과 없음.")
        try:
            print("가게명" + k + "에 대한 리다이렉트 성공")
            switch_frame("entryIframe")
            # ----카테고리 가져오기----
            try:
                ca = driver.find_element_by_css_selector('span._3ocDE').text
                sleep(1)
            except:
                pass
            print("카테고리: " + ca)

            # ----평점 가져오기----
            try:
                store_rating_list = driver.find_element_by_css_selector('._1A8_M').text
                st = re.sub('별점', '', store_rating_list).replace('\n', '')  # 별점이라는 단어 제거
            except:
                pass
            print("별점: " + st)

            # -----별점 및 리뷰 수 가져오기-----
            try:
                cnt_list = driver.find_elements_by_css_selector('span._1Y6hi')
                # print(len(cnt_list))
                ca = cnt_list[0].find_element_by_tag_name('em').text
                vi = cnt_list[1].find_element_by_tag_name('em').text
                bl = cnt_list[2].find_element_by_tag_name('em').text
            except:
                print("리뷰 수 가져오기 실패")
            print(f'별점: {ca}\n방문자 리뷰 수: {vi}\n블로그 리뷰 수: {bl}')

        except:
            print("Error: 가게명 " + k + " 에 대한 결과가 존재하지 않음.")

    driver.switch_to.default_content()
    search.clear()

driver.close()
