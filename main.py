from tkinter import *
from tkinter import messagebox
from pass_data import *
from random import randint, shuffle, choice
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def pass_generator():
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbol = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_letters + password_symbol + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    pass_e.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_e.get()
    email = email_e.get()
    password = pass_e.get()
    new_dict = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="Please don't leave any fields empty..")
    else:
        is_ok = messagebox.askokcancel(title="Data", message=f"This is the entered data:\nWebsite:{website}"
                                                             f"\nEmail:{email}\n Password:{password} ")
        if is_ok:
            try:
                with open("Data_Manager.json", "r") as file_data:
                    k_data = json.load(file_data)
            except FileNotFoundError:
                with open("Data_Manager.json", "w") as file_data:
                    json.dump(new_dict, file_data, indent=4)
            else:
                k_data.update(new_dict)
                with open("Data_Manager.json", "w") as file_data:
                    json.dump(k_data, file_data, indent=4)
            finally:
                website_e.delete(0, END)
                pass_e.delete(0, END)


# ---------------------------- Search Data ------------------------------- #

def find_data():
    website = website_e.get()
    try:
        with open("Data_Manager.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="File doesn't exist..")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Error", message=f"Email:{email} \n Password:{password}")
        else:
            messagebox.showinfo(title="Error", message="No data related to the website found")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password generator")
window.config(padx=50, pady=50)
image = Canvas(height=200, width=200)
lock_img = PhotoImage(file="logo.png")
image.create_image(100, 100, image=lock_img)
image.grid(row=0, column=1)
# Labels
website_l = Label(text="Website:")
website_l.grid(row=1, column=0)
email_l = Label(text="Email/Username:")
email_l.grid(row=2, column=0)
pass_l = Label(text="Password:")
pass_l.grid(row=3, column=0)
# Entry
website_e = Entry(width=24)
website_e.grid(row=1, column=1)
website_e.focus_set()
email_e = Entry(width=43)
email_e.insert(0, "krishna.pisal@gmail.com")
email_e.grid(row=2, column=1, columnspan=2)
pass_e = Entry(width=25)
pass_e.grid(row=3, column=1)

# Buttons
search_btn = Button(text="Search", width=10, command=find_data)
search_btn.grid(row=1, column=2)
gen_btn = Button(text="Generate Password", command=pass_generator)
gen_btn.grid(row=3, column=2, sticky="w")
add_btn = Button(text="Add", width=36, command=save_data)
add_btn.grid(row=4, column=1, columnspan=2)

window.mainloop()
