import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


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

# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경



# 검색창 입력

search = driver.find_element_by_css_selector("input.input_search")
search.click()
time.sleep(1)
search.send_keys("강남역 맛집")
time.sleep(1)
search.send_keys(Keys.ENTER)
time.sleep(2)

# iframe 안으로 들어가기
driver.switch_to.frame("searchIframe")

# browser.switch_to_default_content() iframe 밖으로 나오기

# iframe 안쪽을 한번 클릭하기
driver.find_element_by_css_selector("#_pcmap_list_scroll_container").click()

# 로딩된 데이터 개수 확인
lis = driver.find_elements_by_css_selector("li._1EKsQ")
before_len = len(lis)
print(before_len)

while True:
    # 맨 아래로 스크롤 내린다.
    driver.find_element_by_css_selector("body").send_keys(Keys.END)

    # 스크롤 사이 페이지 로딩 시간
    time.sleep(1.5)

    # 스크롤 후 로딩된 데이터 개수 확인
    lis = driver.find_elements_by_css_selector("li._1EKsQ")
    after_len = len(lis)

    # 로딩된 데이터 개수가 같다면 반복 멈춤
    if before_len == after_len:
        break
    before_len = after_len

# 데이터 기다리는 시간을 0으로 만들어 줘요. (데이터가 없더라도 빠르게 넘어감)
driver.implicitly_wait(0)

index = 0
page = driver.find_elements_by_css_selector('.OXiLu')

for li in lis:
    category = "없음"
    # 별점이 있는 것만
    if len(li.find_elements_by_css_selector("span._2FqTn._1mRAM > em")) > 0:
        # 가게명
        name = li.find_element_by_css_selector("span.OXiLu").text
        # 별점
        star = li.find_element_by_css_selector("span._2FqTn._1mRAM > em").text

        # 영업 시간이 있다면
        if len(li.find_elements_by_css_selector("span._2FqTn._4DbfT")) > 0:
            # 방문자 리뷰수
            try:
                visit_review = li.find_element_by_css_selector("span._2FqTn:nth-child(3)").text
            except:
                visit_review = "0"
            # 블로그 리뷰수
            try:
                blog_review = li.find_element_by_css_selector("span._2FqTn:nth-child(4)").text
            except:
                blog_review = "0"
        # 영업 시간이 없다면
        else:
            # 방문자 리뷰수
            try:
                visit_review = li.find_element_by_css_selector("span._2FqTn:nth-child(2)").text
            except:
                visit_review = "0"
            # 블로그 리뷰수
            try:
                blog_review = li.find_element_by_css_selector("span._2FqTn:nth-child(3)").text
            except:
                blog_review = "0"

        try:
            # 상세 페이지로 이동
            page[index].click()
            sleep(1)
            switch_frame("entryIframe")

            # -----카테고리 가져오기-----
            try:
                category = driver.find_element_by_css_selector('span._3ocDE').text

                sleep(2)
            except:
                print("error")
        except:
            print("!!error!!")
        print(index, name, star, visit_review, blog_review, category)
        index = index + 1
        try:
            switch_frame("searchIframe")
        except:
            print("failed to sitch searchIframe")