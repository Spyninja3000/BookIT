from user import User
from librarydb import LibraryDB
from csvtodict import CSVtoBook

class test_with_imported_dict():

    testbookdict = CSVtoBook("Books.csv")

    Tejas = User("Tejas", False)
    Miti = User("Mitesh", False)
    Teacher = User("Mr. Smith", True)

    testusers = {Tejas: "password",
                 Miti: "fakepassword",
                 Teacher: "dogsname123"}

    new_user = User("NEWB", False)

    myDB = LibraryDB(testbookdict, users=testusers)
    myDB.connect(Tejas, "password")