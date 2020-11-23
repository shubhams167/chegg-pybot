from bin.chrome_chegg_bot import *
from bin.firefox_chegg_bot import *
from util.utility import resolve_captcha


def autopilot(chrome, firefox):
    print("Autopilot ON!")
    print("Sit back and relax, let the bot do its job.")
    # TODO: Implement autopilot


def search_automatically(chrome, firefox):
    # TODO: Get question from the Chrome browser
    pass


def search_manually(driver):
    text = input("Enter question text: ")
    if not driver.search_question(text):
        # Check if bot has been detected
        if driver.is_bot_detected():
            resolve_captcha()
        else:
            print("Something went wrong.")

    if not driver.process_results():
        # Check if bot has been detected
        if driver.is_bot_detected():
            resolve_captcha()
        else:
            print("Something went wrong.")


def main():
    print("********************************")
    print("***** WELCOME TO CHEGG BOT *****")
    print("********************************\n")

    # Create two instances
    firefox = FirefoxCheggBot()
    chrome = ChromeCheggBot()
    # chrome = None
    # firefox = None

    option = 0
    while option != 4:
        print("************* MAIN MENU **************")
        print("1. Start Autopilot")
        print("2. Search a question (fully automated)")
        print("3. Search a question (manual input)")
        print("4. Exit")
        option = int(input("Choose an option: "))
        print()
        if option == 1:
            autopilot(chrome, firefox)
        elif option == 2:
            search_automatically(chrome, firefox)
        elif option == 3:
            search_manually(firefox)
        elif option == 4:
            print("Goodbye!")
        else:
            print("Invalid option. Try again.")
        print()


if __name__ == "__main__":
    main()
