from uc3m_travel.hotel_management_exception import HotelManagementException
from uc3m_travel.hotel_management_config import JSON_FILES_PATH
from storage.json_store import JsonStore


class ReservationStore(JsonStore):
    _file_name = JSON_FILES_PATH + "store_reservation.json"

    def add_reservation(self, reservation_data):
        reservation_found = self.find_item("_HotelReservation__localizer", reservation_data.localizer)
        id_found = self.find_item("_HotelReservation__id_card", reservation_data.id_card)
        if reservation_found:
            raise HotelManagementException("Reservation already exists")
        if id_found:
            raise HotelManagementException("This ID card has another reservation")
        super().add_item(reservation_data)
