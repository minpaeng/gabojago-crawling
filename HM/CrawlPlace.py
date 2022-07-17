# 여행 - 상세정보 가져오기 (성공)
# 여행 - 다음 페이지 넘기기 (진행 중)
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


driver = webdriver.Chrome("D:/a_hm/project/hanium_ICT_2022/chromedriver.exe")

# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경


place = ["경북 여행", "광주 여행", "대구 여행",
          "대전 여행", "부산 여행", "서울 여행", "세종 여행", "울산 여행",
          "인천 여행", "전남 여행", "전북 여행", "제주 여행", "충남 여행", "충북 여행"]

for ple in place:
    driver.get("https://map.naver.com/v5/search")

    driver.implicitly_wait(10)
    driver.maximize_window()

    sleep(1)

    # 검색창 입력
    search = driver.find_element_by_css_selector("input.input_search")
    search.click()
    time.sleep(1)
    search.send_keys(ple)
    time.sleep(1)
    search.send_keys(Keys.ENTER)
    time.sleep(2)

    file = open("./" + ple + ".txt", "w", encoding="UTF-8")
    #print(index, name, star, visit_review, blog_review, category, addr, tele, detail)
    file.write("name|star|visit_review|blog_review|category|addr|tele|detail\n")

    # iframe 안으로 들어가기
    driver.switch_to.frame("searchIframe")

    # browser.switch_to_default_content() iframe 밖으로 나오기

    # iframe 안쪽을 한번 클릭하기
    driver.find_element_by_css_selector("#_pcmap_list_scroll_container").click()

    # 로딩된 데이터 개수 확인
    lis = driver.find_elements_by_css_selector("li._22p-O")
    before_len = len(lis)

    next_btn = driver.find_elements_by_css_selector('._2ky45 > a')
    print(next_btn[0].text)

    #for btn in range(10)[1:]:  # next_btn[0] = 이전 페이지 버튼 무시 -> [1]부터 시작
    for btn in range(len(next_btn))[1:]:  # next_btn[0] = 이전 페이지 버튼 무시 -> [1]부터 시작
        print("----------------------------------------------------------------------")

        while True:
            # 맨 아래로 스크롤 내린다.
            driver.find_element_by_css_selector("body").send_keys(Keys.END)

            # 스크롤 사이 페이지 로딩 시간
            time.sleep(1.5)

            # 스크롤 후 로딩된 데이터 개수 확인
            lis = driver.find_elements_by_css_selector("li._22p-O")
            after_len = len(lis)
            print(after_len)

            # 로딩된 데이터 개수가 같다면 반복 멈춤
            if before_len == after_len:
                break
            before_len = after_len

        # 데이터 기다리는 시간을 0으로 만들어 줘요. (데이터가 없더라도 빠르게 넘어감)
        driver.implicitly_wait(0)

        index = 0
        page = driver.find_elements_by_css_selector('._3Apve')

        for li in lis:
            time.sleep(2)

            # 가게명
            name = li.find_element_by_css_selector("span._3Apve").text
            time.sleep(2)

            # 상세 페이지로 이동
            try:
                page[index].click()
                sleep(5)
                switch_frame("entryIframe")
                time_wait(5, '._3ocDE')
                sleep(1)

                # 카테고리 가져오기
                try:
                    category = driver.find_element_by_css_selector('span._3ocDE').text
                    sleep(5)
                except:
                    category = "None"

                # 별점
                try:
                    star = driver.find_element_by_css_selector("span._1Y6hi._1A8_M > em").text
                except:
                    star = "0.00"
                    print("star err!!")

                # 방문자 리뷰수, 블로그 리뷰수 다 있을 때
                if len(driver.find_elements_by_css_selector("span._1Y6hi > a")) == 2:
                    try:
                        reviews = driver.find_elements_by_css_selector("span._1Y6hi > a")
                        visit_review = reviews[0].text
                        blog_review = reviews[1].text
                    except:
                        visit_review = "0"
                        blog_review = "0"
                # 방문자 리뷰수, 블로그 리뷰수 하나만 있을 때
                elif len(driver.find_elements_by_css_selector("span._1Y6hi > a")) == 1:
                    try:
                        reviews = driver.find_elements_by_css_selector("span._1Y6hi > a")
                        review = reviews[0].text
                        if review[0] == "방":
                            visit_review = review
                            blog_review = "0"
                        elif review[0] == "블":
                            visit_review = "0"
                            blog_review = review
                    except:
                        visit_review = "0"
                        blog_review = "0"
                # 모두 없을 때
                elif len(driver.find_elements_by_css_selector("span._1Y6hi > a")) == 0:
                    visit_review = "0"
                    blog_review = "0"

                # 주소 가져오기
                try:
                    ddr_list = driver.find_elements_by_css_selector('._1aj6-')
                    addr0 = ddr_list[0].find_element_by_css_selector('._1h3B_')
                    addr = addr0.find_element_by_css_selector('span._2yqUQ').text
                    sleep(3)
                except:
                    addr = "None"

                # 전화번호 가져오기
                try:
                    tele = driver.find_element_by_css_selector('span._3ZA0S').text
                    sleep(3)
                except:
                    tele = "None"

                # 가게 상세설명 가져오기
                try:
                    driver.find_element_by_css_selector('.M_704').click()
                    sleep(1)
                except:
                    detail = "None"
                try:
                    detail = driver.find_element_by_css_selector('span.WoYOw').text
                    detail = detail.replace("\n", " ")
                    sleep(1)
                except:
                    detail = "None"

                print(index, name, star, visit_review, blog_review, category, addr, tele, detail)

                string = name + "|" + star + "|" + visit_review + "|" + blog_review + "|" \
                         + category + "|" + addr + "|" + tele + "|" + detail
                file.write(string + "\n")

            except:
                print("!!상세페이지 error!!")

            try:
                switch_frame("searchIframe")
            except:
                print("failed to switch searchIframe")

            index = index + 1

        # 다음 페이지 버튼
        if li == lis[-1]:  # 마지막 매장일 경우 다음버튼 클릭
            print('마지막 매장')
            next_btn[-1].click()
            sleep(2)
            # driver.find_element_by_css_selector('.M_704').click()
        else:
            print('페이지 인식 못함')
            break

    file.close()






