import time

from selenium import webdriver

from asdMyModule.chrome import chrome

from ..state.state import StateMachine

class Site:
    def __init__(self, url: str) -> None:
        self.driver: webdriver.Chrome = chrome(url, False)
        self.state: StateMachine

    def run(self):
        while True:
            time.sleep(1)
            self.state.execute()
