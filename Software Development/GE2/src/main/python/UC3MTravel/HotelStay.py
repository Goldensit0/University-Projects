""" Class HotelStay (GE2.2) """
from datetime import datetime, timedelta
import hashlib


class HotelStay:
    """This class is used to create a hotel stay object."""
    def __init__(self, idcard, localizer, num_days, room_type, room_key=None):
        self.__alg = "SHA-256"
        self.__type = room_type
        self.__localizer = localizer
        self.__idcard = idcard
        justnow = datetime.utcnow()
        self.__arrival = justnow
        # timestamp is represented in seconds.milliseconds
        # to add the number of days we must express num_days in seconds
        self.__departure = self.__arrival + timedelta(days=int(num_days))
        self.__room_key = room_key

    def __signatureString(self):
        """Composes the string to be used for generating the key for the room"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",localizer:" + \
            self.__localizer + ",arrival:" + self.__arrival + \
            ",departure:" + self.__departure + "}"

    @property
    def idcard(self):
        """Property that represents the product_id of the guest"""
        return self.__idcard

    @idcard.setter
    def idcard(self, value):
        """Sets the product_id of the guest"""
        self.__idcard = value

    @property
    def localizer(self):
        """Property that represents the order_id"""
        return self.__localizer

    @localizer.setter
    def localizer(self, value):
        """Sets the order_id of the guest"""
        self.__localizer = value

    @property
    def arrival(self):
        """Property that represents the phone number of the client"""
        return self.__arrival

    @property
    def room_key(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signatureString().encode()).hexdigest()

    @property
    def departure(self):
        """Returns the issued at value"""
        return self.__departure

    @departure.setter
    def departure(self, value):
        """Sets the departure date of the guest"""
        self.__departure = value

    def generateRoomKey(self):
        """This method generates an SHA-256 key for the room."""
        text = (f"{{alg:{self.__alg}, typ:{self.__type}, localizer:{self.__localizer},"
                f"arrival:{self.__arrival},departure:{self.__departure}}}")

        self.__room_key = hashlib.sha256(text.encode()).hexdigest()
        return self.__room_key
