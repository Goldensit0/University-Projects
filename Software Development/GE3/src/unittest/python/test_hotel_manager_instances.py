from unittest import TestCase
from uc3m_travel.hotel_manager import HotelManager
from uc3m_travel.hotel_management_exception import HotelManagementException


class TestHotelManager(TestCase):
    def setUp(self):
        self.manager = HotelManager()

    def test_singleton_instance(self):
        # Test if the instance is a singleton
        manager2 = HotelManager()
        self.assertIs(self.manager, manager2)

    def test_validatecreditcard(self):
        # Test the validatecreditcard method
        valid_credit_card = "5105105105105100"
        invalid_credit_card = "1234567890"  # Invalid length
        self.assertTrue(self.manager.validatecreditcard(valid_credit_card))
        with self.assertRaises(HotelManagementException):
            self.manager.validatecreditcard(invalid_credit_card)
