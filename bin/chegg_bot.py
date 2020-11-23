from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from util.utility import generate_random_delay
from util.constant import *


class CheggBot:
    def login_to_chegg(self, id, password):
        self.driver.get("https://www.chegg.com")
        sign_in_btn = self.driver.find_element_by_xpath('//*[@id="eggshell-15"]/a')
        generate_random_delay()
        sign_in_btn.click()

        email_field = self.driver.find_element_by_xpath('//*[@id="emailForSignIn"]')
        password_field = self.driver.find_element_by_xpath(
            '//*[@id="passwordForSignIn"]'
        )

        generate_random_delay()
        email_field.send_keys(id)
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

    def search_question(self, text):
        try:
            if self.switch_to_tab(CHEGG_RESULTS_PAGE_BASE_URL):
                self.search_question_on_results_page(text)
            else:
                self.search_question_on_homepage(text)
        except Exception as err:
            print(err)
            return False
        return True

    def search_question_on_homepage(self, text):
        try:
            self.driver.get(CHEGG_HOMEPAGE_URL)
            search_field = self.driver.find_element_by_xpath(
                '//*[@id="chegg-searchbox"]'
            )
            search_field.click()
            search_field.clear()
            generate_random_delay()
            search_field.send_keys(text)
            search_field.send_keys(Keys.RETURN)
        except Exception as err:
            print(err)
            return False
        return True

    def search_question_on_results_page(self, text):
        try:
            search_field = self.driver.find_element_by_xpath(
                '//*[@id="chegg-searchbox"]'
            )
            search_field.click()
            generate_random_delay()
            search_field.send_keys(text)
            search_field.send_keys(Keys.RETURN)
        except Exception as err:
            print(err)
            return False
        return True

    def process_results(self):
        try:
            generate_random_delay()
            self.select_study_tab()

            num_results = self.get_search_result_count()
            if num_results == -1:
                print("No results found for this question!")
                return False

            for i in range(1, num_results + 1):
                question = self.driver.find_element_by_css_selector(
                    f".automation-section-1-serp-result-{i} > div:nth-child(1) > a:nth-child(1) > div:nth-child(1) > div:nth-child(2)"
                )
                inner_html = question.get_attribute("innerHTML")
                total_em_tags = inner_html.count("<em>")
                total_words = len(inner_html.split())
                percentage = round(total_em_tags * 100 / total_words)
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
        Helper functions
    """

    def select_study_tab(self):
        # Check if "Study" tab is selected or not, if not then select it
        try:
            study_tab = self.driver.find_element_by_xpath(
                '//*[@id="search-results-tabs_tabheader_2"]'
            )
            is_selected = study_tab.get_attribute("aria-selected")
        except Exception as err:
            print(err)
            return False

        if is_selected != "true":
            study_tab.click()
        return True

    def switch_to_tab(self, url):
        try:
            num_tabs = len(self.driver.window_handles)
            for tab in self.driver.window_handles:
                self.driver.switch_to.window(tab)
                current_url = self.driver.current_url
                if re.search(f"{url}.*", current_url) != None:
                    return True  # Switch success
        except Exception as err:
            print(err)
        return False  # Switch failed

    def is_bot_detected(self):
        try:
            title_text = self.driver.find_element_by_xpath(
                "/html/body/section/div[2]/div/h1"
            ).text
        except:
            return False  # Bot not detected

        if title_text == "Please verify you are a human":
            return True  # Bot detected
        return False  # Bot not detected

    def get_search_result_count(self):
        try:
            num_results = len(
                self.driver.find_elements_by_css_selector(".detjfS > div")
            )
        except:
            return -1
        return num_results
