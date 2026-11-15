from app import handle


def test_list_orders():
    assert handle("/orders/list?customer=7&limit=2") == (200, {"orders": [1041, 1042]})
    assert handle("/orders/list?customer=9") == (200, {"orders": [1043]})


def test_bad_requests():
    assert handle("/orders/list") == (400, {"error": "bad request"})
    assert handle("/nope") == (404, {"error": "no such endpoint"})
    assert handle("/orders/get?id=9999") == (404, {"error": "order not found"})


def test_get_order():
    assert handle("/orders/get?id=1042") == (200, {"id": 1042, "customer": 7, "total": 13.0})


def test_order_items():
    assert handle("/orders/items?id=1043") == (200, {"items": ["stapler"]})


def test_id_with_leading_zero():
    assert handle("/orders/get?id=01044") == (200, {"id": 1044, "customer": 7, "total": 8.0})
