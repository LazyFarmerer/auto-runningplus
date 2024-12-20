from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from .state import State
from ..site.site import Site
from .state_type import 러닝플러스StateType


class 학습중_대기하기State(State[Site]):
    def enter(self) -> None:
        self.util.tab(self.obj.driver, 2)
        self.obj.driver.switch_to.frame("iframeAreaBox")

    def execute(self) -> None:
        study_hour = int(self.obj.driver.find_element(By.CSS_SELECTOR, "span#studyPopupHour").text)
        study_min = int(self.obj.driver.find_element(By.CSS_SELECTOR, "span#studyPopupMin").text)
        if (1 <= study_hour and 15 < study_min) or (2 <= study_hour):
            self.obj.state.setState(러닝플러스StateType.중간창)
            self.obj.driver.close()

    def exit(self) -> None:
        pass

