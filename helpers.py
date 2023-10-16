# helpers.py
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium import webdriver
import os
import requests
from secrets import token_hex
from mailtm import Email

class SeleniumEmailHelpers:
    def get_browser_options(self, browser):
       options = None
       if browser == "firefox":
            options = webdriver.FirefoxOptions()
       elif browser == "chrome":
        user_agent = "Mozilla/5.0 (Linux; Android 5.0; ASUS_T00G Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36"
        options = webdriver.ChromeOptions()
        user_data_dir = f"./chrome_profile_{token_hex(4)}"
        os.makedirs(user_data_dir, exist_ok=True)
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-translate")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        options.add_argument(f"user-agent={user_agent}")
       return options
    def fetch_confirmation_email_content(self, mailtm):
       try:
        api_url = "https://api.mail.tm/messages"
        headers = {
            "Authorization": f"Bearer {mailtm.token}"
        }
        response = requests.get(api_url, headers=headers)
        print("response :", response)
        if response.status_code == 200:
            email_data = response.json()
            print("200: ", email_data)
            if "hydra:member" in email_data and len(email_data["hydra:member"]) > 0:
                latest_email = email_data["hydra:member"][0]
                if "subject" in latest_email:
                    confirmation_email_subject = latest_email["subject"]
                    return confirmation_email_subject
        return ""
       except Exception as e:
        print(f"An error occurred while fetching email subject: {str(e)}")
        return ""
