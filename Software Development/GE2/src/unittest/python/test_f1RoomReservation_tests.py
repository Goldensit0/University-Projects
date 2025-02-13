"""Unittests for the room_reservation method in the HotelManager class"""

import os
import json
from unittest import TestCase
from UC3MTravel.HotelManager import HotelManager

class TestRoomReservation(TestCase):
    """Contains all the tests for the room_reservation method"""

    def test_room_reservation_tc1(self):
        """Valid test case. All the parameters are correct. No files exist. Returns the localizer"""

        # Initial deletion of the file reservations.json to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("5f07422a1f017951169d1b21b745e6a1", value)

    def test_room_reservation_tc2(self):
        """Valid test case. All the parameters are correct. The file reservations.json already exists, empty.
        Returns the localizer"""

        # Delete and create the file reservations.json
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")
        with open("reservations.json", "w", encoding="utf-8") as file:
            json.dump([], file)

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("5f07422a1f017951169d1b21b745e6a1", value)

    def test_room_reservation_tc3(self):
        """Valid test case. All the parameters are correct. The file reservations.json already exists, with data.
        Returns the localizer"""

        # Initial deletion of the file reservations.json to avoid unexpected errors
        if os.path.exists("reservations.json"):
            os.remove("reservations.json")

        my_reservation = HotelManager()
        my_reservation.roomReservation("26867719Q", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")
        my_reservation.roomReservation("61253812M", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("5f07422a1f017951169d1b21b745e6a1", value)

    def test_room_reservation_tc4(self):
        """Invalid test case. The phone number is incorrect (too short). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "66666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid phone number", value)

    def test_room_reservation_tc5(self):
        """Invalid test case. The room type is incorrect. Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "singular", "4")

        self.assertEqual("Invalid room type", value)

    def test_room_reservation_tc6(self):
        """Invalid test case. The number of days is incorrect (lower nonvalid boundary value).
        Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "0")

        self.assertEqual("Invalid number of days", value)

    def test_room_reservation_tc7(self):
        """Invalid test case. The number of days is incorrect (upper nonvalid boundary value).
        Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "11")

        self.assertEqual("Invalid number of days", value)

    def test_room_reservation_tc8(self):
        """Invalid test case. The name is incorrect (name too short). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose luis",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid name", value)

    def test_room_reservation_tc9(self):
        """Invalid test case. The name is incorrect (name too long). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111",
                                                "joseeeeeeeeeeeeeeeeeeee luuuuuiiiiiiissss lopeeeeez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid name", value)

    def test_room_reservation_tc10(self):
        """Invalid test case. The name is incorrect (nonvalid character). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111",
                                                "jose luis pacheño",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid name", value)

    def test_room_reservation_tc11(self):
        """Invalid test case. The arrival date is incorrect (incorrect format,
        uses - instead of /). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01-06-2023", "suite", "4")

        self.assertEqual("Invalid arrival date", value)

    def test_room_reservation_tc12(self):
        """Invalid test case. The arrival date is incorrect (incorrect format, m/d/y). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "06/20/2023", "suite", "4")

        self.assertEqual("Invalid arrival date", value)

    def test_room_reservation_tc13(self):
        """Invalid test case. The arrival date is incorrect (incorrect value, day higher than possible).
        Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "32/05/2023", "suite", "4")

        self.assertEqual("Invalid arrival date", value)

    def test_room_reservation_tc14(self):
        """Invalid test case. The card number is incorrect (incorrect length). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "653213345278911", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid credit card number", value)

    def test_room_reservation_tc15(self):
        """Invalid test case. The card number is incorrect (does not follow the Luhn algorithm)."""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789112", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid credit card number", value)

    def test_room_reservation_tc16(self):
        """Invalid test case. The id is incorrect (incorrect format). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid ID card number", value)

    def test_room_reservation_tc17(self):
        """Invalid test case. The id is incorrect (incorrect letter). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140A", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid ID card number", value)

    def test_room_reservation_tc18(self):
        """Invalid test case. The id is incorrect (incorrect length). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("021661401T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid ID card number", value)

    def test_room_reservation_tc19(self):
        """Invalid test case. The id already exists in the database. Returns the exception message"""

        my_reservation = HotelManager()
        my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("This ID card already has a reservation", value)

    def test_room_reservation_tc20(self):
        """Invalid test case. The phone number is incorrect (too long). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "6666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid phone number", value)

    def test_room_reservation_tc21(self):
        """Invalid test case. The phone number is incorrect (not a number). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "6a7sbd721", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid phone number", value)

    def test_room_reservation_tc22(self):
        """Invalid test case. The number of days is incorrect (not a number). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "01/06/2023", "suite", "one")

        self.assertEqual("Invalid number of days", value)

    def test_room_reservation_tc23(self):
        """Invalid test case. The name is incorrect (only one name). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "joseluismanchego",
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid name", value)

    def test_room_reservation_tc24(self):
        """Invalid test case. The name is incorrect (not a string). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", 12345678910,
                                                "666666666", "01/06/2023", "suite", "4")

        self.assertEqual("Invalid name", value)

    def test_room_reservation_tc25(self):
        """Invalid test case. The date is incorrect (incorrect format, y/m/d). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "2023/06/22", "suite", "4")

        self.assertEqual("Invalid arrival date", value)

    def test_room_reservation_tc26(self):
        """Invalid test case. The date is incorrect (incorrect format, y/d/m). Returns the exception message"""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "2023/22/06", "suite", "4")

        self.assertEqual("Invalid arrival date", value)

    def test_room_reservation_tc27(self):
        """Invalid test case. The date is incorrect (incorrect value, month higher than possible)."""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "22/13/2023", "suite", "4")

        self.assertEqual("Invalid arrival date", value)

    def test_room_reservation_tc28(self):
        """Invalid test case. The date is incorrect (incorrect value, month lower than possible)."""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "22/00/2023", "suite", "4")

        self.assertEqual("Invalid arrival date", value)

    def test_room_reservation_tc29(self):
        """Invalid test case. The date is incorrect (incorrect value, day lower than possible)."""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "00/06/2023", "suite", "4")

        self.assertEqual("Invalid arrival date", value)

    def test_room_reservation_tc30(self):
        """Invalid test case. The date is incorrect (incorrect value, year lower than possible)."""

        my_reservation = HotelManager()
        value = my_reservation.roomReservation("02166140T", "6532133452789111", "jose lopez",
                                                "666666666", "22/06/0000", "suite", "4")

        self.assertEqual("Invalid arrival date", value)
