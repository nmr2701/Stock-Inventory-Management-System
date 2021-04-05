from tkinter import *
from tkinter import ttk
import sqlite3


class Add_page:
    def __init__(self):
        pass

    def add(self):
        root = Tk()
        root.title("Melsons Stock Inventory Management System")
        root.geometry("1200x800")
        global g1
        global g2
        global g3
        global g4
        global saleprice
        global total
        global totalq
        global itemname
        global itemtotal

        def viewdb():  # View Curreent Stock
            from view_db import View_Db
            view = View_Db()
            view.view()

        def editpage():  # Edit Current Stock
            from edit_data import Edit_data
            edit = Edit_data()
            edit.edit()

        def addpage():  # Add New Items
            Add = Add_page()
            Add.add()

        def findb():  # Open Financial Record
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

        total = StringVar()
        totalq = IntVar()

        titles = ('Item', 'Cost of Good', 'Quantity', 'Total Cost', 'Sale Price')

        Label(root, text="Melsons Stock Inventory Management System", fg="white",
              font="arial 24 bold", bg="black").place(x=5, y=10)
        Label(root, text="Add New Item", font="arial 24 bold").place(x=5, y=50)
        Label(root, text="Name of Good", font="arial 18").place(x=35, y=90)
        Label(root, text="Cost of Good", font="arial 18").place(x=250, y=90)
        Label(root, text="Quantity", font="arial 18").place(x=470, y=90)
        Label(root, text="Sale Price", font="arial 18").place(x=660, y=90)
        Label(root, text="Total Value:", font="arial 18 bold").place(x=650, y=10)
        Label(root, text="Total Number of Goods:", font="arial 18 bold").place(x=650, y=50)

        g1 = Entry(root)
        g1.place(x=10, y=125)

        g2 = Entry(root)
        g2.place(x=210, y=125)

        g3 = Entry(root)
        g3.place(x=410, y=125)

        g4 = Entry(root)
        g4.place(x=610, y=125)

        tempview = ttk.Treeview(root, columns=titles, show='headings', height=20)  # Define Treeview

        def Add():  # Add New Item to treeview
            itemtotal = 0
            itemname = g1.get()  # Get Data from entry boxes
            price = float(g2.get())
            quantity = int(g3.get())
            saleprice = float(g4.get())
            itemtotal = float(price * quantity)
            tempview.insert("", "end", values=(itemname, price, quantity,
                                               itemtotal, saleprice))  # Insert into treeview
            totvalue = 0.0
            totquantity = 0
            for child in tempview.get_children():
                totvalue += float(tempview.item(child, 'values')[3])  # Calculating Incoming Value
                # Calculating Incoming Quantity
                totquantity += float(tempview.item(child, 'values')[2])
            total.set(totvalue)  # For Incoming Value
            totalq.set(totquantity)  # For Incoming Quantity
            g1.delete(0, END)  # Clear Entry Boxes
            g2.delete(0, END)
            g3.delete(0, END)
            g4.delete(0, END)
            return itemtotal

        def confirm():  # Add Items from treeview to stock and affect the financial record
            con = sqlite3.connect('inventory.db')  # connection established
            cur = con.cursor()
            for child in tempview.get_children():  # Looped for each row in treeview
                cur.execute("INSERT INTO stock VALUES (:itemname, :price, :quantity, :itemtotal, :saleprice)",  # Match Headings
                            {
                                # Definining inputs
                                'itemname': str(tempview.item(child, 'values')[0]),
                                'price': float(tempview.item(child, 'values')[1]),
                                'quantity': int(tempview.item(child, 'values')[2]),
                                'itemtotal': float(tempview.item(child, 'values')[3]),
                                'saleprice': float(tempview.item(child, 'values')[4])
                            })

            con.commit()  # commit changes to database
            con.close()
            con = sqlite3.connect('inventory.db')
            cur = con.cursor()
            for child in tempview.get_children():
                cur.execute("INSERT INTO financial VALUES (:itemname,  :itemtotal)",  # Repeat for financial
                            {
                                'itemname': str(tempview.item(child, 'values')[0]),
                                # negative for cost
                                'itemtotal': -float(tempview.item(child, 'values')[3])
                            })

            con.commit()
            con.close()
            for child in tempview.get_children():  # clear treeview
                tempview.delete(child)

        def delete():
            temp = tempview.selection()
            for child in temp:
                tempview.delete(child)
            totvalue = 0.0
            totquantity = 0
            for child in tempview.get_children():
                totvalue += float(tempview.item(child, 'values')[3])
                totquantity += float(tempview.item(child, 'values')[2])
            total.set(totvalue)
            totalq.set(totquantity)

        for title in titles:
            tempview.heading(title, text=title)
            tempview.grid(row=1, column=0, columnspan=2)
            tempview.place(x=10, y=300)

        incoming_value = Label(root, text="", font="arial 18 bold", textvariable=total)
        incoming_value.place(x=760, y=10)

        incoming_quantity = Label(root, text="", font="arial 18 bold", textvariable=totalq)
        incoming_quantity.place(x=860, y=50)

        Button(root, text="Add", command=Add, height=2, width=10).place(x=10, y=220)
        Button(root, text="Delete Selected", command=delete, height=3, width=12).place(x=170, y=220)
        Button(root, text="Confirm", command=confirm, height=3, width=12).place(x=320, y=220)

        root.mainloop()
