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


@input_error
def add(book, data):

    data = data[0]
    name = Name(data[0])
    record = Record(name)
    record = book.add_record(record)

    if len(data) > 1:
        phone = data[1]
        result = record.add_phone(phone)
        book.delete(str(record.name.value))
        book.add_record(result)
        return result

    return record


def console_input():
    return input('> ').lower().strip()


@input_error
def edit(book, data):
    data = data[0]
    if len(data) == 2:
        old_name, new_name = data

        record = book.edit_record(old_name, new_name)
        return record

    elif len(data) == 3:
        name, old_phone, new_phone = data
        record = book.find(name)
        record = record.edit_phone(old_phone, new_phone)
        return record
    else:
        raise IndexError


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
        return f"\n{result}\n"


def hello(book, data):
    return '\n  Hello how can I help you?\n'


def help(book, data):
    return TEXT


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
            result = record.remove_phone(phone)
            # book.delete(record)
            book.add_record(result)
            return result
        else:
            raise KeyError


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
        result = book.iterator(2)

        for record in next(result):
            print(record)


@input_error
def parser(user_input, commands):
    for command in commands:
        if user_input.startswith(command):
            data = user_input.replace(command, '').split()
            return commands[command], data
    else:
        raise IndexError


def main():
    book = AddressBook()

    commands = {
        'add': add,
        'close': good_bye,
        'edit': edit,
        'exit': good_bye,
        'good bye': good_bye,
        'hello': hello,
        'help': help,
        'search': search,
        'remove': remove,
        'show all': show_all,
    }
    try:
        with open(FILE_NAME, 'rb') as fh:
            read_book = pickle.load(fh)
            book.data = read_book
    except:
        print('New phone book has been created\n')

    while True:
        # try:
        user_input = console_input()
        function, *data = parser(user_input, commands)
        result = function(book, data)

        if result is not None:
            print(result)
        if result == 'Good bye!':
            break

        # except:
        #     print('\n Check your input! \n')


if __name__ == '__main__':

    TEXT = \
        """
                       Commands list
        
    create new contact   - - - > 'add name' or 'add name phone(10 digits)'
    add phone to contact - - - > 'add name phone(10 digits)'
    find name or phone   - - - > 'find name' or 'find phone'
    edit contact name    - - - > 'edit old_name new_name'
    edit conctact phone  - - - > 'edit name old_phone new_phone(10 digits)'
    remove contact       - - - > 'remove name'
    remove phone         - - - > 'remove name phone'
    searching            - - - > 'search text'
    show all phone book  - - - > 'show all'
    commands list        - - - > 'help'
    """
    print(TEXT)
    main()
