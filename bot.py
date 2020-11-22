from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import random
from time import sleep
import re


# Constants
FIREFOX_PROFILE_PATH = "C:/Users/shubh/AppData/Roaming/Mozilla/Firefox/Profiles/8gftv1ml.default-1592257819872"
CHROME_PROFILE_PATH = "C:/Users/shubh/AppData/Local/Google/Chrome/User Data"
CHEGG_HOMEPAGE_URL = "https://www.chegg.com"
CHEGG_RESULTS_PAGE_BASE_URL = "https://www.chegg.com/search"
TIMEOUT_TIME = 10
THRESHOLD_PERCENTAGE = 50


class CheggBot:
    def __init__(self):
        pass

    def loginToChegg(self, id, password):
        self.driver.get("https://www.chegg.com")
        signInBtn = self.driver.find_element_by_xpath('//*[@id="eggshell-15"]/a')
        generateRandomDelay()
        signInBtn.click()

        emailField = self.driver.find_element_by_xpath('//*[@id="emailForSignIn"]')
        passwordField = self.driver.find_element_by_xpath(
            '//*[@id="passwordForSignIn"]'
        )

        generateRandomDelay()
        emailField.send_keys(id)
        passwordField.send_keys(password)
        passwordField.send_keys(Keys.RETURN)

    def searchQuestion(self, text):
        try:
            if self.switchToTab(CHEGG_RESULTS_PAGE_BASE_URL):
                self.searchQuestionOnResultsPage(text)
            else:
                self.searchQuestionOnHomepage(text)
        except Exception as err:
            print(err)
            return False
        return True

    def searchQuestionOnHomepage(self, text):
        try:
            self.driver.get(CHEGG_HOMEPAGE_URL)
            searchBox = self.driver.find_element_by_xpath('//*[@id="chegg-searchbox"]')
            searchBox.click()
            searchBox.clear()
            generateRandomDelay()
            searchBox.send_keys(text)
            searchBox.send_keys(Keys.RETURN)
        except Exception as err:
            print(err)
            return False
        return True

    def searchQuestionOnResultsPage(self, text):
        try:
            searchBox = self.driver.find_element_by_xpath('//*[@id="chegg-searchbox"]')
            searchBox.click()
            generateRandomDelay()
            searchBox.send_keys(text)
            searchBox.send_keys(Keys.RETURN)
        except Exception as err:
            print(err)
            return False
        return True

    def processResults(self):
        try:
            generateRandomDelay()
            self.selectStudyTab()

            numResults = self.getSearchResultCount()
            if numResults == -1:
                print("No results found for this question!")
                return False

            for i in range(1, numResults + 1):
                question = self.driver.find_element_by_css_selector(
                    f".automation-section-1-serp-result-{i} > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2)"
                )
                html = question.get_attribute("innerHTML")
                totalEmTags = html.count("<em>")
                totalWords = len(html.split())
                percentage = round(totalEmTags * 100 / totalWords)
                print(f"\tAnswer {i}: {percentage}% matching")
                if percentage >= THRESHOLD_PERCENTAGE:
                    print("Relevant result(s) found!")
                    return True  # Function executed successfully

            print("No relevant results found!")
            return True  # Function executed successfully
        except Exception as err:
            print(err)
            return False

    """
        Utility Functions
    """

    def selectStudyTab(self):
        # Check if "Study" tab is selected or not, if not then select it
        try:
            studyTab = self.driver.find_element_by_xpath(
                '//*[@id="search-results-tabs_tabheader_2"]'
            )
            isSelected = studyTab.get_attribute("aria-selected")
        except Exception as err:
            print(err)
            return False

        if isSelected != "true":
            studyTab.click()
        return True

    def switchToTab(self, url):
        try:
            numTabs = len(self.driver.window_handles)
            for tab in self.driver.window_handles:
                self.driver.switch_to.window(tab)
                currentUrl = self.driver.current_url
                if re.search(f"{url}.*", currentUrl) != None:
                    return True  # Switch success
        except Exception as err:
            print(err)
        return False  # Switch failed

    def isBotDetected(self):
        try:
            titleText = self.driver.find_element_by_xpath(
                "/html/body/section/div[2]/div/h1"
            ).text
        except:
            return False  # Bot not detected

        if titleText == "Please verify you are a human":
            return True  # Bot detected
        return False  # Bot not detected

    def getSearchResultCount(self):
        try:
            numResults = len(self.driver.find_elements_by_css_selector(".detjfS > div"))
        except:
            return -1
        return numResults


class ChromeCheggBot(CheggBot):
    def __init__(self):
        option = webdriver.ChromeOptions()
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option("useAutomationExtension", False)
        option.add_argument("--disable-blink-features=AutomationControlled")
        option.add_argument("--start-maximized")
        option.add_argument(f"user-data-dir={CHROME_PROFILE_PATH}")

        print("Opening Chrome...")
        self.driver = webdriver.Chrome(options=option)
        print("Chrome opened")
        self.driver.implicitly_wait(TIMEOUT_TIME)


class FirefoxCheggBot(CheggBot):
    def __init__(self):
        profile = webdriver.FirefoxProfile(FIREFOX_PROFILE_PATH)
        print("Opening Firefox...")
        self.driver = webdriver.Firefox(profile)
        print("Firefox opened")
        self.driver.implicitly_wait(TIMEOUT_TIME)


def generateRandomDelay():
    delay = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"Waiting for {delay} seconds...")
    sleep(delay)


def resolveCaptcha():
    print("Bot has been compromised! Complete the captcha!")
    captchaComplete = input("Is captcha filled? (y/n) ")
    while captchaComplete.lower() != "y":
        print("Please complete the captcha and try again.")
        captchaComplete = input("Is captcha filled? (y/n) ")


def autopilot(chrome, firefox):
    print("Autopilot ON!")
    print("Sit back and relax, let the bot do its job.")
    # TODO: Implement autopilot


def searchAutomatically(chrome, firefox):
    # TODO: Get question from the Chrome browser
    pass


def searchManually(driver):
    text = input("Enter question text: ")
    if not driver.searchQuestion(text):
        # Check if bot has been detected
        if driver.isBotDetected():
            resolveCaptcha()
        else:
            print("Something went wrong.")

    if not driver.processResults():
        # Check if bot has been detected
        if driver.isBotDetected():
            resolveCaptcha()
        else:
            print("Something went wrong.")


def main():
    # Create two instances
    firefox = FirefoxCheggBot()
    # chrome = ChromeCheggBot()
    chrome = None

    option = 0
    while option != 4:
        print("***WELCOME TO CHEGG BOT***")
        print("1. Start Autopilot")
        print("2. Search a question (fully automated)")
        print("3. Search a question (manual input)")
        print("4. Exit")
        option = int(input("Choose an option: "))
        print()
        if option == 1:
            autopilot(chrome, firefox)
        elif option == 2:
            searchAutomatically(chrome, firefox)
        elif option == 3:
            searchManually(firefox)
        elif option == 4:
            print("Goodbye!")
        else:
            print("Invalid option. Try again.")
        print()
    firefox.switchToTab("second")


if __name__ == "__main__":
    main()
