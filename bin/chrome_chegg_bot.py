from .chegg_bot import *


class ChromeCheggBot(CheggBot):
    def __init__(self):
        print("Opening Chrome...")
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option("useAutomationExtension", False)
        option.add_argument("--disable-blink-features=AutomationControlled")
        option.add_argument("--start-maximized")
        option.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
        self.driver = webdriver.Chrome(options=option)
        self.driver.implicitly_wait(TIMEOUT_TIME)
        # self.driver.minimize_window()
        print("Chrome opened\n")

    def __del__(self):
        self.driver.quit()
        print("Chrome closed")
