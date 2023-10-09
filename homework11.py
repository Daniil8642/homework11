from collections import UserDict
import itertools
from datetime import date, datetime


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
    def __init__(self):
        super().__init__()
        self.chunk_size = 5

    def iterator(self):
        keys = list(self.data.keys())
        for i in range(0, len(keys), self.chunk_size):
            yield {
                k: self.data[k] for k in itertools.islice(keys, i, i + self.chunk_size)
            }

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


if __name__ == "__main__":
    bot = AddressBook()
    bot.run()
