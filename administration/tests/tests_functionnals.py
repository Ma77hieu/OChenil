
import os
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from generic.constants import (BOOKING_DELETION_OK,
                               UNAVAILABILITY_OK,
                               IMPOSSIBLE_UNAVAILABILITY)
from generic.tests import login, ensure_change_page


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
            specific_options.add_argument("--start-maximized")
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

    def test_cancel_booking(self):
        """test the cancelation of a booking"""
        login(self, 'admin')
        booking_field = Select(
            self.selenium.find_element_by_id('id_id_to_be_canceled'))
        booking_field.select_by_index(0)
        cancel_booking_btn = self.selenium.find_element_by_id(
            "cancel_booking_btn")
        cancel_booking_btn.send_keys(Keys.RETURN)
        ensure_change_page(self)
        booking_canceled = False
        if BOOKING_DELETION_OK in self.selenium.page_source:
            booking_canceled = True
        assert booking_canceled is True

    def test_declare_unavailability_ok(self):
        """test the successfull declaration of an unavailability"""
        dates = [
            ('id_start_month', 2),
            ('id_start_day', 11),
            ('id_start_year', 0),
            ('id_end_month', 2),
            ('id_end_day', 12),
            ('id_end_year', 0)
        ]
        self.declare_unavailability(dates)
        unavailability_declared = False
        if UNAVAILABILITY_OK in self.selenium.page_source:
            unavailability_declared = True
        assert unavailability_declared is True

    def test_declare_unavailability_not_ok(self):
        """test the unsuccessfull declaration of an unavailability"""
        dates = [
            ('id_start_month', 7),
            ('id_start_day', 20),
            ('id_start_year', 0),
            ('id_end_month', 7),
            ('id_end_day', 21),
            ('id_end_year', 0)
        ]
        self.declare_unavailability(dates)
        unavailability_possible = True
        if IMPOSSIBLE_UNAVAILABILITY in self.selenium.page_source:
            unavailability_possible = False
        assert unavailability_possible is False

    def declare_unavailability(self, dates):
        """used by both tests regarding unavailability declaration"""
        login(self, 'admin')
        box_select = Select(
            self.selenium.find_element_by_id('id_id_box'))
        box_select.select_by_index(0)
        for field in dates:
            dog_size_field = Select(self.selenium.find_element_by_id(field[0]))
            dog_size_field.select_by_index(field[1])
        unavailability_btn = self.selenium.find_element_by_id(
            "unavailability_btn")
        unavailability_btn.send_keys(Keys.RETURN)
        ensure_change_page(self)
        pass
