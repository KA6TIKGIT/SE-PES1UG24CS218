import pytest
from coupon_validator import coupon_discount, best_discount, is_expired


# ---- coupon_discount: guard ----
def test_empty_cart_raises():
    with pytest.raises(ValueError):
        coupon_discount("WELCOME10", 0, True, "mon")

def test_negative_cart_raises():
    with pytest.raises(ValueError):
        coupon_discount("FLAT100", -5, True, "mon")

# ---- WELCOME10 ----
def test_welcome_new_user():
    assert coupon_discount("WELCOME10", 200, True, "mon") == 20

def test_welcome_existing_user():
    assert coupon_discount("WELCOME10", 200, False, "mon") == 0

# ---- WEEKEND20 ----
def test_weekend_sat_big_cart():
    assert coupon_discount("WEEKEND20", 600, True, "sat") == pytest.approx(120)

def test_weekend_sun_exactly_500():
    assert coupon_discount("WEEKEND20", 500, True, "sun") == pytest.approx(100)

def test_weekend_499_gets_flat_50():
    assert coupon_discount("WEEKEND20", 499, True, "sat") == 50

def test_weekend_coupon_on_weekday():
    assert coupon_discount("WEEKEND20", 600, True, "mon") == 0

# ---- FLAT100 ----
def test_flat100_big_cart():
    assert coupon_discount("FLAT100", 301, True, "mon") == 100

def test_flat100_exactly_300():
    assert coupon_discount("FLAT100", 300, True, "mon") == 0

# ---- unknown code ----
def test_unknown_code():
    assert coupon_discount("FAKE", 200, True, "mon") == 0

# ---- best_discount ----
def test_best_discount_empty_list():
    assert best_discount([], 200, True, "mon") == 0

def test_best_discount_picks_highest():
    assert best_discount(["WELCOME10", "FLAT100"], 400, True, "mon") == 100

def test_best_discount_later_code_not_better():
    # FLAT100 gives 100, then WELCOME10 gives 0 (not new user) -> not > best
    assert best_discount(["FLAT100", "WELCOME10"], 400, False, "mon") == 100

def test_best_discount_capped():
    # WEEKEND20 gives 50, cap is 40% of 100 = 40
    assert best_discount(["WEEKEND20"], 100, True, "sat") == pytest.approx(40)

def test_best_discount_under_cap():
    assert best_discount(["WELCOME10"], 200, True, "mon") == 20

# ---- is_expired ----
def test_zero_validity_expired():
    assert is_expired(10, 5, 0) is True

def test_negative_validity_expired():
    assert is_expired(10, 5, -3) is True

def test_expired_true():
    assert is_expired(20, 5, 10) is True

def test_expired_boundary_not_expired():
    assert is_expired(15, 5, 10) is False

def test_expired_false():
    assert is_expired(8, 5, 10) is False
