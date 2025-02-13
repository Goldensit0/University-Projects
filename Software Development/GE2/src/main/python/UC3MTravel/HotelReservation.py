"""This module contains the HotelReservation class."""
import hashlib


class HotelReservation:
    """This class represents a hotel reservation"""
    def __init__(self, idcard, creditcard_numb, name_surname, phone_number, arrival, room_type, num_days):
        self.__credit_card_number = creditcard_numb
        self.__idcard = idcard
        self.__arrival = arrival
        self.__name_surname = name_surname
        self.__phone_number = phone_number
        self.__room_type = room_type
        self.__num_days = num_days

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        # VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"idcard": self.__idcard,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()

    @property
    def credit_card(self):
        """Returns the credit card number"""
        return self.__credit_card_number

    @credit_card.setter
    def credit_card(self, value):
        """Sets the credit card number"""
        self.__credit_card_number = value

    @property
    def idcard(self):
        """Returns the id card"""
        return self.__idcard

    @idcard.setter
    def idcard(self, value):
        """Sets the id card"""
        self.__idcard = value

    @property
    def localizer(self):
        """Returns the md5 signature"""
        return hashlib.md5(str(self).encode()).hexdigest()

    def bookingData(self):
        """Returns the booking data in a dict format"""
        json_info = {"idcard": self.__idcard,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     "localizer": self.localizer
                     }
        return json_info
