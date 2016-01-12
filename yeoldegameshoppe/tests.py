import sys

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from pyvirtualdisplay import Display


class YogsSeleniumTest(StaticLiveServerTestCase):
    """A base class to use for yeoldegameshoppe's Selenium tests.

    You can access the webdriver from self.selenium."""

    @classmethod
    def setUpClass(cls):
        super(YogsSeleniumTest, cls).setUpClass()

        # start virtual display if on linux
        if sys.platform == "linux" or sys.platform == "linux2":
            cls.vdisplay = Display(visible=0, size=(1024, 768))
            cls.vdisplay.start()

        # start browser
        cls.selenium = WebDriver()
        cls.selenium.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()

        if sys.platform == "linux" or sys.platform == "linux2":
            cls.vdisplay.stop()

        super(YogsSeleniumTest, cls).tearDownClass()

    def login_user(self, username, password):
        """Logs in as the given user."""
        self.selenium.get('%s%s' % (self.live_server_url, '/logout'))
        self.selenium.get('%s%s' % (self.live_server_url, '/login'))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(password)
        self.selenium.find_element_by_xpath('//button[@type="submit"]').click()
