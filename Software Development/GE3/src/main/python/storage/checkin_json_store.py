from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from storage.json_store import JsonStore


class CheckinStore(JsonStore):
    _file_name = JSON_FILES_PATH + "store_check_in.json"

    def store_check_in(self, my_checkin):
        # Get the list of room keys
        self.load_json_into_list()

        # Check if the room key is already in the list
        checkin_found = self.find_item("_HotelStay__room_key", my_checkin.room_key)
        if checkin_found:
            raise HotelManagementException("checkin already realized")

        # If not, store check in
        super().add_item(my_checkin)
