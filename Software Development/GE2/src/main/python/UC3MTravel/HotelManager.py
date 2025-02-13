"""This file contains the HotelManager class. This class is used to manage the hotel reservations."""
import json
import re
import os
import datetime
from datetime import datetime
# pip install spanish_dni needed
from spanish_dni.exceptions import NotValidDNIException
from spanish_dni.validator import validate_dni
from .HotelManagementException import HotelManagementException
from .HotelReservation import HotelReservation
from .HotelStay import HotelStay


class HotelManager:
    """This class is used to manage the hotel reservations."""

    def __init__(self):
        self.reservations_file = "reservations.json"
        self.stays_file = "stays.json"
        self.checkouts_file = "checkouts.json"

    def validateId(self, idnum):
        """This method validates the ID card number using the spanish_dni library."""
        valid = True
        try:
            validate_dni(idnum)
        except NotValidDNIException:
            valid = False
        return valid

    def validatePhoneNumber(self, num):
        """This method validates the phone number. It checks that the number has 9 digits, and if it's a number."""
        if len(str(num)) == 9:
            try:
                int(num)
            except ValueError:
                return False
            return True
        return False

    def validateRoomType(self, rtype):
        """This method validates the room type. It checks that the room type is single, double or suite."""
        if rtype in ["single", "double", "suite"]:
            return True
        return False

    def validateDays(self, days):
        """This method validates the number of days. It checks that the number of days is between 1 and 10."""
        try:
            days = int(days)
        except ValueError:
            return False
        if 0 < days <= 10:
            return True
        return False

    def validateName(self, name):
        """This method validates the name. It checks that the
        name has at least 10 characters and at most 50 characters."""
        if not isinstance(name, str):
            return False
        name_pattern = r"^(?=.{10,50}$)[A-Za-z]+(?:\s[A-Za-z]+)+"
        if re.fullmatch(name_pattern, name):
            return True
        return False

    def validateArrival(self, arrival):
        """This method validates the arrival date. It checks that the date is in the format dd/mm/yyyy."""
        # use date time to validate
        try:
            datetime.strptime(arrival, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    def validateCreditCard(self, x):
        """This method validates the credit card number using the Luhn algorithm.
        It checks that the number has 16 digits. If the number is valid, it returns True, otherwise False."""
        # Assuming x is the credit card number:
        credit_number = str(x)
        # Check that length of the credit card number is 16, x being an integer
        if len(credit_number) != 16:
            return False

        # Calculations
        total = 0
        i = 0
        while i < 16:
            if i % 2 == 0:
                total += int(credit_number[i])
            else:
                new_digit = 2 * int(credit_number[i])
                if len(str(new_digit)) < 2:
                    total += new_digit
                else:
                    total += int(str(new_digit)[0]) + int(str(new_digit)[1])
                # total += 2 * int(credit_number[i])
            i += 1
        # Now, i == 16 and total contains the number we needed for the algorithm.
        check = 10 - (total % 10)
        # check = 10 - (56 % 10)
        if check == int(credit_number[i - 1]):
            return True
        return False

    def readDataFromJson(self, fi):
        """This method reads the data from a JSON file and returns a HotelReservation object."""
        try:
            with open(fi, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError as e:
            raise HotelManagementException("Wrong file or file path") from e
        except json.JSONDecodeError as e:
            raise HotelManagementException("JSON Decode Error - Wrong JSON Format") from e

        try:
            c = data["CreditCard"]
            p = data["phoneNumber"]
            req = HotelReservation(idcard="12345678Z", creditcard_numb=c, name_surname="John Doe", phone_number=p,
                                   room_type="single", num_days=3, arrival="01/01/2022")
        except KeyError as e:
            raise HotelManagementException("JSON Decode Error - Invalid JSON Key") from e
        if not self.validateCreditCard(c):
            raise HotelManagementException("Invalid credit card number")

        # Close the file
        return req

    def roomReservation(self, idcard, creditcard, name, phonenum, arrival, rtype, days):
        """This method is used to make a reservation in the hotel.
           It first validates all the parameters and then creates a HotelReservation object."""
        # validate all parameters
        if not self.validatePhoneNumber(phonenum):
            hme_num = HotelManagementException("Invalid phone number")
            return hme_num.message
        if not self.validateRoomType(rtype):
            hme_room = HotelManagementException("Invalid room type")
            return hme_room.message
        if not self.validateDays(days):
            hme_days = HotelManagementException("Invalid number of days")
            return hme_days.message
        if not self.validateName(name):
            hme_name = HotelManagementException("Invalid name")
            return hme_name.message
        if not self.validateArrival(arrival):
            hme_arrival = HotelManagementException("Invalid arrival date")
            return hme_arrival.message
        if not self.validateCreditCard(creditcard):
            hme_credit = HotelManagementException("Invalid credit card number")
            return hme_credit.message
        if not self.validateId(idcard):
            hme_id = HotelManagementException("Invalid ID card number")
            return hme_id.message

        new_reservation = HotelReservation(idcard, creditcard, name, phonenum, arrival, rtype, days)
        reservation_data = new_reservation.bookingData()

        # Now add the reservation to the database, the method will return the localizer of the reservation
        return self.saveDataInFile(reservation_data, self.reservations_file)

    def saveDataInFile(self, reservation_data, file):
        """This method saves the information in the corresponding database.
           It first reads the data from the JSON file and then appends the new data.
           If the file does not exist, it creates a new one."""

        if not os.path.exists(file):
            # If file does not exist, create it.
            with open(file, "w", encoding="utf-8") as archivo:
                json.dump([reservation_data], archivo, indent=4)
            return reservation_data["localizer"]
        # If file exists, read the data and append the new reservation.
        with open(file, "r", encoding="utf-8") as archivo:
            existing_data = json.load(archivo)
        # Check if the ID card already has a reservation
        for reservation in existing_data:
            if reservation_data["idcard"] in reservation["idcard"]:
                return HotelManagementException("This ID card already has a reservation").message
        # If not, add the new reservation
        existing_data.append(reservation_data)
        # Save the updated data in the file.
        with open(file, "w", encoding="utf-8") as archivo:
            json.dump(existing_data, archivo, indent=4)
        # Return the localizer
        return reservation_data["localizer"]

    def guestArrival(self, input_file):
        """This method is used to check in a guest in the hotel.
        It reads the data from a JSON file, checks if there is a reservation matching that data
        and returns a room key after adding to the stays file."""
        # Open input file and get data inside
        if not os.path.exists(input_file):
            raise HotelManagementException("File does not exist")
        with open(input_file, 'r', encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                return HotelManagementException("Invalid JSON format").message
        if not data:
            return HotelManagementException("Cannot open file").message

        # Ensure that data is a dictionary
        if not isinstance(data, dict):
            return HotelManagementException("JSON structure is not valid").message

        # Check if the structure is valid
        expected_keys = ['Localizer', 'IdCard']
        if not all(key in data for key in expected_keys):
            raise HotelManagementException("JSON structure is not valid")

        # Get information from the JSON file and copy it
        localizer = data.get('Localizer', None)
        idcard = data.get('IdCard', None)

        # Return exception if data is not found
        if localizer is None or idcard is None:
            raise HotelManagementException("Data not found")

        # Verify the data in the reservation file
        reservation_file = self.reservations_file
        reservation_found = False
        with open(reservation_file, "r", encoding="utf-8") as file:
            reservations = json.load(file)
        for reservation in reservations:
            # Check if the reservation exists. This way we avoid reading the whole file if we find the idcard.
            if reservation["idcard"] == idcard:
                if reservation["localizer"] == localizer:
                    reservation_found = True
                    found_reservation = reservation
                    break
                return HotelManagementException("Invalid localizer").message

        if not reservation_found:
            return HotelManagementException("Reservation not found").message

        arrival_date = datetime.strptime(found_reservation['arrival_date'], "%d/%m/%Y")
        num_days = int(found_reservation['num_days'])
        room_type = found_reservation['room_type']

        # Check if arrival date matches expected arrival date. No further check is done since the data is already
        # validated in the reservation process and all data is extracted from the reservation file.
        current_arrival_date = datetime.utcnow()
        if arrival_date != current_arrival_date:
            return HotelManagementException("Arrival date does not match expected arrival date").message

        # Create HotelStay object as requested
        client_stay = HotelStay(idcard=idcard, localizer=localizer, num_days=num_days, room_type=room_type)

        # Get hash (SHA256) for the room_key
        room_key = client_stay.generateRoomKey()

        # Store stay in stays file
        stays_file = self.stays_file
        stay_info = {
            "localizer": client_stay.localizer,
            "idcard": client_stay.idcard,
            "arrival": client_stay.arrival.strftime("%d/%m/%Y"),
            "departure": (client_stay.departure.strftime("%d/%m/%Y")),
            "room_key": room_key
        }

        # Save the data in the stays file. If the data is not saved properly, return an error message.
        if self.saveDataInFile(stay_info, stays_file) != client_stay.localizer:
            return HotelManagementException("Error saving data").message

        # Return room_key
        return room_key

    def guestCheckOut(self, room_key):
        """This method is used to check out a guest from the hotel. It receives a room key and returns True if the
        guest has checked out successfully. It raises an exception if the room key is not valid or if the departure
        date is not today."""
        # Validate the input data
        if not isinstance(room_key, str) or len(room_key) != 64:
            raise HotelManagementException("Invalid room key format")

        # Search the check-ins (stays) store file for the room key
        found = False
        stays_file = self.stays_file

        # Open file
        try:
            with open(stays_file, "r", encoding="utf-8") as file:
                stays = json.load(file)

                # Search for the guest in the stays file using the room key
                for stay in stays:
                    if stay["room_key"] == room_key:
                        found = True
                        departure_date = datetime.strptime(stay["departure"], "%d/%m/%Y")
                        break

        # If there is no stays file
        except FileNotFoundError as e:
            raise HotelManagementException("Stays file does not exist") from e

        # If the key is not found, raise an exception
        if not found:
            raise HotelManagementException("Invalid room key")

        # If the key exists, verify that the departure date is today
        if departure_date.date() != datetime.utcnow().date():
            raise HotelManagementException("Departure date does not match today's date")

        # If the above is correct, save the data in the checkouts file
        checkout_data = {"departure_date": departure_date.strftime("%d/%m/%Y"), "room_key": room_key}
        return self.saveCheckOutInFile(checkout_data)

    def saveCheckOutInFile(self, checkout_data):
        """This method saves the checkout information in the checkouts file. It first reads the data from the JSON file
        and then appends the new data. If the file does not exist, it creates a new one."""
        file = self.checkouts_file
        if not os.path.exists(file):
            # If file does not exist, create it.
            with open(file, "w", encoding="utf-8") as archivo:
                json.dump([checkout_data], archivo, indent=4)
            return True
        # If file exists, read the data and append the new checkout.
        with open(file, "r", encoding="utf-8") as archivo:
            existing_data = json.load(archivo)
        # Check if the room key has already checked out.
        for checkout in existing_data:
            if checkout["room_key"] == checkout_data["room_key"]:
                return HotelManagementException("This room key has already checked out").message
        existing_data.append(checkout_data)
        # Save the updated data in the file.
        with open(file, "w", encoding="utf-8") as archivo:
            json.dump(existing_data, archivo, indent=4)
        # Return True if the data is saved.
        return True
