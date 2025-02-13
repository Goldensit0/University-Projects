"""Module for the hotel manager"""
import re
import json
from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_reservation import HotelReservation
from uc3m_travel.hotel_stay import HotelStay
from storage.reservation_json_store import ReservationStore
from storage.checkin_json_store import CheckinStore
from storage.checkout_json_store import CheckoutStore
from inputfiles.input_file import InputFile


class HotelManager:
    """Class with all the methods for managing reservations and stays"""

    class __HotelManager:
        def __init__(self):
            pass

        def validatecreditcard(self, credit_card):
            """validates the credit card number using luhn altorithm"""
            # taken from
            # https://allwin-raju-12.medium.com/
            # credit-card-number-validation-using-luhns-algorithm-in-python-c0ed2fac6234
            # PLEASE INCLUDE HERE THE CODE FOR VALIDATING THE GUID
            # RETURN TRUE IF THE GUID IS RIGHT, OR FALSE IN OTHER CASE

            myregex = re.compile(r"^[0-9]{16}")
            regex_matches = myregex.fullmatch(credit_card)
            if not regex_matches:
                raise HotelManagementException("Invalid credit card format")

            def digits_of(input_string):
                return [int(digit) for digit in str(input_string)]

            digits = digits_of(credit_card)
            odd_digits = digits[-1::-2]
            even_digits = digits[-2::-2]
            checksum = 0
            checksum += sum(odd_digits)
            for digit in even_digits:
                checksum += sum(digits_of(digit * 2))
            if not checksum % 10 == 0:
                raise HotelManagementException("Invalid credit card number (not luhn)")
            return credit_card

        def validate_room_type(self, room_type):
            """validates the room type value using regex"""
            myregex = re.compile(r"(SINGLE|DOUBLE|SUITE)")
            regex_matches = myregex.fullmatch(room_type)
            if not regex_matches:
                raise HotelManagementException("Invalid roomtype value")
            return room_type

        def validate_arrival_date(self, arrival_date):
            """validates the arrival date format  using regex"""
            myregex = re.compile(r"^(([0-2]\d|-3[0-1])\/(0\d|1[0-2])\/\d\d\d\d)$")
            regex_matches = myregex.fullmatch(arrival_date)
            if not regex_matches:
                raise HotelManagementException("Invalid date format")
            return arrival_date

        def validate_phonenumber(self, phone_number):
            """validates the phone number format  using regex"""
            myregex = re.compile(r"^(\+)[0-9]{9}")
            regex_matches = myregex.fullmatch(phone_number)
            if not regex_matches:
                raise HotelManagementException("Invalid phone number format")
            return phone_number

        def validate_numdays(self, num_days):
            """validates the number of days"""
            try:
                days = int(num_days)
            except ValueError as exception:
                raise HotelManagementException("Invalid num_days datatype") from exception
            if days < 1 or days > 10:
                raise HotelManagementException("Numdays should be in the range 1-10")
            return num_days

        @staticmethod
        def validate_dni(dni):
            """RETURN TRUE IF THE DNI IS RIGHT, OR FALSE IN OTHER CASE"""
            correct_values = {"0": "T", "1": "R", "2": "W", "3": "A", "4": "G", "5": "M",
                              "6": "Y", "7": "F", "8": "P", "9": "D", "10": "X", "11": "B",
                              "12": "N", "13": "J", "14": "Z", "15": "S", "16": "Q", "17": "V",
                              "18": "H", "19": "L", "20": "C", "21": "K", "22": "E"}
            dni_number = int(dni[0:8])
            key = str(dni_number % 23)
            return dni[8] == correct_values[key]

        def validate_localizer(self, localizer):
            """validates the localizer format using a regex"""
            regex_format = r'^[a-fA-F0-9]{32}$'
            myregex = re.compile(regex_format)
            if not myregex.fullmatch(localizer):
                raise HotelManagementException("Invalid localizer")
            return localizer

        def validate_roomkey(self, room_key):
            """validates the roomkey format using a regex"""
            regex_format = r'^[a-fA-F0-9]{64}$'
            myregex = re.compile(regex_format)
            if not myregex.fullmatch(room_key):
                raise HotelManagementException("Invalid room key format")
            return room_key

        def read_data_from_json(self, file_name):
            """reads the content of a json file with two fields: CreditCard and phoneNumber"""
            try:
                with open(file_name, encoding='utf-8') as file:
                    json_data = json.load(file)
            except FileNotFoundError as exception:
                raise HotelManagementException("Wrong file or file path") from exception
            except json.JSONDecodeError as exception:
                raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
            try:
                credit_card = json_data["CreditCard"]
                phone_number = json_data["phoneNumber"]
                reservation = HotelReservation(id_card="12345678Z",
                                               credit_card_number=credit_card,
                                               name_surname="John Doe",
                                               phone_number=phone_number,
                                               room_type="single",
                                               num_days=3,
                                               arrival="20/01/2024")
            except KeyError as exception:
                raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from exception
            if not self.validatecreditcard(credit_card):
                raise HotelManagementException("Invalid credit card number")
            # Close the file
            return reservation

        # pylint: disable=too-many-arguments
        def room_reservation(self,
                             credit_card: str,
                             name_surname: str,
                             id_card: str,
                             phone_number: str,
                             room_type: str,
                             arrival_date: str,
                             num_days: int) -> str:
            """manges the hotel reservation: creates a reservation and saves it into a json file"""

            # Validate dni
            regex_format = r'^[0-9]{8}[A-Z]{1}$'
            my_regex = re.compile(regex_format)
            if not my_regex.fullmatch(id_card):
                raise HotelManagementException("Invalid IdCard format")
            if not self.validate_dni(id_card):
                raise HotelManagementException("Invalid IdCard letter")

            # Validate room type
            room_type = self.validate_room_type(room_type)

            # Validate full name
            regex_format = r"^(?=^.{10,50}$)([a-zA-Z]+(\s[a-zA-Z]+)+)$"
            myregex = re.compile(regex_format)
            regex_matches = myregex.fullmatch(name_surname)
            if not regex_matches:
                raise HotelManagementException("Invalid name format")

            # Validate credit card
            credit_card = self.validatecreditcard(credit_card)

            # Validate arrival date
            arrival_date = self.validate_arrival_date(arrival_date)

            # Validate number of days
            num_days = self.validate_numdays(num_days)

            # Validate phone number
            phone_number = self.validate_phonenumber(phone_number)

            # If all is correct, create the reservation
            my_reservation = HotelReservation(id_card=id_card,
                                              credit_card_number=credit_card,
                                              name_surname=name_surname,
                                              phone_number=phone_number,
                                              room_type=room_type,
                                              arrival=arrival_date,
                                              num_days=num_days)

            # Store the reservation in the json file
            reservation_store = ReservationStore()
            reservation_store.add_reservation(my_reservation)

            return my_reservation.localizer

        def guest_arrival(self, file_input: str) -> str:
            """manages the arrival of a guest with a reservation"""
            input_file = InputFile()
            input_list = input_file.list_from_file(file_input)

            # Check values in the input list
            try:
                my_localizer = input_list["Localizer"]
                my_id_card = input_list["IdCard"]
            except KeyError as e:
                raise HotelManagementException("Error - Invalid Key in JSON") from e

            # Validate dni
            regex_format = r'^[0-9]{8}[A-Z]{1}$'
            my_regex = re.compile(regex_format)
            if not my_regex.fullmatch(my_id_card):
                raise HotelManagementException("Invalid IdCard format")
            if not self.validate_dni(my_id_card):
                raise HotelManagementException("Invalid IdCard letter")

            # Validate localizer
            self.validate_localizer(my_localizer)

            # Create HotelStay object and get the localizer
            my_checkin = HotelStay(idcard=my_id_card, localizer=my_localizer)

            # Store check in
            checkin_store = CheckinStore()
            checkin_store.store_check_in(my_checkin)

            return my_checkin.room_key

        def guest_checkout(self, room_key: str) -> bool:
            """manages the checkout of a guest"""

            # Validate room key
            self.validate_roomkey(room_key)

            checkin_store = CheckinStore()

            # Get the list of room keys
            room_key_list = checkin_store.load_json_into_list(checkin=True)

            # Check if the room key is registered and the get the departure date
            found = False
            for item in room_key_list:
                if room_key == item["_HotelStay__room_key"]:
                    departure_date_timestamp = item["_HotelStay__departure"]
                    found = True
                    # Check if today's date coincides with the departure date
                    today = datetime.utcnow().date()
                    if datetime.fromtimestamp(departure_date_timestamp).date() != today:
                        raise HotelManagementException("Error: today is not the departure day")
            if not found:
                raise HotelManagementException("Error: room key not found")

            checkout_store = CheckoutStore()
            checkout_store.store_room_key(room_key)

            return True

    instance = None

    def __new__(cls):
        if not HotelManager.instance:
            HotelManager.instance = HotelManager.__HotelManager()
        return HotelManager.instance

    def __getattr__(self, existing):
        return getattr(self.instance, existing)

    def __setattr__(self, existing, valor):
        return setattr(self.instance, existing, valor)
