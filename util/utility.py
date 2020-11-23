import random
from time import sleep


def generate_random_delay():
    delay = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    print(f"Waiting for {delay} seconds...")
    sleep(delay)


def resolve_captcha():
    print("Bot has been compromised! Complete the captcha!")
    captchaComplete = input("Is captcha filled? (y/n) ")
    while captchaComplete.lower() != "y":
        print("Please complete the captcha and try again.")
        captchaComplete = input("Is captcha filled? (y/n) ")
