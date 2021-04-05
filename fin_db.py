from tkinter import *
from tkinter import ttk
import sqlite3


class Fin_Db:
    def __init__(self):
        pass

    def fin_db(self):
        global totalprofit
        global totalcost
        global balance
        root = Tk()

        totalprofit = StringVar()
        totalcost = StringVar()
        balance = StringVar()

        root.title("Melsons Stock Inventory Management System")
        root.geometry("700x800")
        Label(root, text="Melsons Stock Inventory Management System", fg="white",
              font="arial 24 bold", bg="black").place(x=5, y=10)

        titles = ('Item', 'Balance')
        findb = ttk.Treeview(root, columns=titles, show='headings', height=35)
        for title in titles:
            findb.heading(title, text=title)
            findb.grid(row=1, column=0, columnspan=2)
            findb.place(x=10, y=70)

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

        def financialdb():
            findb = Fin_Db()
            findb.fin_db()

        nav = Menu(root)
        root.config(menu=nav)

        file = Menu(nav)
        nav.add_cascade(label="File", menu=file)
        file.add_command(label="Open Current Stock", command=viewdb)
        file.add_command(label="Open Financial Record", command=financialdb)
        file.add_separator()
        file.add_command(label="Exit", command=root.destroy)

        edit = Menu(nav)
        nav.add_cascade(label="Edit", menu=edit)
        edit.add_command(label="Add New Item", command=addpage)
        edit.add_command(label="Update Current Stock", command=editpage)

        def rundb():  # Display Database
            global totalprofit
            global totalcost
            global balance
            for child in findb.get_children():  # Clear treeview
                findb.delete(child)
            con = sqlite3.connect('inventory.db')  # Connection
            cur = con.cursor()
            cur.execute('''SELECT * , oid FROM financial''')
            content = cur.fetchall()
            for child in content:
                if float(child[1]) > 0:  # If balance is positive
                    x = "Sell"  # Make x=sell for tag
                else:
                    x = "Purchase"
                findb.insert('', 'end', values=(
                    child[0], child[1]), tag=x)  # Insert into treeview with either purchase or sell tag
            con.close()
            colour_rows()  # Colour the rows depending on tag
            prof = 0.0
            cost = 0.0
            for child in findb.get_children():  # Looping thorugh rows to calculate total balance
                value = float(findb.item(child, 'values')[1])
                if value > 0:
                    prof = prof + value
                else:
                    cost = cost+value

            totalprofit.set(prof)
            totalcost.set(cost)
            sum = prof+cost
            balance.set(sum)

            profitlabel = Label(root, text=prof, font="arial 18 ", textvariable=prof)
            profitlabel.place(x=600, y=100)

            costlabel = Label(root, text=cost, font="arial 18 ", textvariable=cost)
            costlabel.place(x=600, y=150)

            balancelabel = Label(root, text=sum, font="arial 18 ", textvariable=balance)
            balancelabel.place(x=600, y=200)

            Label(root, text="Overall Revenue:", font="arial 18 ").place(x="440", y=100)
            Label(root, text="Overall Cost:", font="arial 18 ").place(x="460", y=150)
            Label(root, text="Profit:", font="arial 18 ").place(x="500", y=200)

        def colour_rows():
            findb.tag_configure("Purchase", background="#ffcccb")  # Adding colour
            findb.tag_configure("Sell", background="#90ee90")

        rundb()

        Button(root, text="Refresh", command=rundb).place(x=600, y=10)

        root.mainloop()
