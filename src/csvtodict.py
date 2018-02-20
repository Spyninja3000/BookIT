from book import Book
import csv
from user import User


def CSVtoBook(my_file):
    book_dict = {}

    with open(my_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='|')
        for row in reader:
            id = row[0]
            name = row[1]
            author = row[2]

            book_dict[int(id)] = Book(id, name, author)

    return book_dict


def CSVtoUsers(my_file):
    users = {}

    with open(my_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=",", quotechar='|')
        for row in reader:
            name = str(row[0])
            isteacher = row[1]
            if str(isteacher).lower() == "student":
                isteacher = False
            elif str(isteacher).lower() == "teacher":
                isteacher = True
            password = row[2]

            users[User(name, isteacher)] = str(password)

    return users