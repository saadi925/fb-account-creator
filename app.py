import secrets
from randomdata import select_random_date_of_birth, generate_random_name
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QPushButton, QMessageBox, QLineEdit, QRadioButton, QCheckBox, QLabel
from PyQt5.QtCore import Qt
from helpers import SeleniumEmailHelpers
import time
from mailtm import Email
from shutil import rmtree
import os
from threading import Thread

class FacebookRegistrationApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.selenium_email_helpers = SeleniumEmailHelpers()
        self.driver = None
        
        self.setStyleSheet("background-color: #121212; color: #FFFFFF;")  # Dark theme

    def init_ui(self):
        self.setWindowTitle("Facebook Account Registration")
        self.setGeometry(100, 100, 400, 350)

        layout = QVBoxLayout()

        title_label = QLabel("Facebook Account Registration")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; color: #187bcd;")  # Blue title
        layout.addWidget(title_label)

        self.register_button = QPushButton("Register Account")
        self.register_button.clicked.connect(self.start_registration)
        self.register_button.setStyleSheet("background-color: #187bcd; color: #FFFFFF;")
        layout.addWidget(self.register_button)

        self.default_button = QPushButton("Load Default Configuration")
        self.default_button.clicked.connect(self.load_default_configuration)
        self.default_button.setStyleSheet("background-color: #6eb82c; color: #FFFFFF;")
        layout.addWidget(self.default_button)

        self.proxy_input = QLineEdit(self)
        self.proxy_input.setPlaceholderText("Enter Proxy (e.g., http://proxy.example.com:8080)")
        self.proxy_input.setStyleSheet("background-color: #111; color: #FFFFFF;")  # Dark input field
        layout.addWidget(self.proxy_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Enter Email (optional)")
        self.email_input.setStyleSheet("background-color: #111; color: #FFFFFF;")
        layout.addWidget(self.email_input)

        browser_label = QLabel("Select Browser:")
        browser_label.setStyleSheet("font-weight: bold; color: #FFFFFF;")
        layout.addWidget(browser_label)

        self.firefox_radio = QRadioButton("Firefox")
        self.firefox_radio.setStyleSheet("color: #FFFFFF;")  # White radio button text
        self.chrome_radio = QRadioButton("Chrome")
        self.chrome_radio.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.firefox_radio)
        layout.addWidget(self.chrome_radio)

        basic_checkbox_label = QLabel("Registration Type:")
        basic_checkbox_label.setStyleSheet("font-weight: bold; color: #FFFFFF;")
        layout.addWidget(basic_checkbox_label)

        self.basic_checkbox = QCheckBox("Basic")
        self.basic_checkbox.setStyleSheet("color: #FFFFFF;")
        layout.addWidget(self.basic_checkbox)

        self.setLayout(layout)


    def load_default_configuration(self):
        self.proxy_input.setText("")
        self.chrome_radio.setChecked(True)
        self.basic_checkbox.setChecked(False)

    def create_chrome_profile(self):
        profile_dir = os.path.join(os.getcwd(), "chrome_profiles", secrets.token_hex(8))

        if os.path.exists(profile_dir):
            rmtree(profile_dir)

        chrome_options = ChromeOptions()
        chrome_options.add_argument(f'--user-data-dir={profile_dir}')
        return chrome_options

    def generate_random_password(self, length=11):
        characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"
        password = "".join(secrets.choice(characters) for _ in range(length))
        return password

    def extract_verification_code(self, subject):
        code_match = re.search(r'FB-(\d{5})', subject)
        if code_match:
            code = code_match.group(1)
            return code
        return None

    def check_proxy(self, proxy):
        try:
            response = requests.get("https://www.google.com", proxies={"http": proxy, "https": proxy}, timeout=10)
            if response.status_code == 200:
                return True
        except Exception as e:
            pass
        return False

    def start_registration(self):
        self.register_button.setEnabled(False)
        thread = Thread(target=self.register_account)
        thread.start()

    def register_account(self):
        try:
            mailtm = Email()
            if not self.email_input.text():
                mailtm.register()
            else:
                mailtm.address = self.email_input.text()

            if self.firefox_radio.isChecked():
                options = self.selenium_email_helpers.get_browser_options("firefox")
                self.driver = webdriver.Firefox(options=options)
            elif self.chrome_radio.isChecked():
                chrome_options = self.create_chrome_profile()
                self.driver = webdriver.Chrome(options=chrome_options)

            password = self.generate_random_password()
            firstname, lastname = generate_random_name()

            if self.basic_checkbox.isChecked():
                self.driver.get("https://mbasic.facebook.com/reg")
            else:
                self.driver.get("https://facebook.com/reg")

            self.driver.find_element(By.NAME, "firstname").send_keys(firstname)
            self.driver.find_element(By.NAME, "lastname").send_keys(lastname)

            self.driver.find_element(By.NAME, "reg_email__").send_keys(mailtm.address)

            if not self.basic_checkbox.isChecked():
                self.driver.find_element(By.NAME, "reg_email_confirmation__").send_keys(mailtm.address)

            self.driver.find_element(By.NAME, "reg_passwd__").send_keys(password)

            select_random_date_of_birth(driver=self.driver)

            gender_option = self.driver.find_element(By.NAME, "sex")
            gender_option.click()

            if self.basic_checkbox.isChecked():
                submit = self.driver.find_element(By.NAME, "submit")
                submit.click()
                confirmation_code = None
                start_time = time.time()
                while time.time() - start_time < 600:
                    confirmation_email_subject = self.selenium_email_helpers.fetch_confirmation_email_content(mailtm)
                    verification_code = self.extract_verification_code(confirmation_email_subject)
                    if verification_code is not None:
                        confirmation_code = verification_code
                        break
                if confirmation_code :
                    print(f"your fb verification code is : {confirmation_code}")

                    time.sleep(10)

            if not self.basic_checkbox.isChecked():
                confirm_email_button = self.driver.find_element(By.NAME, "websubmit")
                confirm_email_button.click()

                confirmation_code = None
                start_time = time.time()
                while time.time() - start_time < 600:
                    confirmation_email_subject = self.selenium_email_helpers.fetch_confirmation_email_content(mailtm)
                    verification_code = self.extract_verification_code(confirmation_email_subject)
                    if verification_code is not None:
                        confirmation_code = verification_code
                        break

                    time.sleep(10)

                if confirmation_code:
                    code_input = self.driver.find_element(By.NAME, "code")
                    code_input.send_keys(confirmation_code)

                    next_button = self.driver.find_element(By.XPATH, "//span[text()='Next']")
                    next_button.click()
            
            # The driver is not closed here to keep it running

            if not self.email_input.text() and not self.basic_checkbox.isChecked():
                QMessageBox.information(self, "Registration Successful",
                                        "Registration successful!\nEmail: {}\nPassword: {}".format(mailtm.address, password))
            print("finished")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            if self.driver:
                self.driver.quit()
        finally:
            self.register_button.setEnabled(True)

