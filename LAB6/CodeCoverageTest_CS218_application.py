import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


def test_welcome_coupon_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20

def test_empty_cart_raises():
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")

def test_welcome_coupon_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0

def test_weekend_big_cart():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == pytest.approx(120)

def test_weekend_small_cart():
    assert coupon_discount("WEEKEND20", 200, True, "sun") == 50

def test_weekend_coupon_on_weekday():
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0

def test_flat100_big_cart():
    assert coupon_discount("FLAT100", 400, True, "mon") == 100

def test_flat100_small_cart():
    assert coupon_discount("FLAT100", 200, True, "mon") == 0

def test_unknown_code():
    assert coupon_discount("FAKE", 200, True, "mon") == 0

def test_best_discount_picks_highest():
    assert best_discount(["WELCOME10", "FLAT100"], 400, True, "mon") == 100

def test_best_discount_capped():
    # WEEKEND20 gives 50, but cap is 40% of 100 = 40
    assert best_discount(["WEEKEND20"], 100, True, "sat") == pytest.approx(40)

def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True

def test_expired_true():
    assert is_expired(20, 5, 10) is True

def test_expired_false():
    assert is_expired(8, 5, 10) is False
