from selenium import webdriver
from .chegg_bot import CheggBot
from util.constant import FIREFOX_PROFILE_PATH, TIMEOUT_TIME


class FirefoxCheggBot(CheggBot):
    def __init__(self):
        print("Opening Firefox...")
        profile = webdriver.FirefoxProfile(FIREFOX_PROFILE_PATH)
        self.driver = webdriver.Firefox(profile)
        self.driver.maximize_window()
        self.driver.implicitly_wait(TIMEOUT_TIME)
        # self.driver.minimize_window()
        print("Firefox opened\n")

    def __del__(self):
        self.driver.quit()
        print("Firefox closed")
