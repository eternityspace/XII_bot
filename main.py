from classes import *
import pickle
import itertools


FILE_NAME = 'phone_book.pickle'


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return ('\n  There is no contact with this name!\n')
        except ValueError:
            return ('\n  Check the phone number! Should be 10 digits\n')
        except IndexError:
            return ('\n  Check your input!\n')

    return inner


# @input_error
# def add(book, data):

#     data = data[0]
#     name = Name(data[0])
#     record = Record(name)
#     record = book.add_record(record)

#     if len(data) > 1:
#         phone = data[1]
#         result = record.add_phone(phone)

#         if len(data) > 2:
#             birthday = data[2]
#             result = record.add_birthday(birthday)

#         book.delete(str(record.name.value))
#         book.add_record(result)
#         return result

#     return record


@input_error
def add_contact_phone_birthday(book, data):

    data = data[0]
    name = data[0]
    phone = data[1]
    birthday = None
    if len(data) > 2:
        birthday = data[2]

    record = Record(name, phone, birthday)
    book.add_record(record)

    return record


@input_error
def add_contact(book, data):

    record = Record(Name(data[0][0]))
    book.add_record(record)
    return record


@input_error
def add_phone(book, data):
    data = data[0]
    name = data[0]
    record = book.find(name)
    phone = data[1]
    record.add_phone(phone)
    # result = record.add_phone(phone)
    # book.delete(record)
    # book.add_record(result)
    return record


@input_error
def add_birthday(book, data):
    data = data[0]
    name = data[0]
    record = book.find(name)
    birthday = data[1]
    record.add_birthday(birthday)

    return record


def console_input():
    return input('> ').lower().strip()


@input_error
def edit_name(book, data):
    data = data[0]
    old_name, new_name = data
    record = book.edit_record(old_name, new_name)
    return record


@input_error
def edit_phone(book, data):
    data = data[0]
    name, old_phone, new_phone = data
    print(new_phone, old_phone)
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return record


@input_error
def edit_birthday(book, data):
    data = data[0]
    name, birthday = data
    record = book.find(name)
    record.add_birthday(birthday)
    return record


@input_error
def days_to_birthday(book, data):
    name = data[0][0]
    record = book.find(name)
    if record:
        result = record.days_to_birthday()
        return f"Days to birthday: {result}"


@input_error
def find(book, data):

    search = data[0]

    if search.isdigit():
        phone = search
        for name, record in book.items():
            if record.find_phone(phone):
                return f'\n{record}\n'
            else:
                raise KeyError
    else:

        result = book.find(search)
        if not result:
            raise KeyError
        return result


def hello(book, data):
    return '\n  Hello how can I help you?\n'


def help(book, data):
    return TEXT


@input_error
def good_bye(book, data):
    try:
        with open(FILE_NAME, 'wb') as fh:
            pickle.dump(book.data, fh)

    except Exception as e:
        return e

    return 'Good bye!'


@input_error
def remove(book, data):
    data = data[0]
    name = data[0]

    if len(data) == 1:
        record = book.delete(name)
        return '\n  Contact has been removed\n'

    else:
        phone = data[1]
        record = book.find(name)
        book.delete(record)
        if record:
            record.remove_phone(phone)
            # book.delete(record)
            # book.add_record(result)
            return record
        else:
            raise KeyError


@input_error
def search(book, data):
    text = data[0][0]
    result = book.search(text)

    if result != []:
        for record in result:
            print(record)

    else:
        print('\n  No results \n')


def show_all(book, data):
    if not book:
        print('\n Phone book is empty\n')

    else:
        # for name, record in book.data.items():
        #     print(f'\n{record}\n')
        # result = book.iterator(2)

        for record in book.iterator(2):
            # print(record)
            print(*record)
            input('')


@input_error
def parser(user_input, commands):
    for command in commands:
        if user_input.startswith(command):
            # data = user_input.replace(command, '').split()
            data = user_input.split()[1:]
            return commands[command], data
    else:
        raise IndexError


def main():
    book = AddressBook()

    commands = {




        # New contact, phone, birthday - - - > 1 Alex 1111111111 31.12.1700
        "1": add_contact_phone_birthday,
        "2": add_contact,                # New contact                  - - - > 2 Alex
        "3": add_phone,                  # Add phone                    - - - > 3 Alex 2222222222
        # Add birthday                 - - - > 4 Alex 31.12.1700
        "4": add_birthday,
        "5": edit_name,                  # Edit name                    - - - > 5 Alex Alexandr
        # # Edit phone                   - - - > 6 Alexandr 2222222222 3333333333
        "6": edit_phone,
        # # Edit birthday                - - - > 7 Alexandr 31.12.1701
        '7': edit_birthday,
        "8": days_to_birthday,           # Day to birthday              - - - > 8 Alexandr
        "search": search,                     # Search                       - - - > 9 text
        "remove": remove,
        "show all": show_all,                  # Show all contact            - - - > show all
        'help': help,                      # Commands list               - - - > help
        # # Good bye!                   - - - > good bye / exit / close
        'good bye': good_bye,

    }
    try:
        with open(FILE_NAME, 'rb') as fh:
            read_book = pickle.load(fh)
            book.data = read_book
    except:
        print('New phone book has been created\n')

    while True:
        try:
            user_input = console_input()
            function, *data = parser(user_input, commands)
            result = function(book, data)

            if result is not None:
                print(result)
            if result == 'Good bye!':
                break

        except:
            print('\n Check your input! \n')


if __name__ == '__main__':

    TEXT = \
        """
                       Commands list
        
    1. New contact, phone, birthday - - - > 1 Alex 1111111111 31.12.1700
    2. New contact                  - - - > 2 Alex
    3. Add phone                    - - - > 3 Alex 2222222222
    4. Add birthday                 - - - > 4 Alex 31.12.1700
    5. Edit name                    - - - > 5 Alex Alexandr
    6. Edit phone                   - - - > 6 Alexandr 2222222222 3333333333
    7. Edit birthday                - - - > 7 Alexandr 31.12.1701
    8. Day to birthday              - - - > 8 Alexandr
    9. Search                       - - - > 9 text
    10. remove contact              - - - > remove name
    11. remove phone                - - - > remove name phone
    12. Show all contact            - - - > show all
    13. Commands list               - - - > help
    14. Good bye!                   - - - > good bye / exit / close
    
    """
    print(TEXT)
    main()
