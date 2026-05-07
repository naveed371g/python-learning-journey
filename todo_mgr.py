#!/usr/bin/env python

def todo_mgr():
    todo = []

    while True:
        print("1. Add task")
        print("2. remove task")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            todo.append(input("Enter task: "))
            print(todo)
        elif choice == "2":
            todo.pop(int(input("Enter task number to remove: "))-1)
            print(todo)
        elif choice == "3":
            break
        else:
            print("Invalid choice" )

todo_mgr()



