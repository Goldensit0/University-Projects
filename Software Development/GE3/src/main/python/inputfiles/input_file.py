import json
from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH


class InputFile:
    def __init__(self):
        pass

    def list_from_file(self, file_name, checkin=False):
        # Read the data from the file if it exists. If not, create an empty list
        # File --> list
        try:
            with open(file_name, "r", encoding="utf-8", newline="") as file:
                data_list = json.load(file)
        except FileNotFoundError as ex:
            if checkin:
                raise HotelManagementException("Error: store checkin not found") from ex
            data_list = []
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return data_list
