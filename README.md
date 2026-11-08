# Online Shopping Cart — Final Project

A Python console application that lets a customer browse a product catalogue, add items, manage quantities, and review a simulated checkout. The project demonstrates object-oriented design, CSV input, and input validation.

## Run the program

Use Python 3. No third-party packages are required. Keep the five Python files and the included `product_catalogue.csv` in the same directory, using the filenames listed below. From that directory, run:

```bash
python3 main.py
```

Enter a customer name and delivery address. The program checks that the address fields are non-blank and the ZIP code contains five digits. Then choose **Y** to use today's date or **N** to enter a date in `MM/DD/YYYY` format. The program displays the customer name and order date when the cart is initialized.

## Main menu

| Key | Action |
|---|---|
| `1` | Browse categories, search by product name, and add a catalogue item. |
| `2` | Manage the shopping cart. |
| `3` | Review the order and confirm or cancel simulated checkout. |
| `4` | Quit the program. |

## Manage My Cart

| Key | Action |
|---|---|
| `a` | Add an item. Choose `1` to enter a name, description, price, and quantity manually, or `2` to browse the catalogue. Choose `0` to go back. |
| `r` | Select a numbered cart row and remove units. Confirm before removing all remaining units. |
| `c` | Select a numbered row and use `+` or `-` to increase or decrease its quantity. A decrease to zero requires removal confirmation. |
| `i` | Display the numbered item table and available descriptions. |
| `o` | Display the item costs, total quantity, subtotal, tax, shipping, and grand total. |
| `q` | Return to the main menu. |

The subtotal is the sum of each item's unit price multiplied by its quantity. The grand total adds **8% tax** and **$10.00 shipping**. Checkout blocks empty orders and does not process a real payment.

## Project files

| File | Purpose |
|---|---|
| `main.py` | Coordinates customer setup, menus, and checkout. |
| `item_to_purchase.py` | Stores item details and calculates and displays each line cost. |
| `shopping_cart.py` | Stores cart items and handles additions, removals, quantity changes, and totals. |
| `product_catalog.py` | Reads the CSV and handles category browsing, search, and product selection. |
| `address_validator.py` | Collects, validates, and formats the delivery address. |
| `product_catalogue.csv` | Supplies product names, categories, and prices. |
| `pseudoCode.md` | Walks through the program, classes, and menu logic. |

## Design notes

The cart stores each purchase line as an `ItemToPurchase` object. For quantity changes, the program creates a temporary `ItemToPurchase` carrying the item name and new total quantity, then passes it to `modify_item()`. For full removal, the program calls `remove_item()` after confirmation. Both operations can use the selected object to distinguish cart rows with the same name.

Compatibility aliases retain names used in earlier milestones. For example, `get_num_items_in_cart()` delegates to `get_num_items()`, `get_subtotal()` delegates to `get_cost_of_cart()`, and `items` exposes the existing `cart_items` list. The aliases share the same calculations and cart data.

## Data source

[Online Shop 2024 — products.csv (Kaggle)](https://www.kaggle.com/datasets/marthadimgba/online-shop-2024?select=products.csv). The catalogue requires `product_name`, `category`, and `price`. If no product description is supplied, the program uses the product name.
