from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError("Phone not found.")

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            self.add_phone(new_phone)
            self.remove_phone(old_phone)
        else:
            raise ValueError("Phone not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "N/A"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError("Contact not found.")

    def get_upcoming_birthdays(self):
        today = datetime.today()
        next_week = today + timedelta(days=7)
        birthdays = []
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year)
                if today <= bday_this_year <= next_week:
                    birthdays.append({"name": record.name.value, "birthday": bday_this_year.strftime("%d.%m.%Y")})
        return birthdays

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())

# Command Handlers
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    return "Contact not found."

def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record:
        return str(record)
    return "Contact not found."

def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    return "Contact not found."

def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record and record.birthday:
        return f"Birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    return "Birthday not found."

def upcoming_birthdays(_, book):
    birthdays = book.get_upcoming_birthdays()
    if birthdays:
        return "\n".join(f"{b['name']}: {b['birthday']}" for b in birthdays)
    return "No upcoming birthdays."

def list_all(_, book):
    return str(book) if book.data else "No contacts found."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    commands = {
        "add": add_contact,
        "change": change_contact,
        "phone": show_phone,
        "add-birthday": add_birthday,
        "show-birthday": show_birthday,
        "birthdays": upcoming_birthdays,
        "all": list_all
    }

    while True:
        user_input = input("Enter a command: ")
        parts = user_input.split()
        command, args = parts[0], parts[1:]

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        handler = commands.get(command)
        if handler:
            try:
                print(handler(args, book))
            except (ValueError, KeyError) as e:
                print(e)
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()