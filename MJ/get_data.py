from time import sleep


# ----가게 이름 가져오기----
def get_store_name(driver):
    na = "None"
    try:
        na = driver.find_element_by_css_selector('span._3XamX').text
    except:
        print('Error: 가게 이름 가져오기 실패.')
    return na


# ----카테고리 가져오기----
def get_category(driver):
    ca = "None"
    try:
        ca = driver.find_element_by_css_selector('span._3ocDE').text
        # sleep(1)
    except:
        print("카테고리 없음.")
    return ca


# ----주소 가져오기----
def get_address(driver):
    ad = "None"
    try:
        ad = driver.find_element_by_css_selector('._2yqUQ').text
    except:
        print('Error: 주소 가져오기 실패.')
    return ad


# ----전화번호 가져오기----
def get_tel(driver):
    te = "None"
    try:
        te = driver.find_element_by_css_selector('span._3ZA0S').text
    except:
        print('전화번호 없음.')
    return te


# ----설명 가져오기----
def get_detail(driver):
    de = "None"

    try:
        button = driver.find_element_by_css_selector('._3__3i')
        button.find_element_by_css_selector('.M_704').click()
        de = button.find_element_by_css_selector('span.WoYOw').text
        # sleep(1)
    except:
        print('설명 없음.')
    return de


# -----별점 및 리뷰 수 가져오기-----
def get_star_and_review_cnt(driver):
    st = "None"
    vi = "None"
    bl = "None"
    cnt_list = []

    try:
        cnt_list = driver.find_elements_by_css_selector('span._1Y6hi')
        sleep(1)
    except:
        print('별점 및 리뷰 수 가져오기 실패')

    try:
        st = cnt_list[0].find_element_by_css_selector('.place_blind').text
        if st.find('별점') > -1:
            st = cnt_list[0].find_element_by_css_selector('._1Y6hi > em').text
            del cnt_list[0]
        else:
            print('별점 없음.')
    except:
        print('파싱 오류')

    try:
        for i in cnt_list:
            tmp = i.find_element_by_css_selector('.place_bluelink').text
            if '주문' in tmp or '방문' in tmp:
                vi = i.find_element_by_css_selector('.place_bluelink > em').text
            elif '블로그' in tmp:
                bl = i.find_element_by_css_selector('.place_bluelink > em').text
    except:
        print('리뷰 수 가져오기 실패')
    return st, vi, bl


def get_required_data(driver):
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
    return na, ad, ca, st, vi, bl, te, de
