"""
Stores ItemToPurchase objects and handles cart calculations

Updates on this version : 

Compatibility helpers:
Earlier milestones used different names for some cart operations.
These helpers keep existing calls working without duplicating logic:
- items exposes the same list as cart_items.
- get_num_items_in_cart() and get_total_quantity() delegate to get_num_items(), directly or through another helper.
- get_subtotal() delegates to get_cost_of_cart().

The required methods contain the calculations; the helpers provide
alternative names used by the existing menu and checkout code.

"""

from math import isfinite
from item_to_purchase import ItemToPurchase

class ShoppingCart:
    

    def __init__(self, customer_name, current_date):
        self.customer_name = customer_name
        self.current_date = current_date
        self.cart_items = []
        self.tax_rate = 0.08
        self.shipping_charge = 10.00

    def add_item(self, item):
        self.cart_items.append(item)

        print(
            f"\n{item.item_name}, "
            f"quantity {item.item_quantity}, "
            f"added to your cart."
        )
    
    def add_item_manually(self):
        """Collect the four item fields and add a new item to the cart."""
        print("\n===== ADD ITEM NOT IN CATALOGUE=====")
        print("Disclaimer - You're adding items which are not in our catalouge. Shipping is subject to availibility of the items.")

        name = input("Enter the item name: ").strip()
        while not name:
            name = input("Item name cannot be blank. Enter the item name: ").strip()

        description = input("Enter the item description: ").strip()

        while True:
            try:
                price = float(input("Enter the item price: "))
                if isfinite(price) and price >= 0:
                    break
            except ValueError:
                pass
            print("Enter a valid price of 0 or more.")

        quantity = self.read_unit_count(
        "Enter the item quantity (0 to cancel): "
        )
        if quantity is None:
            return

        item = ItemToPurchase(
            item_name=name,
            item_description=description,
            item_price=price,
            item_quantity=quantity,
            )
        self.add_item(item)
    

    def remove_item(self, item_name, *, selected_item=None):
        for index, item in enumerate(self.cart_items):
            if item.item_name == item_name and (
                selected_item is None or item is selected_item
            ):
                self.cart_items.pop(index)
                return True

        print("Item not found in cart. Nothing removed.")
        return False

    def modify_item(self, updated_item, *, selected_item=None):
        for item in self.cart_items:
            if item.item_name != updated_item.item_name:
                continue
            if selected_item is not None and item is not selected_item:
                continue

            if updated_item.item_description != "none":
                item.item_description = updated_item.item_description
            if updated_item.item_price != 0:
                item.item_price = updated_item.item_price
            if updated_item.item_quantity != 0:
                item.item_quantity = updated_item.item_quantity
            return

        print("Item not found in cart. Nothing modified.")
    

    def get_num_items(self):
        return sum(item.item_quantity for item in self.cart_items)

    def get_num_items_in_cart(self):
        # keep the earlier milestone method available
        return self.get_num_items()

    def get_cost_of_cart(self):
        #retaining earlier method available
        return sum(item.get_item_cost() for item in self.cart_items)

    def print_total(self):
        print(f"{self.customer_name}'s Shopping Cart - {self.current_date}")
        print(f"Number of Items: {self.get_num_items_in_cart()}\n")
        if not self.cart_items:
            print("SHOPPING CART IS EMPTY")
        else:
            for item in self.cart_items:
                item.print_item_cost()
        print(f"\nTotal: ${self.get_cost_of_cart():.2f}")

    def print_descriptions(self):
        print(f"\n{self.customer_name}'s Shopping Cart - {self.current_date}")
        if not self.items:
            print("SHOPPING CART IS EMPTY")
            return
        name_width = max(20, max(len(item.item_name) for item in self.items))
        header = (
            f"{'No.':<5}{'Item':<{name_width}}  "
            f"{'Unit Price':>12}{'Quantity':>10}{'Total':>14}"
        )
        print(header)
        print("-" * len(header))
        for number, item in enumerate(self.items, start=1):
            price = f"${item.item_price:.2f}"
            total = f"${item.get_item_cost():.2f}"
            print(
                f"{number:<5}{item.item_name:<{name_width}}  "
                f"{price:>12}{item.item_quantity:>10}{total:>14}"
            )
        print("-" * len(header))
        print(f"Total quantity: {self.get_total_quantity()}")
        print(f"Subtotal: ${self.get_subtotal():.2f}")
        for item in self.items:
            if item.item_description not in ("", "none", item.item_name):
                print(f"\n{item.item_name}: {item.item_description}")

    def choose_cart_item(self):
        # returns a selected row index, or None when cancelled
        self.print_descriptions()
        if not self.items:
            return None
        while True:
            try:
                number = int(input("\nChoose an item number (0 to cancel): "))
                if number == 0:
                    return None
                if 1 <= number <= len(self.items):
                    return number - 1
            except ValueError:
                pass
            print("Please enter a valid item number.")

    def read_unit_count(self, prompt, maximum=None):
        while True:
            try:
                quantity = int(input(prompt))
                if quantity == 0:
                    return None
                if quantity > 0 and (maximum is None or quantity <= maximum):
                    return quantity
            except ValueError:
                pass
            if maximum is None:
                print("Enter a positive whole number, or 0 to cancel.")
            else:
                print(f"Enter a quantity from 1 to {maximum}, or 0 to cancel.")

    def reduce_item_quantity(self, index, amount):
        item = self.items[index]
        if not 1 <= amount <= item.item_quantity:
            print("Invalid reduction quantity.")
            return
        if amount == item.item_quantity:
            if item.item_quantity == 1:
                print(
                    f"\nThere is only 1 {item.item_name} in your cart. "
                    "Reducing its quantity will remove it from the cart."
                )
            else:
                print(
                    f"\nThis will remove all {amount} units of "
                    f"{item.item_name} from your cart."
                )
            while True:
                choice = input("Continue? (y/n): ").strip().lower()
                if choice in ("y", "n"):
                    break
                print("Please enter y or n.")
            if choice == "n":
                print("Cancelled. Your cart is unchanged.")
                return
            if self.remove_item(item.item_name, selected_item=item):
                print(f"{item.item_name} removed from your cart.")
        else:
            updated_item = ItemToPurchase(
                item_name=item.item_name,
                item_quantity=item.item_quantity - amount,
                )
            self.modify_item(updated_item, selected_item=item)
            print(
                f"{amount} unit(s) removed. "
                f"{item.item_name}: {item.item_quantity} remaining."
                )

    def remove_item_interactive(self):
        index = self.choose_cart_item()
        if index is None:
            return

        item = self.items[index]

        if item.item_quantity == 1:
            self.reduce_item_quantity(index, 1)
            return

        amount = self.read_unit_count(
            f"How many units should be removed? (1–{item.item_quantity}, "
            "0 to cancel): ",
            maximum=item.item_quantity,
        )

        if amount is not None:
            self.reduce_item_quantity(index, amount)
    
    
    def change_quantity_interactive(self):
        index = self.choose_cart_item()
        if index is None:
            return
        item = self.items[index]
        while True:
            choice = input(
                "\n+ to increase quantity, - to reduce quantity, 0 to cancel: "
            ).strip()
            if choice in ("+", "-", "0"):
                break
            print("Please enter +, -, or 0.")
        if choice == "0":
            return
        if choice == "+":
            amount = self.read_unit_count(
                "How many units should be added? (0 to cancel): "
            )
            if amount is not None:
                    updated_item = ItemToPurchase(
                    item_name=item.item_name,
                    item_quantity=item.item_quantity + amount,
                    )
                    self.modify_item(updated_item, selected_item=item)
                    print(f"{item.item_name}: quantity updated to {item.item_quantity}.")
        elif item.item_quantity == 1:
            self.reduce_item_quantity(index, 1)
        else:
            amount = self.read_unit_count(
                f"How many units should be reduced? (1–{item.item_quantity}, "
                "0 to cancel): ", maximum=item.item_quantity,
            )
            if amount is not None:
                self.reduce_item_quantity(index, amount)

    # compatibiility helpers for the earlier catalogue/checkout workflow.
    @property
    def items(self):
        return self.cart_items

    def get_total_quantity(self):
        return self.get_num_items_in_cart()

    def get_subtotal(self):
        return self.get_cost_of_cart()

    def get_tax(self):
        return self.get_subtotal() * self.tax_rate

    def get_grand_total(self):
        return (
            self.get_subtotal()
            + self.get_tax()
            + self.shipping_charge
        )

    def print_cart(self):
        print("\n===== YOUR SHOPPING CART =====")
        print(f"Customer: {self.customer_name}")
        print(f"Date: {self.current_date}")

        if len(self.cart_items) == 0:
            print("SHOPPING CART IS EMPTY")
            return

        for item in self.cart_items:
            item.print_item_cost()

        print("\n-----------------------------")
        print(
            f"Total Items      : {self.get_total_quantity()}"
        )
        print(
            f"Subtotal         : ${self.get_subtotal():.2f}"
        )
        print(
            f"Tax              : ${self.get_tax():.2f}"
        )
        print(
            f"Shipping         : ${self.shipping_charge:.2f}"
        )
        print("-----------------------------")
        print(
            f"TOTAL            : ${self.get_grand_total():.2f}"
        )

    def confirm_checkout(self):
        if len(self.cart_items) == 0:
            return False

        while True:
            choice = input(
                "\nPress 1 to proceed to checkout "
                "or 0 to return to main menu: "
            ).strip()

            if choice == "1":
                return True

            if choice == "0":
                return False

            print("Invalid input. Please enter 1 or 0.")
