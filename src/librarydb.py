from Time import gettime


class LibraryDB(object):
    def __init__(self, book_DB, users=None): # assumes that if will be given no users, but will take in any given ones
        self.bookdict = book_DB
        self.USER = None # Current User (NOT THE USER'S NAME!!! THE USER'S NAME IS UNDER "user.name"! This is an object of the "User" class!)
        self.PASS = None # Current User's password
        if users is None or not isinstance(users, dict):
            self.users = {}
        else:
            self.users = users
        self.original_time = gettime() # At the start, the current sec count
        self.current_time = gettime() # is equal to the original sec count
        self.names = {}
        self.UpdateProgress()

    def UpdateProgress(self): # This method should be constantly called using a multi-thread to ensure time precision
        self.current_time = gettime()
        for person in self.users:
            self.names[person.name] = person
        if self.original_time + 86400 <= self.current_time: # 86400 is how many seconds are in a day
            self.original_time = gettime() # re-updates the original time to essentially only count the exact days
            self.current_time = gettime()
            for user in self.users.keys():
                for book in user.books.keys():
                    user.books[book] -= 1
                    if user.books[book] <= 0:
                        user.fine_user()

    def connect(self, username, password):
        self.UpdateProgress()
        message = ""
        if username in self.names.keys(): # Checks that the username and password are correct
            user = self.names[username]
            if self.users[user] == password:
                self.USER = user # And then sets them as the main credentials for the program
                self.PASS = password
                self.UpdateProgress()
                return [True, message]
            else:
                message = "Wrong Password!"
        self.UpdateProgress()
        return [False, message]

    def add_user(self, new_user, new_password):
        message = ""
        self.UpdateProgress()
        if self.USER.isteacher:
            self.users[new_user] = new_password
        else:
            message = "Only teachers can add new users"
        self.UpdateProgress()
        return message

    def delete_user(self, user):
        self.UpdateProgress()
        message = ""
        if self.USER.isteacher:
            try:
                r = dict(self.users)
                del r[user] # deletes user permanently from the user dictionary
                self.users = r
            except:
                message = "This user is not currently registered in the system."
        else:
            message = "Only teachers can delete existing users"
        self.UpdateProgress()
        return message

    def reset(self):
        self.__init__(self.bookdict, self.users)

'''
Track student and teacher names with ability to enter/view/edit names.
Track the issuance of books for a student or teacher.
Manage different limits for the number of books that can be issued to a student or teacher.
Manage the number of days that students and teachers can check out any book. (Hint: Mostly like the number of days will differ for students and teachers).
Give each book a different ID. Also, each book of same name and same author (but number of copies) will have different ID.
Generate/print weekly report to show books issued to whom and number of days leading to the due date return.
Generate/print weekly report of detail of fines (when book not returned on time).
'''
