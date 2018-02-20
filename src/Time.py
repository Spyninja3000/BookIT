import time as t


def gettime():
    day = ((float(t.localtime()[2]) * 60) * 60) * 24
    hour = (float(t.localtime()[3]) * 60) * 60
    min = float(t.localtime()[4]) * 60
    sec = float(t.localtime()[5])
    return day + hour + min + sec

# 1 * 60 * 60 * 24 == 86400

# One day is 86400 seconds, so the gettime() method should be updated to subtract
# a day from all books of all users every 86400 seconds in LibraryDB's UpdateProgress method