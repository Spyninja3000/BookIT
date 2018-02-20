# This file is the main test for the Database set up process. It can be used to look through the gui process of the product itself
# By: Tejas Shah

import tkinter as tk
from tkinter import filedialog
from librarydb import LibraryDB
import csvtodict
from time import sleep
import threading
from book import Book
from subprocess import Popen

def execute(**nameismain): # mega-method to load into constructor file
    manual_insert_files = True  # Decides whether to have files loaded into software or automatically use pre-loaded default file
    
    logo_file = "Logo.ico"

    if not nameismain:
        print("It's totally fine that you're using a console for this, just don't do anything you're not supposed to do, okay?")

    class thing(object): # this class is just a generic class used throughout as a way to retain and bind attributes
        def __init__(self, arg=None):
            self.arg = arg
        def set(self, arg):
            self.arg = arg
        def get(self):
            return self.arg

    books = thing()
    users = thing()

    if manual_insert_files:

        fileinsert = tk.Tk()
        fileframe = tk.Frame(fileinsert)
        fileinsert.title("Load in files")
        fileinsert.iconbitmap(default=logo_file)

        def open_instructions():
            fname = "BookIT_Instructions.pdf"
            Popen([fname], shell=True)

        tk.Label(fileinsert, text="Please load in the excel documents for both the Books and the Users in CSV file format.").grid()
        tk.Button(fileinsert, text="How exactly must I format my excel documents?", command=open_instructions).grid()

        tk.Label(fileinsert, text="Books file loaded: ").grid(row=3, column=0)
        booke = tk.Label(fileinsert, text="Not Done")
        booke.grid(row=3, column=1)

        tk.Label(fileinsert, text="Users file loaded: ").grid(row=4, column=0)
        usere = tk.Label(fileinsert, text="Not Done")
        usere.grid(row=4, column=1)

        def getbooks():
            bookfpath = filedialog.askopenfilename(initialdir = "/",title = "Select Excel document of Books") # File must be CSV
            temp = csvtodict.CSVtoBook(bookfpath)
            tk.Label(fileinsert, text="All Good!").grid(row=3, column=1)
            fileinsert.update()
            books.set(temp)

        def getusers():
            userfpath = filedialog.askopenfilename(initialdir = "/",title = "Select Excel document of Users") # File must be CSV
            temp = csvtodict.CSVtoUsers(userfpath)
            tk.Label(fileinsert, text="All Good!").grid(row=4, column=1)
            fileinsert.update()
            users.set(temp)

        tk.Button(fileinsert, text="Choose book file", command=getbooks).grid()
        tk.Button(fileinsert, text="Choose users file", command=getusers).grid()

        tk.Button(fileinsert, text="Done", command=fileinsert.destroy).grid()

        fileinsert.mainloop()

    myDB = LibraryDB(books.get(), users=users.get())

    loop = thing(False) # Tells the thread whether or not to activate the crazy-speed updating thread
    # The Update Thread crashes the system, so...

    if loop.get():
        class update_thread(threading.Thread):
            def __init__(self, *args):
                super(update_thread, self).__init__()
                self.args = args
                while True:
                    myDB.UpdateProgress()

        update_loop = update_thread()

    def check_out_window():
        checkout = tk.Tk()
        checkout.title("Check out book")
        checkout.iconbitmap(default=logo_file)

        checkframe = tk.Frame(checkout)
        checkframe.grid()

        tk.Label(checkout, text="Book ID to check out: ").grid(row=0)

        bookid = tk.Entry(checkout)
        bookid.grid(row=0, column=1)

        def search_book():
            id = int(bookid.get())

            if isinstance(myDB.bookdict[id], Book):
                bookname = tk.StringVar(root)
                bookname.set("Would you like to check out: " + str(myDB.bookdict[id].name) + "?")

                quickmessage = tk.Tk()
                quickmessage.title("Confirm book check out")
                quickmessage.iconbitmap(default=logo_file)

                quickframe = tk.Frame(quickmessage)
                quickframe.grid()

                tk.Label(quickmessage, text=bookname.get()).grid()

                def no():
                    quickmessage.destroy()

                def yes():
                    transaction = myDB.USER.check_out_book(myDB.bookdict[id])
                    tk.Label(quickmessage, text=str(transaction)).grid()

                tk.Button(quickmessage, text='No/Exit', command=no).grid(row=3, column=0)
                tk.Button(quickmessage, text="Yes", command=yes).grid(row=3, column=1)

                quickmessage.mainloop()

        tk.Button(checkout, text="Check out Book", command=search_book).grid()

        checkout.mainloop()

    def return_window():
        rewin = tk.Tk()
        rewin.title("Return Book")
        rewin.iconbitmap(default=logo_file)

        reframe = tk.Frame(rewin)
        reframe.grid()

        tk.Label(rewin, text="Book ID to return: ").grid(row=0)

        bookid = tk.Entry(rewin)
        bookid.grid(row=0, column=1)

        def get_book():
            id = int(bookid.get())

            if isinstance(myDB.bookdict[id], Book):
                bookname = tk.StringVar(root)
                bookname.set("Would you like to return: " + str(myDB.bookdict[id].name) + "?")

                quickmessage = tk.Tk()
                quickmessage.title("Confirm Book return")
                quickmessage.iconbitmap(default=logo_file)
                quickframe = tk.Frame(quickmessage)
                quickframe.grid()

                tk.Label(quickmessage, text=bookname.get()).grid()

                def no():
                    quickmessage.destroy()

                def yes():
                    transaction = myDB.USER.return_book(myDB.bookdict[id])
                    tk.Label(quickmessage, text=str(transaction)).grid()
                    sleep(2)

                tk.Button(quickmessage, text='No/Exit', command=no).grid(row=3, column=0)
                tk.Button(quickmessage, text="Yes", command=yes).grid(row=3, column=1)

                quickmessage.mainloop()

        tk.Button(rewin, text="Return Book", command=get_book).grid()
        rewin.mainloop()
        root.update()

    def refresh_main():
        try:
            root.destroy()
        except:
            pass

        open_main()

    def open_main():

        try:
            connect.destroy() # Destroy connect widget unless it's already been destroyed
        except tk.TclError:
            pass

        global root
        root = tk.Tk()

        root.winfo_colormapfull()

        frame = tk.Frame(root)
        frame.grid()

        root.title("My Account Info")
        root.iconbitmap(default=logo_file)

        tk.Label(root, text="My Account Info: " + str(myDB.USER.name)).grid()

        def display_fines():
            formatted = thing("Your fines are: $" + str(myDB.USER.fines))

            fines = tk.StringVar()
            fines.set(str(formatted.get()))

            label = tk.Label(root, text=fines.get(), fg="dark green")
            return label

        def display_books():
            booklabels = []
            booklabels.append(tk.Label(root, text="Books: "))
            for book in myDB.USER.books:
                booklabels.append(tk.Label(root, text="ID=" + str(book.id) + ": " + str(book.name) + " by " + str(book.author)+ ": Due in " + str(myDB.USER.books[book]) + " days"))
            return booklabels

        def add_user():
            add = tk.Tk()

            add.title("Manage Users")
            add.iconbitmap(default=logo_file)

            adframe = tk.Frame(add)
            adframe.grid()

            tk.Label(add, text="Here are this database's current users:").grid()
            for user in myDB.users.keys():
                tk.Label(add, text=str(user.name)).grid()

            tk.Label(add, text="User to Add").grid(row=0)

            usertoadd = tk.Entry(add)
            usertoadd.grid(row=0, column=1)

            tk.Label(add, text="Added User's Password").grid(row=1)

            useaddpass = tk.Entry(add)
            useaddpass.grid(row=1, column=1)

            def submit_add():
                myuser = str(usertoadd.get())
                mypass = str(useaddpass.get())

                confirm = tk.StringVar(root)
                confirm.set("Would you like to add user: " + myuser + "?")

                quickmessage = tk.Tk()
                quickmessage.title("Confirm added user")
                quickmessage.iconbitmap(default=logo_file)
                quickframe = tk.Frame(quickmessage)
                quickframe.grid()

                tk.Label(quickmessage, text=str(confirm.get())).grid()

                def no():
                    quickmessage.destroy()

                def yes():
                    transaction = myDB.add_user(myuser, mypass)
                    tk.Label(quickmessage, text=str(transaction)).grid()
                    sleep(2)

                tk.Button(quickmessage, text='No/Exit', command=no).grid(row=3, column=0)
                tk.Button(quickmessage, text="Yes", command=yes).grid(row=3, column=1)

                quickmessage.mainloop()

            tk.Button(add, text="Add User", command=submit_add).grid()

            tk.Label(add, text="User to remove's name").grid(row=2)

            usertodel = tk.Entry(add)
            usertodel.grid(row=2, column=1)

            def submit_del():
                myuser = str(usertodel.get())

                confirm = tk.StringVar(root)
                confirm.set("Would you like to delete user: " + myuser + "?")

                quickmessage = tk.Tk()
                quickmessage.title("Confirm deletion of User")
                quickmessage.iconbitmap(default=logo_file)
                quickframe = tk.Frame(quickmessage)
                quickframe.grid()

                tk.Label(quickmessage, text=str(confirm.get())).grid()

                def no():
                    quickmessage.destroy()

                def yes():
                    transaction = myDB.delete_user(myDB.names[myuser])
                    tk.Label(quickmessage, text=str(transaction)).grid()
                    sleep(2)

                tk.Button(quickmessage, text='No/Exit', command=no).grid(row=3, column=0)
                tk.Button(quickmessage, text="Yes", command=yes).grid(row=3, column=1)

                quickmessage.mainloop()

            tk.Button(add, text="Delete User", command=submit_del).grid()


        tk.Button(root, text="Refresh", command=refresh_main).grid(row=0, column=0)

        leave = tk.Button(root, text='Exit', width=25, command=exit)
        leave.grid()

        checkout = tk.Button(root, text="Check out Book", width=25, command=check_out_window)
        checkout.grid()

        returnme = tk.Button(root, text="Return Book", width=25, command=return_window)
        returnme.grid()

        if myDB.USER.isteacher:
            adduser = tk.Button(root, text="Manage Users", width=25, command=add_user)
            adduser.grid()

        display_fines().grid(row=5)
        r0w = 6
        for line in display_books():
            line.grid(row=r0w)
            r0w += 1

        myDB.UpdateProgress()
        if loop.get():
            update_loop.start() # Start the infinite loop of constantly updating the progress in the background
        root.mainloop()

    connect = tk.Tk()
    connect.title("Connect to Database")
    connect.iconbitmap(default=logo_file)

    tk.Label(connect, text="Username ").grid(row=0)
    tk.Label(connect, text="Password ").grid(row=1)

    e1 = tk.Entry(connect)
    e2 = tk.Entry(connect)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)

    def submit_info():
        connected = myDB.connect(e1.get(), e2.get())
        status = connected[0]
        if status:
            sleep(1)
            open_main()
        elif not status:
            tk.Label(connect, text="Sorry, your Username/Password was not found. Please try again.").grid()
            e1.insert(0, "")
            e1.insert(0, "")


    quit = tk.Button(connect, text='Quit', command=connect.destroy).grid(row=3, column=0, sticky=tk.W, pady=4)
    submit = tk.Button(connect, text="Submit", command=submit_info).grid(row=3, column=1, sticky=tk.W, pady=4)

    connect.mainloop()