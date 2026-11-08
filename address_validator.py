"""

Class to collects and validates customer's delivery address.
This is an example of how adress validation can be done.
Same class and methods can be used to validate adresses using complex API structures, etc.

"""


import re


class AddressValidator:
    

    def __init__(self):
        self.street_address = ""
        self.city = ""
        self.state = ""
        self.zip_code = ""

    def get_valid_zip(self):
        while True:
            zip_input = input("Please enter your 5-digit ZIP code: ").strip()

            if re.fullmatch(r"\d{5}", zip_input):
                return zip_input

            print(
                "Error: Invalid ZIP code. "
                "It must be exactly 5 digits. Try again.\n"
            )

    def get_non_blank_input(self, prompt):
        while True:
            value = input(prompt).strip()

            if value:
                return value

            print("Error: This field cannot be blank. Try again.\n")

    def collect_address(self):
        print("\n--- Address Collection ---")

        self.state = self.get_non_blank_input("Enter State: ")
        self.city = self.get_non_blank_input("Enter City: ")
        self.street_address = self.get_non_blank_input(
            "Enter your full street address: "
        )
        self.zip_code = self.get_valid_zip()

        print("\nSuccess! Address saved.")

        return self

    def formatted_address(self):
        return (
            f"{self.street_address}, "
            f"{self.city}, "
            f"{self.state} "
            f"{self.zip_code}"
        )
