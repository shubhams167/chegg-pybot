from bin.chrome_chegg_bot import *
from bin.firefox_chegg_bot import *
from util.utility import (
    get_submit_or_skip,
    solve_captcha_manually,
    resolve_issues_manually,
    shorten_text,
    get_skip_or_answer,
)


def autopilot(driver: ChromeCheggBot):
    print("Autopilot ON!")
    print("Sit back and relax, let the bot do its job.")
    driver.start_answering()
    while True:
        text = driver.get_question_text()
        if text is None:
            if driver.is_bot_compromised():
                solve_captcha_manually()
            else:
                resolve_issues_manually()
            driver.switch_to_tab_with_matching_url(CHEGG_EXPERT_ANSWER_URL)
            driver.skip_question()
            continue

        if not driver.search_question(shorten_text(text)):
            # Check if bot has been detected
            if driver.is_bot_compromised():
                solve_captcha_manually()
            else:
                resolve_issues_manually()
            driver.switch_to_tab_with_matching_url(CHEGG_EXPERT_ANSWER_URL)
            driver.skip_question()
            continue

        result = driver.process_results()
        if result == -1:
            # Check if bot has been detected
            if driver.is_bot_compromised():
                solve_captcha_manually()
            else:
                resolve_issues_manually()
            driver.switch_to_tab_with_matching_url(CHEGG_EXPERT_ANSWER_URL)
            driver.skip_question()
            continue

        driver.switch_to_tab_with_matching_url(CHEGG_EXPERT_ANSWER_URL)

        if result == 1:
            user_input = get_skip_or_answer()
            if user_input == "a":
                driver.click_on_answer()
                submit_or_skip = get_submit_or_skip()
                if submit_or_skip == "submit":
                    driver.submit_answer()
                    continue

        driver.skip_question()


def search_automatically(driver: ChromeCheggBot):
    driver.switch_to_tab_with_matching_url(CHEGG_EXPERT_ANSWER_URL)
    text = driver.get_question_text()
    if text is None:
        if driver.is_bot_compromised():
            solve_captcha_manually()
            return
        resolve_issues_manually()
        return

    if not driver.search_question(shorten_text(text)):
        # Check if bot has been detected
        if driver.is_bot_compromised():
            solve_captcha_manually()
            return
        resolve_issues_manually()
        return

    result = driver.process_results()
    if result == -1:
        # Check if bot has been detected
        if driver.is_bot_compromised():
            solve_captcha_manually()
            return
        resolve_issues_manually()
        return
    if result == 1:
        print("Voila! I have found positive result(s). Kindly review the results.")


def main():
    chrome = ChromeCheggBot()

    print("******************************************")
    print("********** WELCOME TO CHEGG BOT **********")
    print("******************************************\n")
    option = 0
    while option != 3:
        print("************* MAIN MENU **************")
        print("1. Start Autopilot")
        print("2. Search a question (fully automated)")
        print("3. Exit")
        option = int(input("Choose an option: "))
        print()
        if option == 1:
            autopilot(chrome)
        elif option == 2:
            search_automatically(chrome)
        elif option == 3:
            print("Goodbye!")
        else:
            print("Invalid option. Try again.")
        print()


if __name__ == "__main__":
    main()
