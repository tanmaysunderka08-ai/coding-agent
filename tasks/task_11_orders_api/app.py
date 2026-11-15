from handlers import get_order, list_orders, order_items
from router import parse_url

ROUTES = {
    "/orders/get": get_order,
    "/orders/items": order_items,
    "/orders/list": list_orders,
}


def handle(url):
    path, params = parse_url(url)
    handler = ROUTES.get(path)
    if handler is None:
        return 404, {"error": "no such endpoint"}
    try:
        return handler(params)
    except (KeyError, ValueError):
        return 400, {"error": "bad request"}
