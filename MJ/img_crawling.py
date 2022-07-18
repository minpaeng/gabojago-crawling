import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from get_data import get_img
from time import sleep


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


df = pd.read_csv('dataset/Seoul/Seoul_cleaned.csv', index_col=0)

keyword = []
store_list = list(df['store_name'])
for i in range(len(store_list)):
    keyword.append('서울' + str(store_list[i]))

driver = webdriver.Chrome()
driver.get('https://map.naver.com/v5/search')
driver.implicitly_wait(10)
driver.maximize_window()

sleep(1)

search = driver.find_element_by_css_selector('input.input_search')

count = 1
image = []
for k in keyword:
    # 진행률
    print(f'{count}/300 진행중: {k}')
    count += 1

    # 쿼리 보내기
    search.click()
    search.send_keys(k)
    search.send_keys(Keys.ENTER)
    sleep(1)
    driver.implicitly_wait(0)

    try:
        start_crawling('.OXiLu')
        im = get_img(driver)

    # case 3: 결과가 없을 떼
    except:
        try:
            start_crawling('._3Apve')
            im = get_img(driver)

        except:
            print(f'Error: 가게명 {k}에 대한 결과가 존재하지 않음.')

    print(f'이미지: {im}')
    print('-' * 80)
    image.append(im)

    driver.switch_to.default_content()
    search.clear()

driver.close()

df = df.assign(image=image)
df.to_csv('dataset/cleaning/Seoul.csv')
