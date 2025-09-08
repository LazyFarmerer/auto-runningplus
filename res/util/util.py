from typing import List, Tuple, Callable

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

class Util:
    def tab(self, driver: webdriver.Chrome, index: int):
        new_windows = driver.window_handles
        driver.switch_to.window(new_windows[index])

    def match(self, text: str) -> Tuple[int, int]:
        text.replace(" ", "")
        b, a = text.split("/")
        return int(b), int(a)

    def first_filter(self, func: Callable[[WebElement], bool], webElements: List[WebElement]) -> WebElement:
        return list(filter(func, webElements))[0]
    
    def print(self, text: str):
        print(text, " " * 10, end="\r")
