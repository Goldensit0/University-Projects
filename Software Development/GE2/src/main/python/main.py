"""THIS MAIN PROGRAM IS ONLY VALID FOR THE FIRST THREE WEEKS OF CLASS
IN GUIDED EXERCISE 2.2, TESTING MUST BE PERFORMED USING UNITTESTS."""

import UC3MTravel.HotelManager


def main():
    """Main function to test the HotelManager class. Only valid for the first three weeks of class."""
    mng = UC3MTravel.HotelManager.HotelManager()
    res = mng.readDataFromJson("test.json")
    str_res = res
    print(str_res)
    print("CreditCard: " + res.credit_card)
    print(res.localizer)


if __name__ == "__main__":
    main()
