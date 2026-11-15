from dataclasses import dataclass, field


@dataclass
class Order:
    id: int
    customer: int
    items: list = field(default_factory=list)   # (name, qty, unit_price)

    def total(self):
        return round(sum(qty * price for _, qty, price in self.items), 2)


ORDERS = [
    Order(1041, 7, [("pen", 10, 1.5)]),
    Order(1042, 7, [("notebook", 2, 4.25), ("pen", 3, 1.5)]),
    Order(1043, 9, [("stapler", 1, 12.0)]),
    Order(1044, 7, [("tape", 4, 2.0)]),
]


def find(order_id):
    for order in ORDERS:
        if order.id == order_id:
            return order
    return None


def for_customer(customer_id):
    return [o for o in ORDERS if o.customer == customer_id]
