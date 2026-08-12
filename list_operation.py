#!/usr/bin/env python3


from cmath import e
filename = "diary_log_txt"


def log_diary_entry(filename):
    filename = "diary_log_txt"
    print("add your input which you want to write")
    user_text = input("add your comments > ")
    with open(filename, "a") as file:
        file.write(user_text + "\n")
    print("saved successfully")


def readfile(filename):
    print("read file history")

    try:
        with open(filename, "r") as file:
            print(file.read())
    except Exception as e:
        print({e})


log_diary_entry(filename)
readfile(filename)
