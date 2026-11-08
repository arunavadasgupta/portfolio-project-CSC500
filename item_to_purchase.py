"""
Stores the details and cost of one shopping-cart item.

"""


class ItemToPurchase:
   
    def __init__(
        self, item_name="none", item_price=0.0, item_quantity=0,
        item_description="none"
    ):
        self.item_description = item_description
        self.item_name = item_name
        self.item_price = float(item_price)
        self.item_quantity = int(item_quantity)

    #  properties let callers read and update item details using shorter names.
    #   for example, item.name and item.item_name refer to the same value.
    #   proce and quantity setters also convert inputs to numeric types.
        
    @property
    def name(self):
        return self.item_name

    @name.setter
    def name(self, value):
        self.item_name = value

    @property
    def price(self):
        return self.item_price

    @price.setter
    def price(self, value):
        self.item_price = float(value)

    @property
    def quantity(self):
        return self.item_quantity

    @quantity.setter
    def quantity(self, value):
        self.item_quantity = int(value)

    @property
    def description(self):
        return self.item_description

    @description.setter
    def description(self, value):
        self.item_description = value

    def get_item_cost(self):
        return self.item_price * self.item_quantity

    def print_item_cost(self):
        print(
            f"{self.item_name} {self.item_quantity} "
            f"@ ${self.item_price:.2f} = ${self.get_item_cost():.2f}"
        )
