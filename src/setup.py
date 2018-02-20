from cx_Freeze import setup, Executable

import os

os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\Python35-32\\tcl\\tk8.6"

include_files = ['Logo.ico', 'BookIT_Instructions.pdf', 'Books.csv', 'Users.csv', 'Logo.png', ]

setup(
    name = "BookIT Library DataBase Organizer",
    version = "0.0.1",
    console=['__main__.py'],
    author = "Tejas Shah",
    author_email = "tejas.shah1950@gmail.com",
    description = ("FBLA 2018 Coding and Programming Challenge. A library database used to track student and teachers, check out/return "
                   "books, Fine users, and otherwise maintain a library."),
    keywords = "library, database, organization, FBLA",
    executables=[Executable('BookIT.py', base='Win32GUI')],
    options={'build_exe':{'include_files': include_files}}
)