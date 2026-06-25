USERS = {
    "admin": {"password": "1ADMIN", "role": "admin"},
    "cashier": {"password": "1CASHIER", "role": "cashier"},
    "customer": {"password": "1CUSTOMER", "role": "customer"}
}


def login():
    print("=== E-Commerce Login ===")
    username = input("Enter your Username: ").strip().lower()
    password = input("Enter your Password: ").strip()

    user = USERS.get(username)
    if user and user["password"] == password:
        print(f"{user['role'].capitalize()}, you are logged in successfully!")
        return user["role"]

    print("Invalid username or password.")
    return None
