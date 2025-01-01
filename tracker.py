import csv
from tkinter import ttk, messagebox
from tkinter import *
from datetime import datetime


def append_data(filename):
    selected_amount = var_amount.get()
    selected_trans = var_type_transaction.get()
    selected_reason = var_reason.get()
    selected_desc = var_desc.get()

    if not (selected_amount and selected_trans and selected_reason and selected_desc):
        messagebox.showerror("Empty Fields", "Please fill in all the fields.")
        return
    if not selected_amount.isdigit():
        messagebox.showerror("Invalid Amount", "Please fill in a valid amount.")
        return
    if selected_amount == "0" or int(selected_amount) < 0:
        messagebox.showerror("Invalid amount", "Please fill in valid amount.")
        return

    final_data = {
        "Amount": selected_amount,
        "Transaction": selected_trans,
        "Reason": selected_reason,
        "Description": selected_desc,
        "Date": date_today,
        "Time": formatted_time
    }
    
    with open(filename, "a", newline="") as file_w:
        csvwriter = csv.DictWriter(file_w, fieldnames=["Amount", "Transaction", "Reason", "Description", "Date", "Time"])
        file_w.seek(0, 2)
        if file_w.tell() == 0:
            csvwriter.writeheader()
        csvwriter.writerow(final_data)
    
    messagebox.showinfo("Transaction Noted", f"""Amount: ₹{selected_amount}
Transaction: {selected_trans}
Reason: {selected_reason}
Date & Time: {date_today} & {formatted_time}
""")
    transaction_data.append(final_data)
    get_total_transaction()


def read_data(filename):
    data = []
    with open(filename, "r") as file_r:
        csvreader = csv.DictReader(file_r)
        for row in csvreader:
            data.append(row)
    return data


def get_total_transaction():
    amount = 0
    for data in transaction_data:
        if data["Transaction"] == "Income":
            amount += int(data["Amount"])
        elif data["Transaction"] == "Expense":
            amount -= int(data["Amount"])
        else:
            amount = 0
    label_total_transaction.config(text=f"Total Amount: ₹{amount}")


def get_reason(event):
    if var_type_transaction.get() == "Expense":
        combo_reason["values"] = sorted(["Entertainment", "Stationery", "Grocery/Utility", "Transportation", "Health/Medical"]) + ["Miscellaneous"]
    else:
        combo_reason["values"] = sorted(["Pocket Money", "Savings"])


file_name = "money_track.csv"
transaction_data = ""
try:
    transaction_data = read_data(file_name)
except FileNotFoundError as e:
    messagebox.showwarning("File not found", """money_track.csv not found.
Creating a new one.""")
    with open('money_track.csv', 'w') as file:
        pass

win = Tk()
win.title("Money Tracker by KadakWNL")

date_today = datetime.today().date()
now = datetime.now()
formatted_time = f"{now.hour:02}:{now.minute:02}:{int(now.second):02}"

var_amount = StringVar()
var_type_transaction = StringVar()
var_reason = StringVar()
var_desc = StringVar()

label_head = Label(win, text="Money Tracker Application", font=("Roboto", 12, "bold"))
label_head.grid(row=0, column=0, columnspan=2)

label_date = Label(win, text=date_today)
label_date.grid(row=1, column=0, columnspan=2)

label_amount = Label(win, text="Enter Amount: ")
label_amount.grid(row=2, column=0, sticky="w", padx=2, pady=2)
entry_amount = Entry(win, textvariable=var_amount, width=23)
entry_amount.grid(row=2, column=1, sticky="e", padx=10, pady=2)

label_transaction = Label(win, text="Type of transaction: ")
label_transaction.grid(row=3, column=0, sticky="w", padx=2, pady=2)
combo_transaction = ttk.Combobox(win, values=["Expense", "Income"], textvariable=var_type_transaction, state="readonly")
combo_transaction.grid(row=3, column=1, sticky="e", padx=10, pady=2)
combo_transaction.bind("<<ComboboxSelected>>", get_reason)

label_reason = Label(win, text="Reason :")
label_reason.grid(row=4, column=0, sticky="w", padx=2, pady=2)
combo_reason = ttk.Combobox(win, values=[], state="readonly", textvariable=var_reason)
combo_reason.grid(row=4, column=1, sticky="e", padx=10, pady=2)

label_desc = Label(win, text="Enter the description: ")
label_desc.grid(row=5, column=0, sticky="w", padx=2, pady=2)
entry_desc = Entry(win, textvariable=var_desc, width=23)
entry_desc.grid(row=5, column=1, sticky="e", padx=10, pady=2)

label_total_transaction = Label(win, text="Total Transaction: ₹0")
label_total_transaction.grid(row=6, column=0, columnspan=2)
get_total_transaction()

button_submit = Button(win, text="Submit", command=lambda: append_data(file_name))
button_submit.grid(row=7, column=0, columnspan=2, pady=5)

win.mainloop()