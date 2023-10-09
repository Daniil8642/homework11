from collections import UserDict
import itertools
from datetime import date, datetime


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except (ValueError, IndexError):
            return "Give me name and phone please"

    return wrapper


class AssistantBot:
    def __init__(self):
        self.contacts = {}

    @input_error
    def add_contact(self, name, phone):
        self.contacts[name] = phone
        return f"Added {name} with phone number {phone}"

    @input_error
    def change_contact(self, name, phone):
        if name in self.contacts:
            self.contacts[name] = phone
            return f"Changed phone number for {name} to {phone}"
        else:
            return f"Contact {name} not found"

    @input_error
    def show_phone(self, name):
        if name in self.contacts:
            return f"{name}'s phone number is {self.contacts[name]}"
        else:
            return f"Contact {name} not found"

    def show_all(self):
        if not self.contacts:
            return "No contacts found"
        else:
            result = ""
            for name, phone in self.contacts.items():
                result += f"{name}: {phone}\n"
            return result

    def handle_command(self, command):
        command = command.lower()
        if command == "hello":
            return "How can I help you?"
        elif command.startswith("add "):
            parts = command.split(" ", 2)
            if len(parts) != 3:
                return "Invalid input format"
            name, phone = parts[1], parts[2]
            return self.add_contact(name, phone)
        elif command.startswith("change "):
            parts = command.split(" ", 2)
            if len(parts) != 3:
                return "Invalid input format"
            name, phone = parts[1], parts[2]
            return self.change_contact(name, phone)
        elif command.startswith("phone "):
            name = command.split(" ", 1)[1]
            return self.show_phone(name)
        elif command == "show all":
            return self.show_all()
        elif command in ("good bye", "close", "exit"):
            return "Good bye!"
        else:
            return "Unknown command"

    def run(self):
        while True:
            command = input("Enter a command: ")
            if command == ".":
                break
            response = self.handle_command(command)
            print(response)


if __name__ == "__main__":
    bot = AssistantBot()
    bot.run()


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return str(self._value)

    @value.setter
    def value(self, value):
        self.validate(value)
        self._value = value

    def validate(self, value):
        pass

    def __str__(self):
        return str(self._value)


class Name(Field):
    pass


class Phone(Field):
    def validate(self, value):
        if not (len(value) == 10 and value.isdigit()):
            raise ValueError("Неверный формат номера телефона")


class Birthday(Field):
    def validate(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неверный формат даты дня рождения")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def days_to_birthday(self):
        if self.birthday:
            today = date.today()
            next_birthday = date(
                today.year, self.birthday.value.month, self.birthday.value.day
            )
            if today > next_birthday:
                next_birthday = date(
                    today.year + 1, self.birthday.value.month, self.birthday.value.day
                )
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        if old_phone in [p.value for p in self.phones]:
            self.remove_phone(old_phone)
            self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def iterator(self, chunk_size):
        keys = list(self.data.keys())
        for i in range(0, len(keys), chunk_size):
            yield {k: self.data[k] for k in itertools.islice(keys, i, i + chunk_size)}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]



