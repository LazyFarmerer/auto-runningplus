from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from .state import State
from ..site.site import Site
from .state_type import 러닝플러스StateType


class 중간창State(State[Site]):
    """학습실에서 클릭하면 나오는 창: 
    100% 가 아닌 첫번째 선택\n
    나보니까 시험치는것도 있던데 그것도 고려할 것"""
    def enter(self) -> None:
        self.util.print("중간창State")
        self.util.tab(self.obj.driver, 1)
        선택요소 = self.obj.driver.find_elements(By.XPATH, "/html/body/div[1]/div[5]/div/div[5]/div[1]/div[1]/div[4]/a")
        if 선택요소:
            선택요소[0].click()

    def execute(self) -> None:
        학습정보_리스트 = self.obj.driver.find_element(By.CLASS_NAME, "studyRoomTable").find_element(By.TAG_NAME, "tbody").find_elements(By.TAG_NAME, "tr")
        덜한거_리스트 = list(filter(lambda x: "100%" != x.find_elements(By.TAG_NAME, "td")[2].text.strip(), 학습정보_리스트))
        if 덜한거_리스트:
            덜한거_리스트[0].find_element(By.CSS_SELECTOR, "td a").click()
            self.obj.state.setState(러닝플러스StateType.학습중_넘기기)

    def exit(self) -> None:
        pass
