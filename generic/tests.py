from decouple import config
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from generic.constants import WAIT_TIME
import time


# Create your tests here.


def ensure_change_page(self):
    """function used by other test to let the <body> of the new page loads
    when a change of page is required for tests"""
    timeout = 2
    WebDriverWait(self.selenium, timeout).until(
        lambda driver: driver.find_element_by_tag_name('body'))
    time.sleep(WAIT_TIME)


def login(self, role):
    """login function used by other tests

    Parameters:
    role (can be regular_user or admin based on user type)
    """
    timeout = 2
    if role == "regular_user":
        USER = config('USER_LOGIN')
        PWD = config('USER_PWD')
    elif role == "admin":
        USER = config('ADMIN_USER_LOGIN')
        PWD = config('ADMIN_USER_PWD')
    self.selenium.get('{}'.format(self.live_server_url + '/signin'))
    username_input = self.selenium.find_elements_by_name("username")[0]
    username_input.send_keys(USER)
    password_input = self.selenium.find_elements_by_name("password")[0]
    password_input.send_keys(PWD)
    password_input.send_keys(Keys.RETURN)
    WebDriverWait(self.selenium, timeout).until(
        lambda driver: driver.find_element_by_tag_name('body'))
    time.sleep(WAIT_TIME)
