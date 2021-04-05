from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from add_page import Add_page
import sqlite3


class Login:
    def __init__(self):
        root = Tk()
        root.title("Melsons Stock Inventory Management System")
        root.geometry("300x200")
        Label(root, text="Login Page", font="arial 24 bold").place(x=60, y=20)
        Label(root, text="Username:", font="arial 15").place(x=60, y=60)
        Label(root, text="Password:", font="arial 15").place(x=60, y=90)

        username = Entry(root, width=12)
        username.place(x=160, y=65)

        password = Entry(root, width=12, show="*")
        password.place(x=160, y=95)

        def login():
            if (username.get() == "admin" and password.get() == "123"):
                root.destroy()
                Add = Add_page()
                Add.add()

            else:
                messagebox.showinfo("", "Incorrect Username and Password")

        Button(root, text="Submit", command=login, height=3, width=13).place(x=92, y=130)

        root.mainloop()


if __name__ == "__main__":
    Login = Login()
