import random
from time import sleep


def generate_random_delay():
    delay = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    animation = "|/-\\"
    idx = 0
    for i in range(0, 10 * (delay + 1), 1):
        print(
            animation[idx % len(animation)], end="\r",
        )
        idx += 1
        sleep(0.1)
    print(" " * 30, end="\r")


def solve_captcha_manually():

    # TODO: Make a sound to alert the user

    print("Bot has been compromised! Complete the captcha!")
    is_captcha_complete = input("Is captcha filled? (y/n) ")
    while is_captcha_complete.lower() != "y":
        print("Please complete the captcha and try again")
        is_captcha_complete = input("Is captcha filled? (y/n) ")


def resolve_issues_manually():

    # TODO: Make a sound to alert the user

    print("Bot has messed up something, needs your help :(")
    print("Try to fix things manually, go back to the main menu and start again")
    is_everything_fixed = input("Are you done? (y/n) ")
    while is_everything_fixed.lower() != "y":
        print("Please fix things and let me know when its done")
        is_everything_fixed = input("Are you done? (y/n) ")


def get_skip_or_answer():

    # TODO: Make a sound to alert the user

    print("Voila! I have found positive result(s). Kindly review the results.")
    user_input = input("Should I (S)kip this question or do you want to (A)nswer? ")
    while user_input.lower() != "s" and user_input.lower() != "a":
        user_input = input("Enter either S (to skip) or A (to answer): ")
    return user_input


def get_submit_or_skip():
    user_input = "n"
    while user_input == "n":
        print("Do you want me to submit the answer? (y/n)")
        user_input = input("Enter: ")
        while user_input.lower() != "y" and user_input.lower() != "n":
            print("Invalid input")
            user_input = input("Enter: ")

        if user_input.lower() == "y":
            return "submit"

        print("Do you want me to skip the question? (y/n)")
        user_input = input("Enter: ")
        while user_input.lower() != "y" and user_input.lower() != "n":
            print("Invalid input")
            user_input = input("Enter: ")
        if user_input.lower() == "y":
            return "skip"


def shorten_text(text):
    words = text.split()
    short_text = " ".join(words[0 : min(50, len(words))])
    return short_text

