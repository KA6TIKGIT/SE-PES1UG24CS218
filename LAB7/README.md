# Lab 7: Fuzz Testing for Input Validation Bugs

This repository contains the implementation, fuzz testing suite, and hardened solution for **Lab 7: Fuzz Testing for Input Validation Bugs**.

Property-based fuzz testing is performed using Python's [Hypothesis](https://hypothesis.readthedocs.io/) library alongside `pytest` to uncover edge-case inputs, handle unexpected types, and harden code using defensive programming.

---

## 📁 Repository Structure

| File | Description |
| :--- | :--- |
| `coupon_validator.py` | Main application containing the coupon parsing, price calculation, and date validation logic. |
| `test_coupon_validator.py` | Property-based fuzz test suite powered by `hypothesis`. |
| `README.md` | Lab documentation and execution instructions. |

---

## 🛠️ Prerequisites & Installation

Ensure you have Python 3.8+ installed. Install the required testing dependencies:

```bash
pip install hypothesis pytest
```

---

## ⚙️ Functions Under Test

1. **`split_code(code)`**:
   - Parses a coupon string formatted as `PREFIX-VALUE` (e.g., `SAVE-20`).
   - Normalizes whitespace, converts the prefix to uppercase, and returns a tuple `(prefix, value)` where `value` is an integer.
   - Gracefully returns `None` for invalid formats, missing delimiters, non-numeric values, or non-string inputs.

2. **`most_expensive(prices_csv)`**:
   - Parses a comma-separated list of numeric prices (e.g., `"199, 49.5, 320"`).
   - Computes and returns the maximum price as a float.
   - Gracefully handles extra whitespace, malformed delimiters, empty elements, and returns `None` for empty or non-numeric sequences.

3. **`expiry_days(date_text)`**:
   - Parses a date string formatted as `YYYY-MM-DD` (e.g., `2027-01-05`).
   - Computes approximate days relative to the base year 2024: `(year - 2024) * 365 + (month - 1) * 30 + day`.
   - Validates proper delimiters, numeric parsing, month bounds (`1-12`), and day bounds (`1-31`). Returns `None` if invalid.

---

## 🚀 Lab Workflow & Instructions

### Step 1: Install Dependencies
```bash
pip install hypothesis pytest
```

### Step 2: Run Application with Sample Inputs
Run the interactive application:
```bash
python coupon_validator.py
```
*Example test inputs:*
- Coupon code: `SAVE-20`
- Item prices: `199, 49.5, 320`
- Expiry date: `2027-01-05`

### Step 3: Write Property-Based Fuzz Tests
The test suite in `test_coupon_validator.py` uses the `@given(st.text() | st.none())` strategy to generate hundreds of unexpected Unicode strings, empty strings, and `None` inputs to verify that the functions do not crash with unhandled exceptions:

```python
from hypothesis import given, strategies as st
from coupon_validator import split_code, most_expensive, expiry_days

@given(st.text() | st.none())
def test_split_code_no_crash(s):
    try:
        split_code(s)
    except Exception as e:
        assert False, f"split_code crashed with: {e}"

@given(st.text() | st.none())
def test_most_expensive_no_crash(s):
    try:
        most_expensive(s)
    except Exception as e:
        assert False, f"most_expensive crashed with: {e}"

@given(st.text() | st.none())
def test_expiry_days_no_crash(s):
    try:
        expiry_days(s)
    except Exception as e:
        assert False, f"expiry_days crashed with: {e}"
```

### Step 4: Run Tests Against Buggy Implementation
Execute pytest to observe fuzzing uncover input-handling bugs:
```bash
pytest test_coupon_validator.py
```
*Hypothesis identifies minimal falsifying examples such as `s=None`, `s=''`, missing separators, and invalid type conversions.*

### Step 5: Harden Application Code
Defensively program all functions in `coupon_validator.py` by:
- Enforcing type checks (`isinstance(code, str)`)
- Guarding string splits and token bounds
- Validating integer and float conversions within `try...except` blocks
- Validating calendar ranges

Test the interactive script again to confirm valid inputs still work:
```bash
python coupon_validator.py
```

### Step 6: Verify Passing Tests
Re-run pytest against the hardened script:
```bash
pytest test_coupon_validator.py
```
Expected output:
```text
============================== 3 passed in 0.36s ===============================
```

---

## 📸 Screenshots Checklist

1. **Screenshot 1:** Terminal execution and output of initial script with valid inputs.
2. **Screenshot 2:** Pytest execution showing failing tests with Hypothesis falsifying examples.
3. **Screenshot 3:** Terminal output running the hardened `coupon_validator.py`.
4. **Screenshot 4:** Pytest execution showing all 3 tests passing.
