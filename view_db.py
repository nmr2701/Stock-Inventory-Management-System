from tkinter import *
from tkinter import ttk
import sqlite3


class View_Db:
    def __init__(self):
        pass

    def view(self):
        root = Tk()
        root.title("Melsons Stock Inventory Management System")
        root.geometry("1250x800")
        Label(root, text="Melsons Stock Inventory Management System", fg="white",
              font="arial 24 bold", bg="black").place(x=5, y=10)

        titles = ('Primary Key', 'Item', 'Cost of Good', 'Quantity', 'Total Cost', 'Sale Price')
        database = ttk.Treeview(root, columns=titles, show='headings', height=35)

        def viewdb():
            view = View_Db()
            view.view()

        def editpage():
            from edit_data import Edit_data
            edit = Edit_data()
            edit.edit()

        def addpage():
            from add_page import Add_page
            Add = Add_page()
            Add.add()

        def findb():
            from fin_db import Fin_Db
            findb = Fin_Db()
            findb.fin_db()

        nav = Menu(root)
        root.config(menu=nav)

        file = Menu(nav)
        nav.add_cascade(label="File", menu=file)
        file.add_command(label="Open Current Stock", command=viewdb)
        file.add_command(label="Open Financial Record", command=findb)
        file.add_separator()
        file.add_command(label="Exit", command=root.destroy)

        edit = Menu(nav)
        nav.add_cascade(label="Edit", menu=edit)
        edit.add_command(label="Add New Item", command=addpage)
        edit.add_command(label="Update Current Stock", command=editpage)

        for title in titles:
            database.heading(title, text=title)
            database.grid(row=1, column=0, columnspan=2)
            database.place(x=10, y=70)

        def rundb():
            for child in database.get_children():
                database.delete(child)
            con = sqlite3.connect('inventory.db')
            cur = con.cursor()
            cur.execute('''SELECT * , oid FROM stock''')
            content = cur.fetchall()
            for child in content:
                database.insert('', 'end', values=(
                    child[5], child[0], child[1], child[2], child[3], child[4]))  # Input data into treeview from database... child 5 is ID
            con.close()

        rundb()
        Button(root, text="Refresh", command=rundb).place(x=600, y=10)
        root.mainloop()
