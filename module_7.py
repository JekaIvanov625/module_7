from datetime import datetime, timedelta
class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return str(self.value)
class Birthday(Field):
    def __init__(self, value):
        if not self.is_valid_date(value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY.")
        super().__init__(value)
    @staticmethod
    def is_valid_date(value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            return True
        except ValueError:
            return False
    def to_date(self):
        return datetime.strptime(self.value, "%d.%m.%Y").date()
class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phones = [] if phone is None else [phone]
        self.birthday = Birthday(birthday) if birthday else None
    def add_phone(self, phone):
        "Додати номер телефону до запису"
        self.phones.append(phone)
    def edit_phone(self, old_phone, new_phone):
        "Редагувати існуючий номер телефону"
        if not self.is_valid_phone(new_phone):
            raise ValueError("Invalid phone number.")
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone
        else:
            raise ValueError("Phone number not found.")
    @staticmethod
    def is_valid_phone(phone):
        """Перевірка на валідність номера"""
        return phone.isdigit() and len(phone) >= 7
    def add_birthday(self, birthday):
        "Додати день народження"
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = ', '.join(self.phones)
        birthday = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"{self.name}: {phones}{birthday}"
class Contacts:
    def __init__(self):
        self.contacts = {}
    def add_contact(self, name, phone, birthday=None):
        "Додати контакт"
        if name in self.contacts:
            self.contacts[name].add_phone(phone)
        else:
            self.contacts[name] = Record(name, phone, birthday)
        return "Contact added."
    def change_phone(self, name, old_phone, new_phone):
        "Змінити номер телефону"
        if name in self.contacts:
            self.contacts[name].edit_phone(old_phone, new_phone)
            return "Contact updated."
        else:
            raise KeyError("Contact not found.")
    def show_phone(self, name):
        "Показати номер телефону"
        if name in self.contacts:
            return str(self.contacts[name])
        else:
            raise KeyError("Contact not found.")
    def add_birthday(self, name, birthday):
        "Додати день народження до контакту"
        if name in self.contacts:
            self.contacts[name].add_birthday(birthday)
            return "Birthday added."
        else:
            raise KeyError("Contact not found.")
    def show_birthday(self, name):
        "Показати день народження"
        if name in self.contacts:
            record = self.contacts[name]
            return record.birthday.value if record.birthday else "Birthday not set."
        else:
            raise KeyError("Contact not found.")

    def get_upcoming_birthdays(self):
        " список днів народження на найближчі 7 днів"
        today = datetime.today().date()
        next_week = today + timedelta(days=7)
        upcoming = []
        for record in self.contacts.values():
            if record.birthday:
                bday = record.birthday.to_date()
                bday_this_year = bday.replace(year=today.year)
                if today <= bday_this_year <= next_week:
                    upcoming.append({
                        "name": record.name,
                        "birthday": bday_this_year.strftime("%d.%m.%Y")
                    })
        return upcoming
    def show_all(self):
        "Показати  контакти"
        if not self.contacts:
            return "No contacts found."
        return "\n".join([str(record) for record in self.contacts.values()])
def input_error(func):
    "Обробка помилок введення"
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Invalid command. Please check the input."
    return wrapper


def parse_input(user_input):
    "Обробка введення"
    parts = user_input.strip().lower().split(maxsplit=2)
    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []
    return command, args
def main():
    print("Welcome to the assistant bot!")
    contacts = Contacts()
    while True:
        user_input = input("Enter command: ")
        command, args = parse_input(user_input)
        if command == "hello":
            print("How can I help you?")
        elif command == "add":
            if len(args) < 2:
                print("Give me name and phone please.")
            else:
                name, phone = args[0], args[1]
                birthday = args[2] if len(args) > 2 else None
                print(contacts.add_contact(name, phone, birthday))
        elif command == "change":
            if len(args) < 3:
                print("Give me name, old phone, and new phone please.")
            else:
                name, old_phone, new_phone = args[0], args[1], args[2]
                print(input_error(contacts.change_phone)(name, old_phone, new_phone))
        elif command == "phone":
            if len(args) < 1:
                print("Give me a name please.")
            else:
                name = args[0]
                print(input_error(contacts.show_phone)(name))
        elif command == "add-birthday":
            if len(args) < 2:
                print("Give me name and birthday please.")
            else:
                name, birthday = args[0], args[1]
                print(input_error(contacts.add_birthday)(name, birthday))
        elif command == "show-birthday":
            if len(args) < 1:
                print("Give me a name please.")
            else:
                name = args[0]
                print(input_error(contacts.show_birthday)(name))
        elif command == "birthdays":
            upcoming = contacts.get_upcoming_birthdays()
            if not upcoming:
                print("No upcoming birthdays.")
            else:
                for b in upcoming:
                    print(f"{b['name']}: {b['birthday']}")
        elif command == "all":
            print(contacts.show_all())
        elif command in ["close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command.")
if __name__ == "__main__":
    main()