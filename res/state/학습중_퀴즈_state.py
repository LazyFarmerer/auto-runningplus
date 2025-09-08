import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from .state import State
from ..site.site import Site
from .state_type import 러닝플러스StateType


class 학습중_퀴즈State(State[Site]):
    """순서: 
    1. 3개의 문제가 순서대로 있고 순서대로 켜지고 나머지는 안보이는 상태
    2. html 에 a[data-anwser='o'] 정보가 있다면 그게 정답임
    3. 클릭 후 다음문제 클릭해야 넘어감
    4. 그와중에 마지막 문제 풀고나면 유형확인 버튼까지 눌러야 함"""
    def enter(self) -> None:
        print("학습중_퀴즈State")
        self.util.tab(self.obj.driver, 2)
        self.obj.driver.switch_to.frame("iframeAreaBox")

    def execute(self) -> None:
        quiz_elements = self.obj.driver.find_elements(By.CSS_SELECTOR, "div.quiz")
        quiz = list(filter(lambda x: "display: block" in x.get_attribute("style"), quiz_elements))[0] # type: ignore
        quiz.find_element(By.CSS_SELECTOR, "a[data-anwser='o']").click()
        time.sleep(2)

        # 마지막 문제는 버튼 클래스이름이 다름
        quiz_btns = quiz.find_elements(By.CSS_SELECTOR, "div.nextQuizBtn a")
        if len(quiz_btns) == 0:
            quiz.find_element(By.CSS_SELECTOR, "div.resultQuizBtn a").click()
            time.sleep(1)
            # 유형확인 클릭
            result_btn = self.obj.driver.find_elements(By.CSS_SELECTOR, "div.prequizresult div.resultchk a.levelchk")
            if result_btn:
                result_btn[0].click()
            time.sleep(1)
            # 이제 찾아서 넘기기
            paging = self.obj.driver.find_element(By.ID, "paging")
            a, b = self.util.match(paging.text)
            if (a != b):
                self.obj.driver.find_element(By.CLASS_NAME, "pageNext").click()

            self.obj.state.setState(러닝플러스StateType.학습중_넘기기)
            return

        quiz_btns[0].click()

    def exit(self) -> None:
        pass

