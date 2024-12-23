import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from ..state.state import StateMachine


class Site:
    def __init__(self, url: str) -> None:
        self.driver: webdriver.Chrome = _chrome(url)
        self.state: StateMachine
        self.is_run = True

    def run(self):
        while self.is_run:
            time.sleep(1)
            self.state.execute()


def _chrome(url: str) -> webdriver.Chrome:
    options = Options()
    # 브라우저 바로 닫힘 방지
    options.add_experimental_option("detach", True)
    # 불필요한 메시지 제거
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # 최대 크기로 시작
    # options.add_argument("--start-maximized")
    options.add_argument("--force-dark-mode")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return driver