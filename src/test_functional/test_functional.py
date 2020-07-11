# https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de
from selenium import webdriver
import unittest


class TestHomepageTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_home_page(self):
        self.browser.get('http://localhost:8000')
        self.assertIn("FairTracker | Home", self.browser.title)
        self.assertIn("Learn more!", self.browser.find_element_by_css_selector("a.home-button"))



