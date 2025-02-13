"""Unittests for the guest_chekout method in the HotelManager class"""

import json
import os
from unittest import TestCase
from freezegun import freeze_time
from UC3MTravel.HotelManagementException import HotelManagementException
from UC3MTravel.HotelManager import HotelManager


class TestGuestCheckout(TestCase):
    """Contains all the tests for the guest_checkout method"""
    @freeze_time("2023-06-01")
    def test_guest_checkout_tc1(self):
        """Valid test case. File does not exist. Returns True"""

        # Initial deletion of files to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")
        if os.path.exists("checkouts.json"):
            os.remove("checkouts.json")


        # Room reservation
        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        # Input data for the guest arrival
        input_data = {
            "Localizer": value,
            "IdCard": "02166140T"
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        # Get room key
        room_key = my_reservation.guestArrival("input_data.json")

        # Checkout
        with freeze_time("2023-06-05"):
            confirmation = my_reservation.guestCheckOut(room_key)
            self.assertEqual(confirmation, True)

    @freeze_time("2023-06-01")
    def test_guest_checkout_tc2(self):
        """Valid test case. File exists (empty). Returns True"""

        # Initial deletion of files to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")
        if os.path.exists("checkouts.json"):
            os.remove("checkouts.json")

        # Create empty checkouts file
        with open("checkouts.json", "w", encoding="utf-8") as file:
            json.dump([], file)

        # Room reservation
        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        # Input data for the guest arrival
        input_data = {
            "Localizer": value,
            "IdCard": "02166140T"
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        # Get room key
        room_key = my_reservation.guestArrival("input_data.json")

        # Checkout
        with freeze_time("2023-06-05"):
            confirmation = my_reservation.guestCheckOut(room_key)
            self.assertEqual(confirmation, True)

    @freeze_time("2023-06-01")
    def test_guest_checkout_tc3(self):
        """Valid test case. File exists (not empty). Returns True"""
        # Initial deletion of the file reservations.json to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")
        if os.path.exists("checkouts.json"):
            os.remove("checkouts.json")

        # Room reservations to validate checkin
        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")
        value1 = my_reservation.roomReservation("26867719Q", "6532133452789111", "jose lopez",
                                                 "666666666", "01/06/2023", "suite", "4")
        value2 = my_reservation.roomReservation("61253812M", "6532133452789111", "jose lopez",
                                                 "666666666", "01/06/2023", "suite", "4")

        # Input data for the guest arrival
        input_data = {
            "Localizer": value,
            "IdCard": "02166140T"
        }
        input_data1 = {
            "Localizer": value1,
            "IdCard": "26867719Q"
        }
        input_data2 = {
            "Localizer": value2,
            "IdCard": "61253812M"
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data1, file)
        room_key1 = my_reservation.guestArrival("input_data.json")
        self.assertEqual(len(room_key1), 64)
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data2, file)
        room_key2 = my_reservation.guestArrival("input_data.json")
        self.assertEqual(len(room_key2), 64)

        # Save the actual test reservation
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)
        room_key = my_reservation.guestArrival("input_data.json")

        # Checkouts
        with freeze_time("2023-06-05"):
            confirmation = my_reservation.guestCheckOut(room_key)
            self.assertEqual(confirmation, True)
            confirmation = my_reservation.guestCheckOut(room_key1)
            self.assertEqual(confirmation, True)
            confirmation = my_reservation.guestCheckOut(room_key2)
            self.assertEqual(confirmation, True)

    def test_guest_arrival_tc4(self):
        """Invalid test case. Room key's length is less than 64. Returns the exception message"""

        # Initial deletion of files to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")

        # Room reservation
        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        # Input data for the guest arrival
        input_data = {
            "Localizer": value[:30],
            "IdCard": "02166140T"
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        # Get room key
        room_key = my_reservation.guestArrival("input_data.json")

        # Checkout
        with freeze_time("2023-06-05"):
            with self.assertRaises(HotelManagementException) as context:
                my_reservation.guestCheckOut(room_key)
            self.assertEqual(str(context.exception), "Invalid room key format")


    def test_guest_arrival_tc5(self):
        """Invalid test case. Room key's type is not string. Returns the exception message"""

        # Initial deletion of files to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")

        # Room reservation
        my_reservation = HotelManager()

        # Input data for the guest arrival
        input_data = {
            "Localizer": "5f07422a1f017951169d1b21b745e6a1",
            "IdCard": "02166140T"
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        try:
            room_key = 123456789  # Int type room key
            my_reservation.guestCheckOut(room_key)
            self.assertEqual(1, 0)  # This line should not be executed if the test is correct.

        except HotelManagementException as e:
            self.assertEqual(str(e), "Invalid room key format")

    def test_guest_arrival_tc6(self):
        """Invalid test case. There is no input. Returns the exception message"""

        # Initial deletion of files to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")

        # Room reservation
        my_reservation = HotelManager()

        try:
            my_reservation.guestCheckOut("room_key_value")
            self.assertEqual(1, 0)  # This line should not be executed if the test is correct.
        except HotelManagementException as e:
            self.assertEqual(str(e), "Invalid room key format")

    @freeze_time("2023-06-01")
    def test_guest_arrival_tc7(self):
        """Invalid test case. Wrong departure date. Returns the exception message"""

        # Initial deletion of files to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")

        # Room reservation
        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        # Input data for the guest arrival
        input_data = {
            "Localizer": value,
            "IdCard": "02166140T"
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        # Guest arrival. Get room key
        room_key = my_reservation.guestArrival("input_data.json")

        # Check with an incorrect departure date
        try:
            my_reservation.guestCheckOut(room_key)  # Attempt to check out
            self.assertEqual(1, 0)  # This line should not be executed if the test is correct.
        except HotelManagementException as e:
            self.assertEqual(str(e), "Departure date does not match today's date")

    @freeze_time("2023-06-01")
    def test_guest_arrival_tc8(self):
        """Invalid test case. Stays file does not exist. Returns the exception message"""

        # Initial deletion of files to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")
        if os.path.exists("checkouts.json"):
            os.remove("checkouts.json")

        # Room reservation
        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        # Input data for the guest arrival
        input_data = {
            "Localizer": value,
            "IdCard": "02166140T"
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        # Get room key
        room_key = my_reservation.guestArrival("input_data.json")

        if os.path.exists("stays.json"):
            os.remove("stays.json")

        # Checkout
        with freeze_time("2023-06-05"):
            try:
                my_reservation.guestCheckOut(room_key)
                self.assertEqual(1, 0)  # This line should not be executed if the test is correct.
            except HotelManagementException as e:
                self.assertEqual(str(e), "Stays file does not exist")
