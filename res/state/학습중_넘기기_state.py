from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from .state import State
from ..site.site import Site
from .state_type import 러닝플러스StateType


class 학습중_넘기기State1(State[Site]):
    """학습창인 상태에서 넘기기 제어: 
    퀴즈가 있다면 퀴즈상태로 넘김
    
    확인 후 (id="paging" 체크)
    - 덜 넘겼다면: 버튼 클릭
    - 다 넘겼다면 대기상태 넘김"""
    def enter(self) -> None:
        self.util.print("학습중_넘기기State1")
        self.util.tab(self.obj.driver, 2)
        self.obj.driver.switch_to.frame("iframeAreaBox")

    def execute(self) -> None:
        quizs = self.obj.driver.find_elements(By.CLASS_NAME, "quiz")
        if quizs:
            # 퀴즈 상태
            self.obj.state.setState(러닝플러스StateType.학습중_퀴즈)
            return
        try:
            paging = self.obj.driver.find_element(By.ID, "paging")
            a, b = self.util.match(paging.text)
            self.util.print(f"{a} / {b}")
            if (a != b):
                self.obj.driver.find_element(By.CLASS_NAME, "pageNext").click()
                return
            if (a == b):
                self.obj.state.setState(러닝플러스StateType.학습중_대기하기)
        except:
            self.obj.state.changeState(러닝플러스StateType.학습중_넘기기, 학습중_넘기기State2(self.obj))
            self.obj.state.setState(러닝플러스StateType.학습중_넘기기)

    def exit(self) -> None:
        pass

class 학습중_넘기기State2(State[Site]):
    def enter(self) -> None:
        self.util.print("학습중_넘기기State2")
        self.util.tab(self.obj.driver, 2)
        self.obj.driver.switch_to.frame("iframeAreaBox")

    def execute(self) -> None:
        try:
            self.obj.driver.execute_script("""
                let v = document.querySelector("video");
                v.currentTime = 3600;
                """)
            presPageNo = int(self.obj.driver.find_element(By.CLASS_NAME, "_presPageNo").text)
            totPageNo = int(self.obj.driver.find_element(By.CLASS_NAME, "_totPageNo").text)
            self.util.print(f"{presPageNo} / {totPageNo}")
            if presPageNo == totPageNo:
                self.obj.state.setState(러닝플러스StateType.학습중_대기하기)
                return
            self.obj.driver.find_element(By.CLASS_NAME, "_nextBtn").click()
        except:
            self.obj.state.changeState(러닝플러스StateType.학습중_넘기기, 학습중_넘기기State3(self.obj))
            self.obj.state.setState(러닝플러스StateType.학습중_넘기기)

    def exit(self) -> None:
        pass
        # self.obj.driver.switch_to.default_content()


# 2025-02-06 추가
class 학습중_넘기기State3(State[Site]):
    def enter(self) -> None:
        self.util.print("학습중_넘기기State3")

    def execute(self) -> None:
        self.util.tab(self.obj.driver, 2)
        self.obj.driver.switch_to.frame("iframeAreaBox")
        try:
            thisPageNum = int(self.obj.driver.find_element(By.CLASS_NAME, "thisPageNum").text)
            totalPageNum = int(self.obj.driver.find_element(By.CLASS_NAME, "totalPageNum").text)
            self.util.print(f"{thisPageNum} / {totalPageNum}")
            if thisPageNum == totalPageNum:
                self.obj.state.setState(러닝플러스StateType.학습중_대기하기)
                return
            self.obj.driver.find_element(By.CLASS_NAME, "nextBtn").click()
        except:
            self.obj.state.changeState(러닝플러스StateType.학습중_넘기기, 학습중_넘기기State4(self.obj))
            self.obj.state.setState(러닝플러스StateType.학습중_넘기기)

    def exit(self) -> None:
        pass

# 2026-09-04 추가
class 학습중_넘기기State4(State[Site]):
    def enter(self) -> None:
        self.util.print("학습중_넘기기State4")

    def execute(self) -> None:
        self.util.tab(self.obj.driver, 2)
        self.obj.driver.switch_to.frame("iframeAreaBox")
        try:
            pageNum = self.obj.driver.find_element(By.CSS_SELECTOR, "button[title='Current Page']")
            a, b = self.util.match(pageNum.text)
            self.util.print(f"{a} / {b}")
            if (a != b):
                self.obj.driver.find_element(By.CSS_SELECTOR, "button[title='Next']").click()
                return
            if (a == b):
                self.obj.state.setState(러닝플러스StateType.학습중_대기하기)
        except:
            self.obj.state.changeState(러닝플러스StateType.학습중_넘기기, 학습중_넘기기State1(self.obj))
            self.obj.state.setState(러닝플러스StateType.학습중_넘기기)

    def exit(self) -> None:
        pass