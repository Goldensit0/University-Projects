from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from storage.json_store import JsonStore
from datetime import datetime


class CheckoutStore(JsonStore):
    _file_name = JSON_FILES_PATH + "store_check_out.json"

    def store_room_key(self, room_key):

        # Get the list of room keys
        room_key_list = self.load_json_into_list()

        # Check if the room key is already in the list
        for checkout in room_key_list:
            if checkout["room_key"] == room_key:
                raise HotelManagementException("Guest is already out")

        # If no, add the room key to the list
        room_checkout = {"room_key": room_key, "checkout_time": datetime.timestamp(datetime.utcnow())}
        room_key_list.append(room_checkout)

        # Write the data to the file
        self.write_data_into_json()
