from repo import find, for_customer


def get_order(params):
    order = find(params.get("id"))
    if order is None:
        return 404, {"error": "order not found"}
    return 200, {"id": order.id, "customer": order.customer, "total": order.total()}


def order_items(params):
    order = find(params.get("id"))
    if order is None:
        return 404, {"error": "order not found"}
    return 200, {"items": [name for name, _, _ in order.items]}


def list_orders(params):
    customer = int(params["customer"])
    limit = int(params.get("limit", 10))
    orders = for_customer(customer)[:limit]
    return 200, {"orders": [o.id for o in orders]}
