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

local2 = ["경기 맛집", "경남 맛집", "경북 맛집", "광주 맛집", "대구 맛집",
          "대전 맛집", "부산 맛집", "서울 맛집", "세종 맛집", "울산 맛집",
          "인천 맛집", "전남 맛집", "전북 맛집", "제주 맛집", "충남 맛집", "충북 맛집"]

for lo in local2:
    driver.get("https://map.naver.com/v5/search")

    driver.implicitly_wait(10)
    driver.maximize_window()

    sleep(1)

    # 검색창 입력
    search = driver.find_element_by_css_selector("input.input_search")
    search.click()
    time.sleep(1)
    # local = "전북 맛집"
    search.send_keys(lo)
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

    file = open("./" + lo + ".txt", "w", encoding="UTF-8")
    file.write("name|star|visit_review|blog_review|category|addr|tele|detail\n")

    for li in lis:
        time.sleep(2)

        # 가게명
        name = li.find_element_by_css_selector("span.OXiLu").text

        # 별점 있을때
        try:
            time.sleep(2)
            star = li.find_element_by_css_selector("span._2FqTn._1mRAM > em").text

            time.sleep(2)
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
        # 별점 없을 때
        except:
            star = "0.00"
            #print("No star")

            time.sleep(2)
            # 영업 시간이 있다면
            if len(li.find_elements_by_css_selector("span._2FqTn._4DbfT")) > 0:
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
            # 영업 시간이 없다면
            else:
                # 방문자 리뷰수
                try:
                    visit_review = li.find_element_by_css_selector("span._2FqTn:nth-child(1)").text
                except:
                    visit_review = "0"
                # 블로그 리뷰수
                try:
                    blog_review = li.find_element_by_css_selector("span._2FqTn:nth-child(2)").text
                except:
                    blog_review = "0"


        try:
            # 상세 페이지로 이동
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
                print("error category")

            # 가게 상세설명 가져오기
            try:
                driver.find_element_by_css_selector('.M_704').click()
                sleep(1)
            except:
                #print("설명 더보기 클릭 실패")
                detail = "None"
            try:
                detail = driver.find_element_by_css_selector('span.WoYOw').text
                detail = detail.replace("\n", " ")
                sleep(1)
            except:
                #print("설명 가져오기 실패")
                detail = "None"
            #print(f"설명: {de}")


            # 주소 가져오기
            try:
                ddr_list = driver.find_elements_by_css_selector('._1aj6-')
                addr0 = ddr_list[0].find_element_by_css_selector('._1h3B_')
                addr = addr0.find_element_by_css_selector('span._2yqUQ').text
                sleep(3)
            except:
                addr = "None"
                print("error addr")

            # 전화번호 가져오기
            try:
                tele = driver.find_element_by_css_selector('span._3ZA0S').text
                sleep(3)
            except:
                tele = "None"
                print("error tele")

            print(index, name, star, visit_review, blog_review, category, addr, tele, detail)

            string = name + "|" + star + "|" + visit_review + "|" + blog_review + "|" \
                     + category + "|" + addr + "|" + tele + "|" +detail
            file.write(string + "\n")

        except:
            print("!!error!!")
            #index = index - 1
        try:
            switch_frame("searchIframe")
        except:
            print("failed to switch searchIframe")

        index = index + 1

    file.close()
