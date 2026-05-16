is_logged_in = False
animals = ["Lion", "Elephant", "Penguin"]


def admin_required(function):
    def wrapper():
        if is_logged_in:
            function()
        else:
            print("Please login as admin first.")

    return wrapper


def login():
    global is_logged_in

    username = input("Username: ")
    password = input("Password: ")

    if username == "admin" and password == "zoo123":
        is_logged_in = True
        print("Login successful.")
    else:
        print("Wrong username or password.")


def logout():
    global is_logged_in

    is_logged_in = False
    print("Logged out.")


@admin_required
def view_animals():
    print("\nZoo Animals:")
    for animal in animals:
        print("-", animal)


@admin_required
def add_animal():
    animal = input("Animal name: ")
    animals.append(animal)
    print("Animal added.")


def main():
    while True:
        print("\nZoo Admin Login System")
        print("1. Login")
        print("2. View animals")
        print("3. Add animal")
        print("4. Logout")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            login()
        elif choice == "2":
            view_animals()
        elif choice == "3":
            add_animal()
        elif choice == "4":
            logout()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
