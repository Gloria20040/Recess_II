import csv
import json
import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSV_FILE = os.path.join(BASE_DIR, "students.csv")
JSON_FILE = os.path.join(BASE_DIR, "students.json")
LOG_FILE = os.path.join(BASE_DIR, "student_system.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class StudentExistsError(Exception):
    pass
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Registration", "Name", "Age"])

if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, "w") as file:
        json.dump({}, file, indent=4)

def display_menu():
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Exit")

def load_json():
    with open(JSON_FILE, "r") as file:
        return json.load(file)


def save_json(data):
    with open(JSON_FILE, "w") as file:
        json.dump(data, file, indent=4)

def add_student():

    try:
        reg = input("Registration Number: ").strip().upper()

        if reg == "":
            print("Registration number cannot be empty.")
            return

        name = input("Student Name: ").strip()

        if name == "":
            print("Name cannot be empty.")
            return

        age = int(input("Age: "))

        if age <= 0:
            print("Age must be greater than zero.")
            return

        address = input("Address: ")
        contact = input("Contact: ")
        program = input("Program: ")

        details = load_json()

        if reg in details:
            raise 
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([reg, name, age])

        details[reg] = {
            "address": address,
            "contact": contact,
            "program": program
        }

        save_json(details)

        logging.info(f"{reg} added successfully.")

        print("Student added successfully!")

    except ValueError:
        print("Age must be a number.")
        logging.error("Invalid age entered.")

    except StudentExistsError as e:
        print(e)
        logging.error(e)

    except Exception as e:
        print("Error:", e)
        logging.error(e)

def view_students():

    try:
        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)

            rows = list(reader)

            if len(rows) <= 1:
                print("\nNo student records found.")
                return

            print("\n===== STUDENT RECORDS =====")
            print(f"{'Registration':<15}{'Name':<25}{'Age':<5}")
            print("-" * 45)

            for row in rows[1:]:
                print(f"{row[0]:<15}{row[1]:<25}{row[2]:<5}")

        logging.info("Viewed all student records.")

    except FileNotFoundError:
        print("Student file not found.")
        logging.error("CSV_FILE not found.")

    except Exception as e:
        print("Error:", e)
        logging.error(e)

def search_student():

    try:
        reg = input("Enter Registration Number: ").strip().upper()

        found = False

        details = load_json()

        with open(CSV_FILE, "r") as file:
            reader = csv.reader(file)

            next(reader)

            for row in reader:

                if row[0] == reg:

                    print("\n===== STUDENT FOUND =====")
                    print(f"Registration : {row[0]}")
                    print(f"Name         : {row[1]}")
                    print(f"Age          : {row[2]}")

                    if reg in details:
                        print(f"Address      : {details[reg]['address']}")
                        print(f"Contact      : {details[reg]['contact']}")
                        print(f"Program      : {details[reg]['program']}")

                    found = True
                    logging.info(f"Student {reg} searched.")
                    break

        if not found:
            print("Student not found.")
            logging.warning(f"Search failed for {reg}.")

    except FileNotFoundError:
        print("Student records file not found.")
        logging.error("CSV_FILE not found.")

    except Exception as e:
        print("Error:", e)
        logging.error(e)

def update_student():

    try:
        reg = input("Enter Registration Number to update: ").strip().upper()

        rows = []

        updated = False

        details = load_json()

        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.reader(file)

            header = next(reader)
            rows.append(header)

            for row in reader:

                if row[0] == reg:

                    print("\nEnter New Details")

                    name = input("New Name: ").strip()

                    while True:
                        try:
                            age = int(input("New Age: "))
                            if age > 0:
                                break
                            else:
                                print("Age must be greater than zero.")
                        except ValueError:
                            print("Age must be a number.")

                    address = input("New Address: ")
                    contact = input("New Contact: ")
                    program = input("New Program: ")

                    row = [reg, name, age]

                    details[reg] = {
                        "address": address,
                        "contact": contact,
                        "program": program
                    }

                    updated = True

                rows.append(row)

        if updated:

            with open(CSV_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            save_json(details)

            print("Student updated successfully.")

            logging.info(f"{reg} updated.")

        else:
            print("Student not found.")

    except Exception as e:
        print("Error:", e)
        logging.error(e)

def delete_student():

    try:
        reg = input("Enter Registration Number to delete: ").strip().upper()

        rows = []
        deleted = False

        details = load_json()

        with open(CSV_FILE, "r", newline="") as file:
            reader = csv.reader(file)

            header = next(reader)
            rows.append(header)

            for row in reader:
                if row[0] == reg:
                    deleted = True
                    continue   

                rows.append(row)

        if deleted:
            with open(CSV_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(rows)

            if reg in details:
                del details[reg]

            save_json(details)

            print("Student deleted successfully.")
            logging.info(f"{reg} deleted successfully.")

        else:
            print("Student not found.")
            logging.warning(f"Delete failed. {reg} not found.")

    except FileNotFoundError:
        print("Student records file not found.")
        logging.error("CSV_FILE not found.")

    except Exception as e:
        print("Error:", e)
        logging.error(e)


def main():

    while True:

        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
         add_student()

        elif choice == "2":
         view_students()

        elif choice == "3":
         search_student()

        elif choice == "4":
         update_student()

        elif choice == "5":
         delete_student()

        elif choice == "6":
            print("Thank you.")
            logging.info("Program closed.")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()