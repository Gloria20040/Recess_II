from login import login

COUPONS = {
    "NEWBIES": 0.10,
    "WELCOME": 0.08,
    "FREESHIP": 0.05
}

TAX_RATES = {
    "A": 0.0825,
    "B": 0.08875,
    "C": 0.0625,
    "DEFAULT": 0.07
}


def calcFinalPrice(subtotal, tax_rate, discount_rate, coupon_rate):
    discount_amount = subtotal * discount_rate
    coupon_amount = subtotal * coupon_rate
    taxable_amount = subtotal - discount_amount - coupon_amount
    tax_amount = taxable_amount * tax_rate
    final_price = taxable_amount + tax_amount
    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "coupon_amount": coupon_amount,
        "taxable_amount": taxable_amount,
        "tax_amount": tax_amount,
        "final_price": final_price
    }


def get_location_tax_rate(location):
    location = location.strip().upper()
    if location == "A":
        return TAX_RATES["A"]
    elif location == "B":
        return TAX_RATES["B"]
    else:
        if location == "C":
            return TAX_RATES["C"]
        return TAX_RATES["DEFAULT"]


def get_discount_rate(subtotal):
    if subtotal >= 500:
        return 0.15
    else:
        if subtotal >= 250:
            return 0.10
        elif subtotal >= 100:
            return 0.05
        else:
            return 0.00


def validate_coupon(coupon_code):
    coupon_code = coupon_code.strip().upper()
    if coupon_code == "":
        return 0.0, "No coupon code used."
    if coupon_code in COUPONS:
        return COUPONS[coupon_code], f"Coupon '{coupon_code}' applied."
    return 0.0, f"Coupon '{coupon_code}' is invalid. No coupon discount applied."


def request_float(prompt, default=0.0):
    while True:
        value = input(prompt).strip()
        if value == "" and default is not None:
            return default
        try:
            return float(value)
        except ValueError:
            print("Please enter a valid numeric value.")


def run_ecommerce():
    role = login()
    if role is None:
        return

    print(f"Logged in as: {role.capitalize()}")
    print("=== Order Calculator ===")

    subtotal = request_float("Enter subtotal amount: SHS ")
    location = input("Enter location code (A, B, C, or other): ").strip()
    tax_rate = get_location_tax_rate(location)
    tier_discount = get_discount_rate(subtotal)

    coupon_input = input("Enter coupon code (leave blank if none): ").strip()
    coupon_rate, coupon_message = validate_coupon(coupon_input)
    print(coupon_message)

    manual_discount = 0.0
    if role in ("admin", "cashier"):
        manual_discount = request_float(
            "Enter manual discount percentage to apply (0-20, leave blank for none): ",
            default=0.0
        ) / 100.0
        if manual_discount < 0:
            manual_discount = 0.0
        elif manual_discount > 0.20:
            manual_discount = 0.20
            print("Manual discount capped at 20% for security.")

    if role == "customer" and manual_discount > 0:
        manual_discount = 0.0
        print("Customers cannot apply manual discount percentages.")

    effective_discount = max(tier_discount, manual_discount)
    if manual_discount > tier_discount:
        discount_source = "manual discount"
    else:
        discount_source = "subtotal tier discount"

    results = calcFinalPrice(subtotal, tax_rate, effective_discount, coupon_rate)

    print("\n=== Price Summary ===")
    print(f"Subtotal: SHS {results['subtotal']:.2f}")
    print(f"Tax rate: {tax_rate * 100:.2f}%")
    print(f"{discount_source.capitalize()}: {effective_discount * 100:.2f}%")
    print(f"Discount amount: SHS {results['discount_amount']:.2f}")
    print(f"Coupon amount: SHS {results['coupon_amount']:.2f}")
    print(f"Taxable amount after discounts: SHS {results['taxable_amount']:.2f}")
    print(f"Tax amount: SHS {results['tax_amount']:.2f}")
    print(f"Final price: SHS {results['final_price']:.2f}")

    if role == "admin":
        print("\nAdmin access: full calculator mode enabled.")
    elif role == "cashier":
        print("Cashier access: order entry and coupon validation enabled.")
    else:
        print("Customer access: view order totals and apply valid coupons.")


if __name__ == "__main__":
    run_ecommerce()


