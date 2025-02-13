import re
import json
from datetime import datetime
from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH


class JsonStore:
    _data_list = []
    _file_name = ""

    def __init__(self):
        pass

    def write_data_into_json(self):
        # Write the data to the file
        # List --> file
        try:
            with open(self._file_name, "w", encoding="utf-8", newline="") as file:
                json.dump(self._data_list, file, indent=2)
        except FileNotFoundError as exception:
            raise HotelManagementException("Wrong file  or file path") from exception

    def load_json_into_list(self, checkin=False):
        # Read the data from the file if it exists. If not, create an empty list
        # File --> list
        try:
            with open(self._file_name, "r", encoding="utf-8", newline="") as file:
                self._data_list = json.load(file)
        except FileNotFoundError as ex:
            if checkin:
                raise HotelManagementException("Error: store checkin not found") from ex
            self._data_list = []
        except json.JSONDecodeError as exception:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from exception
        return self._data_list

    def add_item(self, item):
        self._data_list.append(item.__dict__)
        self.write_data_into_json()

    def find_item(self, key, value):
        self.load_json_into_list()
        for item in self._data_list:
            if item[key] == value:
                return item
        return None
