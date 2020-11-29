from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re
from util.utility import generate_random_delay, solve_captcha_manually
from util.constant import *


class CheggBot:
    def __init__(self):
        self.current_qid = None

    def login_to_chegg(self, id, password):
        try:
            self.driver.get("https://www.chegg.com")
            sign_in_btn = self.driver.find_element_by_xpath('//*[@id="eggshell-15"]/a')

            generate_random_delay()  # Delay

            sign_in_btn.click()

            email_field = self.driver.find_element_by_xpath('//*[@id="emailForSignIn"]')
            password_field = self.driver.find_element_by_xpath(
                '//*[@id="passwordForSignIn"]'
            )

            generate_random_delay()  # Delay

            email_field.send_keys(id)
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)
        except Exception as err:
            print(err)

    ##############################################################################################################
    ##################################### GET QUESTION TEXT FUNCTIONS ############################################
    ##############################################################################################################

    def get_question_text(self):
        generate_random_delay()  # Delay
        try:
            self.current_qid = self._get_qid()
            print(f"Question ID: {self.current_qid}")
            # Check if question has image(s) or not
            if self._does_question_contain_images():
                text = self._get_question_transcript()
            else:
                text = self.driver.find_element_by_class_name("question").get_attribute(
                    "innerText"
                )
            return text
        except Exception as err:
            print(err)
        return None

    def _does_question_contain_images(self):
        try:
            inner_html = self.driver.find_element_by_class_name(
                "question"
            ).get_attribute("innerHTML")
            is_img_tag_present = re.search("<img ", inner_html, re.M)
            if is_img_tag_present:
                return True
        except Exception as err:
            print(err)
        return False

    def _get_question_transcript(self):
        try:
            original_tab = self.driver.current_window_handle
            self.open_new_tab(CHEGG_QUESTION_BASE_URL + self.current_qid)
            # Get the transcript
            transcript = self.driver.find_element_by_class_name(
                "transcribed-image-text-show"
            ).text

            generate_random_delay()  # Delay

            self.close_recent_tab()
            # Switch to original tab
            self.driver.switch_to.window(original_tab)
            return transcript
        except Exception as err:
            print(err)
        return None

    def _get_qid(self):
        try:
            logs = self.driver.get_log("browser")
            qids = []
            for log in logs:
                if log["level"] == "INFO":
                    match = re.search("SQid : (\d+)", log["message"])
                    if match is not None:
                        qids.append(match.group(1))
            # Return last captured qid
            return qids[-1]
        except Exception as err:
            print(err)
        return None

    ##############################################################################################################
    ########################################### SEARCH FUNCTIONS #################################################
    ##############################################################################################################

    def search_question(self, text):
        generate_random_delay()  # Delay
        try:
            if self.switch_to_tab_with_matching_url(CHEGG_RESULTS_PAGE_BASE_URL):
                self._search_question_on_results_page(text)
            else:
                self.open_new_tab(CHEGG_HOMEPAGE_URL)
                self._search_question_on_homepage(text)
        except Exception as err:
            print(err)
            return False
        return True

    def _search_question_on_homepage(self, text):
        try:
            search_field = self.driver.find_element_by_xpath(
                '//*[@id="chegg-searchbox"]'
            )
            search_field.click()

            generate_random_delay()  # Delay

            search_field.send_keys(text)

            generate_random_delay()  # Delay

            search_field.send_keys(Keys.RETURN)
        except Exception as err:
            print(err)
            return False
        return True

    def _search_question_on_results_page(self, text):
        try:
            search_field = self.driver.find_element_by_xpath(
                '//*[@id="chegg-searchbox"]'
            )
            search_field.click()
            self.driver.execute_script(
                "document.querySelector('#chegg-searchbox').value = ''"
            )

            generate_random_delay()  # Delay

            search_field.send_keys(text)
            search_field.send_keys(Keys.RETURN)
        except Exception as err:
            print(err)
            return False
        return True

    def process_results(self):
        try:
            self._select_study_tab()
        except Exception as err:
            print(err)
            # At this point, reCaptcha comes quite often
            if self.is_bot_compromised():
                if not self.solve_captcha_automatically():
                    solve_captcha_manually()
            self._select_study_tab()

        try:
            num_results = self._get_search_result_count()
            if num_results == -1:
                return 0
        except Exception as err:
            print(err)
            return -1

        try:
            print("Search results:")
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
                    return 1
        except Exception as err:
            print(err)
        return 0

    ##############################################################################################################
    ########################################### HELPER FUNCTIONS #################################################
    ##############################################################################################################

    def start_answering(self):
        try:
            self.driver.get(CHEGG_EXPERT_ANSWER_URL)
        except Exception as err:
            print(err)

    def skip_question(self):
        pass

    def click_on_answer(self):
        try:
            self.driver.find_element_by_id("ques-ans-btn").click()
        except Exception as err:
            print(err)

    def stop_answering(self):
        try:
            self.driver.find_element_by_id("skipQuestion-Leave").click()
        except Exception as err:
            print(err)

    def submit_answer(self):
        pass

    def open_new_tab(self, url):
        try:
            # Open a new blank tab
            self.driver.execute_script(f"window.open('')")
            # Switch to newly opened tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            # Open question page
            self.driver.get(url)
        except Exception as err:
            print(err)

    def close_recent_tab(self):
        try:
            # Switch to recently opened tab
            self.driver.switch_to.window(self.driver.window_handles[-1])
            # Close the current tab
            self.driver.close()
        except Exception as err:
            print(err)

    def refresh_current_tab(self):
        self.driver.refresh()

    def _select_study_tab(self):
        # Check if "Study" tab is selected or not, if not then select it
        try:
            study_tab = self.driver.find_element_by_xpath(
                '//*[@id="search-results-tabs_tabheader_2"]'
            )
            is_selected = study_tab.get_attribute("aria-selected")

            if is_selected != "true":
                study_tab.click()
        except Exception as err:
            raise err

    def switch_to_tab_with_matching_url(self, url):
        try:
            for tab in self.driver.window_handles:
                self.driver.switch_to.window(tab)
                current_url = self.driver.current_url
                if re.search(f"{url}.*", current_url) != None:
                    return True  # Switch success
        except Exception as err:
            print(err)
        return False  # Switch failed

    def is_bot_compromised(self):
        try:
            title_text = self.driver.find_element_by_xpath(
                "/html/body/section/div[2]/div/h1"
            ).text
        except:
            return False  # Bot not detected

        if title_text == "Please verify you are a human":
            return True  # Bot detected
        return False  # Bot not detected

    def solve_captcha_automatically(self):
        try:
            iframe = self.driver.find_element_by_xpath(
                "//iframe[starts-with(@name, 'a-') and starts-with(@src, 'https://www.google.com/recaptcha')]"
            )
            self.driver.switch_to.frame(iframe)
            self.driver.find_element_by_css_selector("div.rc-anchor-content").click()
            self.driver.switch_to.default_content()
        except Exception as err:
            print(err)
            return False

        generate_random_delay()  # Delay
        return True

    def _get_search_result_count(self):
        num_results = 0
        try:
            container = self.driver.find_element_by_xpath(
                '//*[@id="se-search-serp"]/div/div[1]/div/div[2]/div[2]/div'
            )
            while num_results < 8 and container.find_element_by_xpath(
                f'./div[@data-area="result{num_results + 1}"]'
            ):
                num_results += 1

        except Exception as err:
            print(err)
            if num_results == 0:
                return -1
        return num_results

