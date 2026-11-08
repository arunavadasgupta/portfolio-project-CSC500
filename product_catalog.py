"""

Class to handle Product Catalogue with functions for each of the following :

- read and organize database of products, prices and quantities
- handle display of product categories and then products inside the categories, organized by page
- handle searching products

"""




import csv
from item_to_purchase import ItemToPurchase


class ProductCatalog:

    #loads the product database and handles product selection

    def __init__(self, filename):
        self.filename = filename
        self.products = []
        self.load_products()

    def load_products(self):
        self.products = []

        try:
            with open(self.filename, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    self.products.append(row)

        except FileNotFoundError:
            print(
                f"Error: '{self.filename}' was not found. "
                "Please place the CSV file in the program folder."
            )
            raise

    def get_categories(self):
        return sorted(
            set(product["category"] for product in self.products)
        )

    def choose_category(self):
        categories = self.get_categories()

        while True:
            print("\n===== PRODUCT CATEGORIES =====")

            for number, category in enumerate(categories, start=1):
                print(f"{number}. {category}")

            print("B. Back to main menu")

            choice = input("\nChoose a category: ").strip().lower()

            if choice in ("b", "q", "quit"):
                return None

            try:
                category_number = int(choice)

                if 1 <= category_number <= len(categories):
                    return categories[category_number - 1]

                print("Invalid category number. Try again.")

            except ValueError:
                print(
                    "Invalid input. Enter a category number "
                    "or B to return to the main menu."
                )

    def search_products(self, category, search_text):
        matching_products = []

        for product in self.products:
            if (
                product["category"] == category
                and search_text.lower() in product["product_name"].lower()
            ):
                matching_products.append(product)

        return matching_products

    def get_quantity(self, product_name):
        while True:
            quantity_input = input(
                f"Enter quantity for {product_name}: "
            ).strip()

            try:
                quantity = int(quantity_input)

                if quantity > 0:
                    return quantity

                print("Quantity must be greater than 0.")

            except ValueError:
                print(
                    f"'{quantity_input}' is not a valid quantity. "
                    "Enter a whole number."
                )

    def choose_product(self, category):
        while True:
            print(f"\nPress Enter to see all products page by page or")
            search_text = input(
                f"\nSearch within {category} "
                "(B = categories, M = main menu): "
            ).strip()

            if search_text.lower() == "m":
                return "main"

            if search_text.lower() == "b":
                return None

            matching_products = self.search_products(
                category,
                search_text
            )

            if len(matching_products) == 0:
                print("No matching products found. Try again.")
                continue

            page_size = 5
            start_index = 0

            while True:
                end_index = start_index + page_size
                current_page = matching_products[start_index:end_index]

                print("\n===== MATCHING PRODUCTS =====")

                for number, product in enumerate(
                    current_page,
                    start=1
                ):
                    print(
                        f"{number}. "
                        f"{product['product_name']} "
                        f"- ${float(product['price']):.2f}"
                    )

                current_page_number = (
                    start_index // page_size
                ) + 1

                total_pages = (
                    len(matching_products) + page_size - 1
                ) // page_size

                print(
                    f"\nPage {current_page_number} "
                    f"of {total_pages}"
                )

                print("\n1-5 = Select product")
                print("N   = Next page")
                print("P   = Previous page")
                print("S   = New search")
                print("B   = Back to categories")
                print("M   = Back to main menu")

                choice = input(
                    "\nYour choice: "
                ).strip().lower()

                if choice == "n":
                    if end_index < len(matching_products):
                        start_index += page_size
                    else:
                        print(
                            "\nYou are already on the last page."
                        )

                elif choice == "p":
                    if start_index >= page_size:
                        start_index -= page_size
                    else:
                        print(
                            "\nYou are already on the first page."
                        )

                elif choice == "s":
                    break

                elif choice == "b":
                    return None

                elif choice in ("m", "q", "quit"):
                    return "main"

                elif choice.isdigit():
                    product_number = int(choice)

                    if 1 <= product_number <= len(current_page):
                        selected_product = current_page[
                            product_number - 1
                        ]

                        quantity = self.get_quantity(
                            selected_product["product_name"]
                        )

                        description = (
                            selected_product.get("description")
                            or selected_product.get("product_description")
                            or selected_product["product_name"]
                        )

                        return ItemToPurchase(
                            item_name=selected_product["product_name"],
                            item_price=float(
                                selected_product["price"]
                            ),
                            item_quantity=quantity,
                            item_description=description
                        )

                    print("Invalid product number.")

                else:
                    print("Invalid choice.")
