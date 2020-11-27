from .chegg_bot import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import StaleElementReferenceException


class ChromeCheggBot(CheggBot):
    def __init__(self):
        super().__init__()
        print("Opening Chrome...")
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option("useAutomationExtension", False)
        option.add_argument("--disable-blink-features=AutomationControlled")
        option.add_argument("--start-maximized")
        option.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")
        option.add_argument("--log-level=3")
        d = DesiredCapabilities.CHROME
        d["goog:loggingPrefs"] = {"browser": "ALL"}  # To get console logs
        self.driver = webdriver.Chrome(options=option, desired_capabilities=d)
        self.driver.implicitly_wait(TIMEOUT_TIME)
        # self.driver.minimize_window()
        print("Chrome opened\n")

    def skip_question(self):
        generate_random_delay()  # Delay
        try:
            # TODO: Check if it is taking forever to skip, then that means bot has been detected

            self.driver.find_element_by_id("ext-skip-btn").click()
            while self.driver.find_element_by_id("countdown").text != "9 min 55 sec":
                pass
        except StaleElementReferenceException as err:
            generate_random_delay()  # Delay
        except Exception as err:
            print(err)
            return
        print("Question skipped\n")

    def click_on_answer(self):
        try:
            self.driver.find_element_by_id("ext-answer-btn").click()
        except Exception as err:
            print(err)
        print("You may start answering now")

    def submit_answer(self):
        try:
            self.driver.find_element_by_id("ext-submit-btn").click()
            while self.driver.find_element_by_id("countdown").text != "9 min 55 sec":
                pass
        except StaleElementReferenceException as err:
            generate_random_delay()  # Delay
        except Exception as err:
            print(err)
            return
        print("Answer submitted\n")

    def __del__(self):
        self.driver.quit()
        print("Chrome closed")
