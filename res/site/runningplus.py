import os
from dotenv import load_dotenv

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .site import Site
from ..state.state import StateMachine
from ..state.나의학습실_state import 나의학습실State
from ..state.중간창_state import 중간창State
from ..state.학습중_넘기기_state import 학습중_넘기기State1
from ..state.학습중_퀴즈_state import 학습중_퀴즈State
from ..state.학습중_대기하기_state import 학습중_대기하기State
from ..state.state_type import 러닝플러스StateType

class 러닝플러스(Site):

    def __init__(self) -> None:
        super().__init__("https://www.runningplus.net/Member/Login.nm")

        load_dotenv()
        ID = os.getenv("RUNNINGPLUS_ID")
        PW = os.getenv("RUNNINGPLUS_PW")
        # 둘중 하나라도 없으면 종료
        if (ID is None) or (PW is None): quit()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "mdID"))
        )
        self.driver.find_element(By.ID, "mdID").send_keys(ID)
        self.driver.find_element(By.ID, "mdPW").send_keys(PW)
        self.driver.find_element(By.ID, "mdPW").send_keys(Keys.ENTER)

        self.driver.get("https://www.runningplus.net/Mystudy/MyStudyList.nm")


        self.state = StateMachine[러닝플러스StateType]({
            러닝플러스StateType.나의학습실: 나의학습실State(self),
            러닝플러스StateType.중간창: 중간창State(self),
            러닝플러스StateType.학습중_넘기기: 학습중_넘기기State1(self),
            러닝플러스StateType.학습중_퀴즈: 학습중_퀴즈State(self),
            러닝플러스StateType.학습중_대기하기: 학습중_대기하기State(self),
        })


