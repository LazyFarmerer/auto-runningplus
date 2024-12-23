from typing import Tuple
from enum import Enum, auto
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from asdMyModule.chrome import chrome, tab, By, Keys


class State(Enum):
    중간창 = auto()
    학습중_넘기기 = auto()
    학습중_퀴즈 = auto()
    학습중_대기하기 = auto()

def match(text: str) -> Tuple[int, int]:
    b, a = text.split("/ ")
    return int(b), int(a)

driver = chrome("https://www.runningplus.net/Member/Login.nm", False)
# 로그인
driver.find_element(By.ID, "mdID").send_keys("jungangnara091")
driver.find_element(By.ID, "mdPW").send_keys("kkhk2ne1!")
driver.find_element(By.ID, "mdPW").send_keys(Keys.ENTER)
# 로그인 완료

# 학습실 찾아 열기
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "menu")))
els = driver.find_element(By.ID, "menu")
list(filter(lambda x: x.text == "나의 학습실", els.find_elements(By.CLASS_NAME, "gnbMenu ")))[0].click()

# 수강중인 과정 찾아 열기
# els = driver.find_element(By.XPATH)

# 아직 여기까지 안왔음
# 일단 두번째 창 제어부터
run = True
curr_state: State = State.중간창
학습정보_리스트 = driver.find_element(By.CLASS_NAME, "studyRoomTable").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
리스트_수 = len(학습정보_리스트)
학습정보_리스트_index = 4
while 학습정보_리스트_index <= 리스트_수:
    time.sleep(1)

    if curr_state == State.중간창:
        tab(driver, 1)
        학습정보_리스트 = driver.find_element(By.CLASS_NAME, "studyRoomTable").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        학습정보 = 학습정보_리스트[학습정보_리스트_index].find_elements(By.TAG_NAME, "td")[-1].find_element(By.TAG_NAME, "a").click()
        curr_state = State.학습중_넘기기
        continue
    ########################################################
    if curr_state == State.학습중_넘기기:
        tab(driver, 2)
        driver.execute_script("""
            let iframe = document.querySelector("iframe#iframeAreaBox");
            let iframeDoc = iframe.contentWindow.document;
            let v = iframeDoc.querySelector("video");
            v.currentTime = 3600;
        """)
        driver.switch_to.frame("iframeAreaBox")
        quizs = driver.find_elements(By.CLASS_NAME, "quiz")
        if quizs:
            # 퀴즈 상태
            curr_state = State.학습중_퀴즈
            continue

        paging = driver.find_element(By.ID, "paging")
        a, b = match(paging.text)
        if (a != b):
            driver.find_element(By.CLASS_NAME, "pageNext").click()
            continue
        if (a == b):
            curr_state = State.학습중_대기하기
    
    ########################################################
    if curr_state == State.학습중_퀴즈:
        tab(driver, 2)
        driver.switch_to.frame("iframeAreaBox")

        quiz_elements = driver.find_elements(By.CSS_SELECTOR, "div.quiz")
        quiz = list(filter(lambda x: "display: block" in x.get_attribute("style"), quiz_elements))[0] # type: ignore
        quiz.find_element(By.CSS_SELECTOR, "a[data-anwser='o']").click()
        time.sleep(2)
        # 마지막 문제는 버튼 클래스이름이 다름
        # 어쨌든 
        quiz_btns = quiz.find_elements(By.CSS_SELECTOR, "div.nextQuizBtn a")
        if len(quiz_btns) == 0:
            quiz.find_element(By.CSS_SELECTOR, "div.resultQuizBtn a").click()
            time.sleep(1)
            # 유형확인 클릭
            result_btn = driver.find_elements(By.CSS_SELECTOR, "div.prequizresult div.resultchk a.levelchk")
            if result_btn:
                result_btn[0].click()
            time.sleep(1)
            # 이제 찾아서 넘기기
            paging = driver.find_element(By.ID, "paging")
            a, b = match(paging.text)
            if (a != b):
                driver.find_element(By.CLASS_NAME, "pageNext").click()
            curr_state = State.학습중_넘기기
            continue

        quiz_btns[0].click()
    
    ########################################################
    if curr_state == State.학습중_대기하기:
        time.sleep(1) # 그냥 1초 더 기다리기, 결과적으로 2초 마다 확인
        tab(driver, 2)
        study_hour = int(driver.find_element(By.CSS_SELECTOR, "span#studyPopupHour").text)
        study_min = int(driver.find_element(By.CSS_SELECTOR, "span#studyPopupMin").text)
        if (1 <= study_hour and 15 < study_min) or (2 <= study_hour):
            학습정보_리스트_index += 1
            curr_state = State.중간창
            driver.close()



    # 여기는 열린 창 시간 확인
    # timebar_study = driver.find_element(By.ID, "timebarStudy")