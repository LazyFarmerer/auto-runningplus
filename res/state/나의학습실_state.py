from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from .state import State
from ..site.site import Site
from .state_type import 러닝플러스StateType

class 나의학습실State(State[Site]):
    """나의학습실 진입 후 시작: 
    수강중인 과정 리스트에서 100% 가 아닌 첫번째 선택"""
    def enter(self) -> None:
        els = self.obj.driver.find_elements(By.CSS_SELECTOR, "div.pdt20")
        el = self.util.first_filter(lambda x: "수강중인 과정" in x.find_element(By.CLASS_NAME, "listTitle").text, els)
        # [1:] 로 첫번째 제외하는 이유: 표 가장 위 타이틀임 ㅋㅋㅋㅋ
        self.수강리스트 = el.find_elements(By.CSS_SELECTOR, "tr")[1:]

        if self.수강리스트[0].text == "수강중인 과정이 없습니다.":
            # 다 들었음, 그냥 종료
            self.exit()


    def execute(self) -> None:
        result = list(filter(lambda x: "100%" != x.find_element(By.CLASS_NAME, "right").text.strip(), self.수강리스트))
        if result:
            result[0].find_element(By.CSS_SELECTOR, "td.left a").click()
            self.obj.state.setState(러닝플러스StateType.중간창)
            return
        # 없다면(모든 수강 완료)
        quit()

    def exit(self) -> None:
        # self.obj.driver.close()
        print("종료 함")
        self.obj.is_run = False
