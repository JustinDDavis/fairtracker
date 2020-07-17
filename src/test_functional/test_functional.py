# https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import os

# Loading the Secrets from .env file
from dotenv import load_dotenv
load_dotenv()

# Temp
import time

class TestHomepageTest(unittest.TestCase):
    def setUp(self):
        self.host = 'http://localhost:8000'
        self.browser = webdriver.Chrome()
        self._signin_for_auth()


    def tearDown(self) -> None:
        self.browser.quit()

    def test_navigate_to_dashboard(self):
        # Navigate to the Fair page
        self.browser.get(self.host + "/fair")
        # Add a fair
        name = self.browser.find_element_by_name("name")
        name.send_keys("Test Fair")

        city = self.browser.find_element_by_name("city")
        city.send_keys("Test City")

        state = self.browser.find_element_by_name("state")
        state.send_keys("Test State")
        state.send_keys(Keys.RETURN)
        time.sleep(3)

        # Go through the table rows and delete
        delete_link = self.browser.find_element_by_xpath('//i[@class="fa-trash"]')
        delete_link.click()




    def _signin_for_auth(self):
        self.browser.get(self.host)
        self.assertIn("FairTracker | Home", self.browser.title)
        # Login from homepage
        login_button = self.browser.find_element_by_css_selector(".btn")  # .btn-outline-success .my-2 .my-sm-0")
        login_button.click()
        time.sleep(3)
        email_field = self.browser.find_element_by_name("email")
        email_field.send_keys(os.environ['LOGIN_EMAIL'])
        pass_field = self.browser.find_element_by_name("password")
        pass_field.send_keys(os.environ['LOGIN_PASSWORD'])
        pass_field.send_keys(Keys.RETURN)
        time.sleep(3)



