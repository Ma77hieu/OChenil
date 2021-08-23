from decouple import config
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from generic.constants import NO_AVAILABILITY
from generic.tests import login, ensure_change_page
from generic.custom_logging import custom_log
import time


class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['fixture_db.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        is_travis = 'TRAVIS' in os.environ
        # detect if tests run locally or in server through travis
        if not is_travis:
            specific_options = Options()
            specific_options.add_argument("--start-maximized")
            cls.selenium = WebDriver(options=specific_options)
        elif is_travis:
            specific_options = Options()
            specific_options.add_argument("--no-sandbox")
            specific_options.add_argument("--headless")
            specific_options.add_argument("--disable-dev-shm-usage")
            specific_options.add_argument("--disable-gpu")
            cls.selenium = WebDriver(options=specific_options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_add_dog(self):
        """test the add dog function"""
        login(self, 'regular_user')
        field_value_match = [
            ('id_dog_name', 'DOG_NAME'),
            ('id_dog_age', 'DOG_AGE'),
            ('id_dog_race', 'DOG_RACE')
        ]
        for field in field_value_match:
            to_be_filled = self.selenium.find_element_by_id(field[0])
            to_be_filled.send_keys(config(field[1]))
        dog_size_field = Select(self.selenium.find_element_by_id('id_dogsize'))
        dog_size_field.select_by_index(1)
        add_dog_btn = self.selenium.find_element_by_id(
            "add_dog_btn")
        add_dog_btn.send_keys(Keys.RETURN)
        ensure_change_page(self)
        dog_added = False
        if "test_race" in self.selenium.page_source:
            dog_added = True
        assert dog_added is True

    def test_add_booking_ok(self):
        """test the add booking function when there is available room"""
        login(self, 'regular_user')
        self.check_navbar_collapsed()
        booking_btn = self.selenium.find_element_by_id(
            "menu_booking_link_usr")
        booking_btn.send_keys(Keys.RETURN)
        ensure_change_page(self)
        dog_name_field = Select(
            self.selenium.find_element_by_id('id_dog_name'))
        dog_name_field.select_by_index(0)
        field_value_match = [
            ('id_start_date_month', 9),
            ('id_start_date_day', 11),
            ('id_start_date_year', 1),
            ('id_end_date_month', 9),
            ('id_end_date_day', 12),
            ('id_end_date_year', 1)
        ]
        for field in field_value_match:
            dog_size_field = Select(self.selenium.find_element_by_id(field[0]))
            dog_size_field.select_by_index(field[1])
        booking_btn_in_page = self.selenium.find_element_by_id(
            "booking_btn_in_page")
        booking_btn_in_page.send_keys(Keys.RETURN)
        ensure_change_page(self)
        booking_added = False
        if "Oct. 12, 2022" in self.selenium.page_source:
            booking_added = True
        assert booking_added is True

    def test_add_booking_not_ok(self):
        """test the add booking function when there is no available room"""
        login(self, 'regular_user')
        self.check_navbar_collapsed()
        booking_btn = self.selenium.find_element_by_id(
            "menu_booking_link_usr")
        booking_btn.send_keys(Keys.RETURN)
        ensure_change_page(self)
        dog_name_field = Select(
            self.selenium.find_element_by_id('id_dog_name'))
        dog_name_field.select_by_index(1)
        field_value_match = [
            ('id_start_date_month', 7),
            ('id_start_date_day', 14),
            ('id_start_date_year', 0),
            ('id_end_date_month', 7),
            ('id_end_date_day', 17),
            ('id_end_date_year', 0)
        ]
        for field in field_value_match:
            dog_size_field = Select(self.selenium.find_element_by_id(field[0]))
            dog_size_field.select_by_index(field[1])
        booking_btn_in_page = self.selenium.find_element_by_id(
            "booking_btn_in_page")
        booking_btn_in_page.send_keys(Keys.RETURN)
        ensure_change_page(self)
        booking_added = True
        if (NO_AVAILABILITY in self.selenium.page_source) and (
            "Aug. 16, 2021" not in self.selenium.page_source
        ):
            booking_added = False
        assert booking_added is False

    def check_navbar_collapsed(self):
        """check foor the presence of the collapsed navbar menu button,
        click on the button to deploy the navbar if it was collapsed"""
        collapsed_navbar_button = (
            self.selenium.find_element_by_class_name(
                "fa-bars"))
        is_navbar_collapsed = collapsed_navbar_button.is_displayed()
        if is_navbar_collapsed:
            collapsed_navbar_button.send_keys(Keys.RETURN)
