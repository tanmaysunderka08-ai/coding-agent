from checkout import pay


def test_bad_format():
    assert pay(10, "4111-1111-abcd-1111", "12/27", "123") == {
        "status": "declined", "reasons": ["card number has the wrong format"]}


def test_expired_card():
    result = pay(10, "4111 1111 1111 1111", "10/26", "123")
    assert result["status"] == "declined" and "card has expired" in result["reasons"]


def test_visa_payment():
    assert pay(49.5, "4111 1111 1111 1111", "12/27", "123") == {
        "status": "approved", "amount": 49.5, "card": "************1111"}


def test_other_brands():
    assert pay(5, "5555-5555-5555-4444", "11/26", "321")["status"] == "approved"
    assert pay(5, "378282246310005", "01/28", "1234")["status"] == "approved"
    assert pay(5, "4012888888881881", "06/29", "999")["status"] == "approved"
    assert pay(5, "6011111111111117", "03/27", "000")["status"] == "approved"


def test_amex_needs_four_digit_code():
    assert pay(5, "378282246310005", "01/28", "123")["reasons"] == ["security code is wrong"]


def test_typo_in_card_number():
    assert pay(10, "4111 1111 1111 1112", "12/27", "123") == {
        "status": "declined", "reasons": ["card number is not valid"]}
    assert pay(10, "5555-5555-5555-4445", "12/27", "123")["reasons"] == ["card number is not valid"]
