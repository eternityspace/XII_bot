from collections import UserDict
from datetime import datetime


class Field:

    def __init__(self, value):

        if self.validator(value):
            self.__value = value
        else:
            raise ValueError

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    @staticmethod
    def validator(value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):

        if self.validator(value):
            self.__value = value
        else:
            raise ValueError


class Name(Field):
    pass


class Phone(Field):

    @staticmethod
    def validator(value):
        return len(str(value)) == 10 and value.isdigit()


class Birthday(Field):
    @staticmethod
    def validator(value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            return True
        except:
            return False


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)

        self.phones = []

        if phone:
            self.phones.append(Phone(phone))

        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone = Phone(phone)
        # if str(phone.value) not in [str(p.value) for p in self.phones]:
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)

        return phone

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
        return self.birthday

    def days_to_birthday(self):

        if self.birthday:
            day_of_birthday = datetime.strptime(
                self.birthday.value, '%d.%m.%Y')
            today = datetime.today()
            data = day_of_birthday.replace(year=today.year)

            delta = data - today
            if delta.days < 0:
                data = data.replace(year=today.year + 1)
                delta = data - today

            return delta.days

        return

    def edit_name(self, new_name):
        self.name.value = Name(new_name)

    def edit_phone(self, old_phone, new_phone):
        Phone(new_phone)
        if self.remove_phone(old_phone) is not None:
            return self.add_phone(new_phone)
        return

    def find_phone(self, search):

        for phone in self.phones:
            if str(phone.value) == search:
                return phone

        raise ValueError

    def remove_phone(self, phone):
        len_before = len(self.phones)
        self.phones = [p for p in self.phones if p.value != phone]
        if len_before == len(self.phones):
            return None
        return self

    def __str__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {str(self.birthday)}"

    def __repr__(self):
        return f"Contact name: {str(self.name)}, phones: {'; '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        for user, data in self.data.items():
            if str(data.name.value) == str(record.name.value):
                # if data.name.value == record.name.value:
                return self.data[user]
        self.data[record.name.value] = record

        return record

    def find(self, name: str):  # -> Record:
        # inner method. not for user's search
        for key, value in self.data.items():
            if name == str(key.value):
                # if name == key:
                return self.data[key]

    def iterator(self, n=2):
        values = list(self.data.values())
        for i in range(0, len(values), n):
            yield values[i:i+n]

    def delete(self, name) -> str:
        for person in self.data:

            if isinstance(person, Name):
                if str(person.value) == name:
                    self.data.pop(person)
                    return
            else:
                if person == name:
                    self.data.pop(person)
                    return
        return

    def search(self, text):
        searched_text = text.strip().lower()
        result = []
        if not searched_text:
            return result
        for record in self.data.values():
            if searched_text in str(record.name.value).lower() + ' '.join([phone.value for phone in record.phones]):
                result.append(record)
        return result

    def edit_record(self, old_name, new_name: str):
        slot = self.find(new_name)
        if slot:
            return f'This name {slot} already exists!'
        record = self.find(old_name)
        if record:

            self.delete(str(record.name.value))
            record.edit_name(new_name)
            record = self.add_record(record)

        else:
            raise KeyError

        return record
    # def __eq__(self, other):
    #     return isinstance(other, Phone) and self.value == other.value
