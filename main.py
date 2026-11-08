"""
Final Project: Online Shopping Cart

Data source continue to the same from Kaggle - 
https://www.kaggle.com/datasets/marthadimgba/online-shop-2024?select=products.csv

Class responsibilities:
- ItemToPurchase: stores item details and calculates item cost.
- ProductCatalog: loads CSV data; handles browsing, search and selection.
- ShoppingCart: manages items, quantities, cart displays and order totals.
- AddressValidator: collects and validates delivery-address inputs.
- main.py: coordinates customer setup, menus and checkout.

Changes in this version:
- Added a four-option main menu: Browse Categories, Manage My Cart,Checkout and Quit.
- Added a date prompt to use today's date or enter a valid order date.
- Displayed the customer name and date immediately after cart creation.
- Added manual item entry alongside existing catalogue browsing.
- Added numbered cart selection, partial removal and quantity changes.
- Used remove_item() for confirmed removal of all remaining units.
- Passed a temporary ItemToPurchase object to modify_item() when changing quantities.
- Handled duplicate names by passing the selected cart object.
- Retained the cart table, checkout totals and compatibility aliases.


"""

from datetime import datetime
from pathlib import Path

from address_validator import AddressValidator
from product_catalog import ProductCatalog
from shopping_cart import ShoppingCart


def add_from_catalog(shopping_cart, catalog):
    """Return after adding an item or choosing Back to main menu."""
    while True:
        category = catalog.choose_category()
        if category is None:
            return

        item = catalog.choose_product(category)
        if item == "main":
            return
        if item is not None:
            shopping_cart.add_item(item)
            print(f"\n{shopping_cart.get_total_quantity()} items currently in cart.")
            return


def print_menu(shopping_cart, catalog=None):
    """Manage the existing cart; q returns to the main menu."""
    while True:
        print("\n===== MANAGE MY CART =====")
        print("a - Add Item")
        print("r - Remove Item")
        print("c - Change Item Quantity")
        print("i - Output Items' Descriptions")
        print("o - Output Shopping Cart (totals)")
        print("q - Quit managing cart and go back to main menu)")
        choice = input("\nChoose an option: ").strip().lower()

        if choice == "q":
            return
        elif choice == "a":
            print("\n1 - Enter item details manually")
            print("2 - Browse catalogue")
            print("0 - Back to Manage My Cart")
            
            add_choice = input("Choose an option: ").strip()

            if add_choice == "1":
                shopping_cart.add_item_manually()
            elif add_choice == "2":
                if catalog is None:
                    catalog = ProductCatalog(
                        Path(__file__).with_name("product_catalogue.csv")
                    )
                add_from_catalog(shopping_cart, catalog)
            elif add_choice != "0":
                print("Invalid option. Please enter 1, 2, or 0.")
        
        elif choice == "r":
            shopping_cart.remove_item_interactive()
        elif choice == "c":
            shopping_cart.change_quantity_interactive()
        elif choice == "i":
            shopping_cart.print_descriptions()
        elif choice == "o":
            shopping_cart.print_cart()
        else:
            print("Invalid option. Please enter a, r, c, i, o, or q.")


def checkout(cart, address, order_date):
    """Return True only when a non-empty order is confirmed."""
    if not cart.items:
        print("\nYour cart is empty. Add an item before checking out.")
        return False

    cart.print_cart()
    while True:
        choice = input(
            "\nProceed to checkout? (y/n; n returns to main menu): "
        ).strip().lower()
        if choice == "n":
            return False
        if choice == "y":
            break
        print("Please enter y or n.")

    print("\n===== CHECKOUT =====")
    print(f"\nOrder#          : {order_date}")
    print(f"To              : {cart.customer_name}")
    print(f"Shipping Address: {address.formatted_address()}")
    print(f"Order Total     : ${cart.get_grand_total():.2f}")
    print("\nProceeding to payment...")
    return True


def main():
    print("\n--------------------------------")
    print("***** ONLINE SHOPPING CART *****")
    print("--------------------------------")
    customer_name = input("\nPlease enter your name: ").strip()
    print(
        "\nPlease enter your delivery address."
        "\nPlease note - we are currently capable "
        "of delivering in the United States."
    )
    address = AddressValidator()
    address.collect_address()

    while True:
        date_choice = input(
            "Do you want to use today's date as the default (Y/N)? "
        ).strip().lower()

        if date_choice == "y":
            order_date = datetime.now()
            break
        elif date_choice == "n":
            while True:
                entered_date = input("Enter Order Date (MM/DD/YYYY): ").strip()
                try:
                    order_date = datetime.strptime(entered_date, "%m/%d/%Y")
                except ValueError:
                    print("Please enter a valid date in MM/DD/YYYY format.")
                    continue

                if order_date.strftime("%m/%d/%Y") == entered_date:
                    break
                print("Please enter a valid date in MM/DD/YYYY format.")
            break
        else:
            print("Please enter Y or N.")
        
    cart = ShoppingCart(
        customer_name=customer_name,
        current_date=order_date.strftime("%B %d, %Y"),
    )

    print("\n===== SHOPPING CART INITIALIZED =====")
    print(f"Customer Name: {cart.customer_name}")
    print(f"Order Date: {cart.current_date}")
    # load the catalogue on first use so managing an empty cart or quitting
    # does not require opening the CSV.
    catalog = None

    while True:
        print("\n===== MAIN MENU =====")
        print("1. Browse and Shop from Categories")
        print("2. Manage Cart, Add/Remove Items, View Cart, Add out-of-catalogue items")
        print("3. Checkout to Payment")
        print("4. Quit")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            if catalog is None:
                catalog = ProductCatalog(
                    Path(__file__).with_name("product_catalogue.csv")
                )
            add_from_catalog(cart, catalog)
        elif choice == "2":
            print_menu(cart, catalog)
        elif choice == "3":
            if checkout(cart, address, order_date):
                return
        elif choice == "4":
            print("\nShopping session ended.")
            return
        else:
            print("Invalid option. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
