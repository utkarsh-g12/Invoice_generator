import tkinter
from tkinter import ttk
import datetime
from docxtpl import DocxTemplate
from tkinter import messagebox
invoice_list = []
window = tkinter.Tk()

window.title("Invoice Generator Software")


def mobile_checker(p):
    if p.isdigit() and len(p) <= 10 or p == "":
        return True
    return False


callback = window.register(mobile_checker)


def clear_fields():
    qty_entry.delete(0, tkinter.END)
    qty_entry.insert(0, "1")
    description_entry.delete(0, tkinter.END)
    unit_price_entry.delete(0, tkinter.END)
    unit_price_entry.insert(0, "1")


def add_item():
    qty = int(qty_entry.get())
    desc = description_entry.get()
    unit_price = int(unit_price_entry.get())
    total = qty*unit_price
    invoice_item = [qty, desc, unit_price, total]
    tree.insert('', 0, values=invoice_item)
    clear_fields()
    qty_entry.focus_set()
    invoice_list.append(invoice_item)


def new_invoice():
    first_name_entry.delete(0, tkinter.END)
    last_name_entry.delete(0, tkinter.END)
    phone_entry.delete(0, tkinter.END)
    tree.delete(*tree.get_children())
    clear_fields()
    first_name_entry.focus_set()
    invoice_list.clear()


def generate_invoice():
    doc = DocxTemplate("INVOICE.docx")
    date = datetime.datetime.now()
    name = first_name_entry.get()+" "+last_name_entry.get()
    phone = phone_entry.get()
    subtotal = sum(item[3] for item in invoice_list)
    salestax = 0.1
    total = subtotal*(1-salestax)
    doc.render({"Date": date,
                "Name": name,
                "Phone": phone,
                "invoice_list": invoice_list,
                "subtotal": subtotal,
                "salestax": str(salestax*100)+"%",
                "total": total})
    doc_name = "new_invoice" + name + datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".docx"
    doc.save(doc_name)
    messagebox.showinfo("Invoice", "Invoice Generated Successfully")
    new_invoice()


frame = tkinter.Frame(window)
frame.pack(padx=30, pady=10)

first_name_lable = tkinter.Label(frame, text="First Name")
first_name_lable.grid(row=0, column=0, pady=10)

first_name_entry = tkinter.Entry(frame)
first_name_entry.grid(row=1, column=0, pady=10)

last_name_lable = tkinter.Label(frame, text="Last Name")
last_name_lable.grid(row=0, column=1, pady=10)

last_name_entry = tkinter.Entry(frame)
last_name_entry.grid(row=1, column=1, pady=10)


phone_lable = tkinter.Label(frame, text="Phone")
phone_lable.grid(row=0, column=2, pady=10)

phone_entry = tkinter.Entry(frame)
phone_entry.grid(row=1, column=2, pady=10)
phone_entry.configure(validate="key", validatecommand=(callback, "%P"))

qty_lable = tkinter.Label(frame, text="Qty")
qty_lable.grid(row=2, column=0, pady=10)

qty_entry = tkinter.Spinbox(frame, from_=1, to=100)
qty_entry.grid(row=3, column=0, pady=10)

description_lable = tkinter.Label(frame, text="Discription")
description_lable.grid(row=2, column=1, pady=10)

description_entry = tkinter.Entry(frame)
description_entry.grid(row=3, column=1, pady=10)

unit_price_lable = tkinter.Label(frame, text="Unit Price")
unit_price_lable.grid(row=2, column=2, pady=10)

unit_price_entry = tkinter.Spinbox(frame, from_=1, to=100)
unit_price_entry.grid(row=3, column=2, pady=10)

add_item_button = tkinter.Button(frame, text="Add Item", command=add_item)
add_item_button.grid(row=4, column=2, pady=10)

columns = ('qty', 'desc', 'price', 'total')
tree = ttk.Treeview(frame, columns=columns, show="headings")
tree.heading('qty', text='Qty')
tree.heading('desc', text='Description')
tree.heading('price', text='Price')
tree.heading('total', text='Total')
tree.grid(row=5, column=0, columnspan=3, pady=10)

gen_invoice_button = tkinter.Button(frame, text="Generate Invoice", command=generate_invoice)
gen_invoice_button.grid(row=6, column=0, columnspan=3, sticky="news", pady=10)

new_invoice_button = tkinter.Button(frame, text="New Invoice", command=new_invoice)
new_invoice_button.grid(row=7, column=0, columnspan=3, sticky="news", pady=10)
window.mainloop()
