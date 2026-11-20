def split_code(code):
    try:
        if not isinstance(code, str):
            return None
        code = code.strip()
        parts = code.split('-')
        if len(parts) != 2:
            return None
        prefix, value_str = parts[0].strip().upper(), parts[1].strip()
        if not prefix or not value_str:
            return None
        value = int(value_str)
        return prefix, value
    except Exception:
        return None

def most_expensive(prices_csv):
    try:
        if not isinstance(prices_csv, str):
            return None
        raw_items = prices_csv.split(',')
        items = [p.strip() for p in raw_items if p.strip()]
        if not items:
            return None
        prices = [float(p) for p in items]
        return max(prices)
    except Exception:
        return None

def expiry_days(date_text):
    try:
        if not isinstance(date_text, str):
            return None
        parts = date_text.strip().split('-')
        if len(parts) != 3:
            return None
        year, month, day = [int(p.strip()) for p in parts]
        if not (1 <= month <= 12 and 1 <= day <= 31):
            return None
        return (year - 2024) * 365 + (month - 1) * 30 + day
    except Exception:
        return None

def main():
    print("==== Running split_code ====")
    user_input = input("Enter a coupon code (e.g. save-20): ")
    result = split_code(user_input)
    print("Prefix and Value:", result)

    print("\n==== Running most_expensive ====")
    user_input = input("Enter item prices as CSV (e.g. 199,49.5,320): ")
    result = most_expensive(user_input)
    print("Most Expensive Item:", result)

    print("\n==== Running expiry_days ====")
    user_input = input("Enter an expiry date as YYYY-MM-DD: ")
    result = expiry_days(user_input)
    print("Days Since 2024:", result)

if __name__ == "__main__":
    main()
