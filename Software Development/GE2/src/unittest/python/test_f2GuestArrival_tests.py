"""Unittests for the guest_arrival method in the HotelStay class"""

from unittest import TestCase
import json
import os
from freezegun import freeze_time
from UC3MTravel.HotelManager import HotelManager
from UC3MTravel.HotelManagementException import HotelManagementException


class TestGuestArrival(TestCase):
    """Contains all the tests for the guest_arrival method"""

    @freeze_time("2023-06-01")
    def test_guest_arrival_tc1(self):
        """Valid test case. All the parameters are correct. No files exist."""

        # Initial deletion of the files to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")

        # Room reservation to validate checkin
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

        room_key = my_reservation.guestArrival("input_data.json")
        self.assertEqual(len(room_key), 64)
        self.assertEqual(room_key, "ee389f4b9bf3494f6ca577b6e5b4a031d348e940ecb44cd8e3b468a97e20466a")

    @freeze_time("2023-06-01")
    def test_guest_arrival_tc2(self):
        """Valid test case. All the parameters are correct. Files exists, empty."""

        # Initial deletion of the file reservations.json to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")
        with open("stays.json", "w", encoding="utf-8") as file:
            json.dump([], file)

        # Room reservation to validate checkin
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

        room_key = my_reservation.guestArrival("input_data.json")
        self.assertEqual(len(room_key), 64)
        self.assertEqual(room_key, "ee389f4b9bf3494f6ca577b6e5b4a031d348e940ecb44cd8e3b468a97e20466a")

    @freeze_time("2023-06-01")
    def test_guest_arrival_tc3(self):
        """Valid test case. All the parameters are correct. Files exists, not empty."""

        # Initial deletion of the file reservations.json to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        if os.path.exists("stays.json"):
            os.remove("stays.json")

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

        self.assertEqual(len(room_key), 64)
        self.assertEqual(room_key, "ee389f4b9bf3494f6ca577b6e5b4a031d348e940ecb44cd8e3b468a97e20466a")

    def test_guest_arrival_tc4(self):
        """Invalid test case. The localizer is incorrect. Returns the exception message"""

        # Initial deletion of the file reservations.json to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")

        # Room reservation
        my_reservation = HotelManager()
        my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        # Input data for the guest arrival. Incorrect localizer but correct IDCard
        input_data = {
            "Localizer": " ",
            "IdCard": "02166140T"
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        room_key = my_reservation.guestArrival("input_data.json")
        self.assertEqual(room_key, "Invalid localizer")

    def test_guest_arrival_tc5(self):
        """Invalid test case. The IDCard is incorrect. Returns the exception message"""

        # Initial deletion of the file reservations.json to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")

        # Room reservation
        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        # Input data for the guest arrival. Incorrect IDCard but correct localizer
        input_data = {
            "Localizer": value,
            "IdCard": " "
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        room_key = my_reservation.guestArrival("input_data.json")
        self.assertEqual(room_key, "Reservation not found")

    def test_guest_arrival_tc6(self):
        """Invalid test case. The JSON file cannot be found. Returns the exception message"""

        # Initial deletion of the file input_data.json to avoid unexpected errors
        if os.path.exists("input_data.json"):
            os.remove("input_data.json")

        try:
            hotel_stay = HotelManager()
            hotel_stay.guestArrival("input_data.json")
            self.assertEqual(1, 0) # This line should not be executed if the test is correct.
        except HotelManagementException as e:
            self.assertEqual(str(e), "File does not exist")

    def test_guest_arrival_tc7(self):
        """Invalid test case. Keys are not found in the JSON file. Returns the exception message"""

        input_data = {
            "localizer": "5f07422a1f017951169d1b21b745e6a1",
            "idcard": "02166140T"
        }
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        try:
            hotel_stay = HotelManager()
            hotel_stay.guestArrival("input_data.json")
            self.assertEqual(1, 0)  # This line should not be executed if the test is correct.
        except HotelManagementException as e:
            self.assertEqual(str(e), "JSON structure is not valid")

    def test_guest_arrival_tc8(self):
        """Invalid test case. Incorrect arrival date. Returns the exception message"""

        # Initial deletion of the file reservations.json to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")

        # Room reservation
        my_reservation = HotelManager()
        my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")
        # Input data for the guest arrival
        input_data = {
            "Localizer": "5f07422a1f017951169d1b21b745e6a1",
            "IdCard": "02166140T"
        }

        # Save the input data in a JSON file
        with open("input_data.json", "w", encoding="utf-8") as file:
            json.dump(input_data, file)

        room_key = my_reservation.guestArrival("input_data.json")
        self.assertEqual(room_key, "Arrival date does not match expected arrival date")
