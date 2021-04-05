from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox


class Edit_data:
    def __init__(self):
        pass

    def edit(self):
        root = Tk()
        root.title("Melsons Stock Inventory Management System")
        root.geometry("1200x800")
        Label(root, text="Melsons Stock Inventory Management System", fg="white",
              font="arial 24 bold", bg="black").place(x=5, y=10)
        Label(root, text="Update Stock of Item", font="arial 24 bold").place(x=5, y=50)
        Label(root, text="Primary Key of Good", font="arial 18").place(x=10, y=90)
        Label(root, text="Restock Quantity", font="arial 18").place(x=40, y=250)
        Label(root, text="Quantity Sold", font="arial 18").place(x=260, y=250)
        Label(root, text="Quantity Discarded", font="arial 18").place(x=430, y=250)
        global chosen

        def viewdb():
            from view_db import View_Db
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

        chosen = StringVar()

        e1 = Entry(root)
        e1.place(x=15, y=300)

        e2 = Entry(root)
        e2.place(x=215, y=300)

        e3 = Entry(root)
        e3.place(x=415, y=300)

        titles = ('Item', 'Cost of Good', 'Quantity', 'Total Cost', 'Sale Price')

        displayoldrec = ttk.Treeview(root, columns=titles, show='headings', height=1)

        for title in titles:
            displayoldrec.heading(title, text=title)
            displayoldrec.grid(row=1, column=0, columnspan=2)
            displayoldrec.place(x=10, y=200)

        def updateoptions():
            con = sqlite3.connect('inventory.db')  # Connection to db
            cur = con.cursor()
            cur.execute('''SELECT oid FROM stock''')
            primarykeys = cur.fetchall()
            con.close()
            chosen.set("Choose One")
            droplist = OptionMenu(root, chosen, *primarykeys)  # Setting up drop down list
            droplist.config(width=10)
            droplist.place(x=25, y=125)

        def findrecord():
            for child in displayoldrec.get_children():
                displayoldrec.delete(child)
            global id
            id = str(chosen.get()[1])
            con = sqlite3.connect('inventory.db')
            cur = con.cursor()
            cur.execute("SELECT* FROM stock WHERE oid = " + id)
            global record
            record = cur.fetchall()
            con.close()
            displayoldrec.insert("", "end", values=(record[0]))

        def editrecord():
            con = sqlite3.connect('inventory.db')  # connection to db
            cur = con.cursor()
            additional = int(e1.get())  # Entry values inputed by client
            sold = int(e2.get())
            thrown = e3.get()
            x = IntVar()
            for child in displayoldrec.get_children():
                x = displayoldrec.item(child)["values"][2]
            newquantity = int(additional) + x
            y = IntVar()
            y = newquantity-float(sold)-int(thrown)
            if y < 0:  # Checks if quantity sold/discarded is greater than available stock
                messagebox.showinfo(
                    "", "Quantity sold/discarded exceeds avaailable quantity please try again.")
                return
            if sold > 0:  # If there is some quantity sold, this calculates profit made and adds to financial database
                for child in displayoldrec.get_children():
                    sp = float(displayoldrec.item(child)["values"][4])  # gets sale price
                profit = sold * sp
                con = sqlite3.connect('inventory.db')
                cur = con.cursor()
                for child in displayoldrec.get_children():
                    cur.execute("INSERT INTO financial VALUES (:itemname,  :itemtotal)",  # Inserts into financial data
                                {
                                    'itemname': str(displayoldrec.item(child, 'values')[0]),
                                    'itemtotal': profit
                                })
            if additional > 0:  # Checks if any quanitty is bought so the total cost cna be calculated and shown in the financial db
                for child in displayoldrec.get_children():
                    cog = float(displayoldrec.item(child)["values"][1])
                tc = additional * cog

                for child in displayoldrec.get_children():
                    cur.execute("INSERT INTO financial VALUES (:itemname,  :itemtotal)",
                                {
                                    'itemname': str(displayoldrec.item(child, 'values')[0]),
                                    'itemtotal': -tc
                                })
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            for child in displayoldrec.get_children():
                displayoldrec.delete(child)
            update = """Update stock set quantity =? where oid = ?"""
            input = (y, id)
            cur.execute(update, input)
            con.commit()
            con.close()

        def deleterecord():
            con = sqlite3.connect('inventory.db')
            cur = con.cursor()
            cur.execute("SELECT* FROM stock WHERE oid = " + id)
            for child in displayoldrec.get_children():
                x = displayoldrec.item(child)["values"][2]
            if x != 0:  # Checks if quantity of good is equal to 0
                messagebox.showinfo(
                    "", "Item can't be deleted as there is still some stock. Please either report sales of the time or discard the remaining quantity before.")
                return
            cur.execute("DELETE from stock WHERE oid =" + id)  # Deletes item
            con.commit()
            con.close()
            for child in displayoldrec.get_children():
                displayoldrec.delete(child)

        updateoptions()

        Button(root, text="Update", command=findrecord, height=2, width=10).place(x=200, y=120)
        Button(root, text="Edit", command=editrecord, height=2, width=10).place(x=645, y=290)
        Button(root, text="Delete Item", command=deleterecord,
               height=2, width=12).place(x=750, y=290)

        root.mainloop()
