from tkinter import *
import sqlite3

root = Tk()
root.title("Melsons Stock Inventory Management System")
root.geometry("1200x800")

# creation of database
con = sqlite3.connect('inventory.db')

# Creation of cursor
cur = con.cursor()

# creeat database table

cur.execute("""CREATE TABLE stock(
    Item Name text,
    Cost of Good real,
    Quantity integer,
    Total Price real,
    Sale price real

)""")

# commit changes
con.commit()

# terminate connection
con.close()


con = sqlite3.connect('inventory.db')
cur = con.cursor()
cur.execute("""CREATE TABLE financial(
    Item Name text,
    Balance real
)""")
con.commit()
con.close()


root.mainloop()
