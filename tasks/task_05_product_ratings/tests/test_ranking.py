from ranking import leaderboard, product_page

DATA = """
kettle  | 5 | 10 | yes
kettle  | 2 | 0  | no
kettle  | 4 | 3  | yes
toaster | 5 | 0  | no
toaster | 5 | 1  | no
toaster | 3 | 10 | yes
lamp    | 4 | 0  | yes
lamp    | 4 | 0  | yes
lamp    | 6 | 0  | yes
"""


def test_product_without_reviews():
    assert product_page(DATA, "fridge") == {"reviews": 0, "plain": 0.0, "rating": 0.0, "score": 3.0}


def test_kettle_page():
    assert product_page(DATA, "kettle") == {"reviews": 3, "plain": 3.67, "rating": 4.16, "score": 3.5}


def test_lamp_page():
    assert product_page(DATA, "lamp") == {"reviews": 2, "plain": 4.0, "rating": 4.0, "score": 3.33}


def test_leaderboard():
    assert leaderboard(DATA) == ["kettle", "toaster", "lamp"]
