from hypothesis import given, strategies as st
from coupon_validator import split_code, most_expensive, expiry_days

@given(st.text() | st.none())
def test_split_code_no_crash(s):

@given(st.text() | st.none())
def test_most_expensive_no_crash(s):

@given(st.text() | st.none())
def test_expiry_days_no_crash(s):
