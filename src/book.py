class Book(object):
    def __init__(self, id, name, author):
        self.id = id
        self.name = name
        self.author = author
        self.checked_out = False

    def set(self, name):
        self.name = name

    def get(self):
        return self.name

    def check_out(self):
        self.checked_out = True

    def return_self(self):
        self.checked_out = False