class User(object):
    def __init__(self, name, is_teacher):
        self.name = name
        self.isteacher = is_teacher
        self.isstudent = not is_teacher
        self.books = {}
        self.fines = 0

    def check_out_book(self, book):
        message = ""
        if self.isteacher:
            if len(self.books.keys()) < 10: # Teachers can't have more than 9 books
                if book.checked_out:
                    message = "Sorry, this book has already been checked out!"
                else:
                    self.books[book] = 50 # Give teacher 50 days with the book
                    message = "You have 50 days before you must return this book"
                    book.check_out()
            else:
                message = "As a teacher, you can't have more than 9 books at a time"
        if self.isstudent:
            if len(self.books.keys()) < 4: # Students can't have more than three books
                if book.checked_out:
                    message = "Sorry, this book has already been checked out!"
                else:
                    self.books[book] = 25 # Give students 25 days with the book
                    message = "You have 25 days before you must return this book"
                    book.check_out()
            else:
                message = "As a student, you can't have more than 3 books at a time"
        return message  # returns the message as a way to "squeeze out" more data from a simple function call

    def return_book(self, book):
        message = ""
        if book not in self.books:
            message = "You haven't checked out this book!"
        else:
            r = dict(self.books)
            del r[book]
            self.books = r
            book.return_self()
            message = "Book successfully returned!"
        return message # Again, return message to give more data for less

    def fine_user(self):
        if self.fines <= 0.8:
            self.fines += 0.20 # For the first five days, the price goes up 20 cents
        elif self.fines <= 6.0:
            self.fines += 1.00 # After that, the price goes up $1 each time
        else:
            self.fines += 2.00 # After 10 days, the price goes up $2 indefinitely
