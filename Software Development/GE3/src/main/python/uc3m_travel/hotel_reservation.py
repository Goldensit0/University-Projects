"""Hotel reservation class"""
import hashlib
from datetime import datetime
from freezegun import freeze_time
from storage.reservation_json_store import ReservationStore
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.attributes.attribute_phone_number import PhoneNumber
from uc3m_travel.attributes.attribute_name_surname import NameSurname
from uc3m_travel.attributes.attribute_room_type import RoomType
from uc3m_travel.attributes.attribute_arrival import Arrival

class HotelReservation:
    """Class for representing hotel reservations"""

    # pylint: disable=too-many-arguments, too-many-instance-attributes
    def __init__(self,
                 id_card: str,
                 credit_card_number: str,
                 name_surname: str,
                 phone_number: str,
                 room_type: str,
                 arrival: str,
                 num_days: int):
        """constructor of reservation objects"""
        self.__credit_card_number = credit_card_number
        self.__id_card = id_card
        justnow = datetime.utcnow()
        self.__arrival = Arrival(arrival).value
        self.__reservation_date = datetime.timestamp(justnow)
        self.__name_surname = NameSurname(name_surname).value
        self.__phone_number = PhoneNumber(phone_number).value
        self.__room_type = RoomType(room_type).value
        self.__num_days = num_days
        self.__localizer = hashlib.md5(str(self).encode()).hexdigest()

    def __str__(self):
        """return a json string with the elements required to calculate the localizer"""
        # VERY IMPORTANT: JSON KEYS CANNOT BE RENAMED
        json_info = {"id_card": self.__id_card,
                     "name_surname": self.__name_surname,
                     "credit_card": self.__credit_card_number,
                     "phone_number:": self.__phone_number,
                     "reservation_date": self.__reservation_date,
                     "arrival_date": self.__arrival,
                     "num_days": self.__num_days,
                     "room_type": self.__room_type,
                     }
        return "HotelReservation:" + json_info.__str__()

    @property
    def credit_card(self):
        """property for getting and setting the credit_card number"""
        return self.__credit_card_number

    @credit_card.setter
    def credit_card(self, value):
        self.__credit_card_number = value

    @property
    def id_card(self):
        """property for getting and setting the id_card"""
        return self.__id_card

    @property
    def room_type(self):
        """property for getting and setting the room_type"""
        return self.__room_type

    @property
    def arrival(self):
        """property for getting and setting the arrival"""
        return self.__arrival

    @property
    def num_days(self):
        """property for getting and setting the num_days"""
        return self.__num_days

    @id_card.setter
    def id_card(self, value):
        self.__id_card = value

    @property
    def localizer(self):
        """Returns the md5 signature"""
        return self.__localizer

    @classmethod
    def load_reservation_from_localizer(cls, localizer: str):
        reservations = ReservationStore()
        reservation_data = reservations.find_item("_HotelReservation__localizer", localizer)

        if reservation_data:
            reservation_date = datetime.fromtimestamp(reservation_data["_HotelReservation__reservation_date"])
        else:
            raise HotelManagementException("Error: localizer not found")

        with freeze_time(reservation_date):
            new_reservation = cls(
                credit_card_number=reservation_data["_HotelReservation__credit_card_number"],
                id_card=reservation_data["_HotelReservation__id_card"],
                num_days=reservation_data["_HotelReservation__num_days"],
                room_type=reservation_data["_HotelReservation__room_type"],
                arrival=reservation_data["_HotelReservation__arrival"],
                name_surname=reservation_data["_HotelReservation__name_surname"],
                phone_number=reservation_data["_HotelReservation__phone_number"])
        if new_reservation.localizer != localizer:
            raise HotelManagementException("Error: reservation has been manipulated")

        return new_reservation
