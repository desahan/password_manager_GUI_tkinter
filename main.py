from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
               's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
               'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, password)

    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website_data = website_input.get()
    email_data = email_input.get()
    password_data = password_input.get()
    new_data = {
        website_data: {
            "Email": email_data,
            "Password": password_data,
        }
    }

    if len(website_data) == 0 or len(password_data) == 0:
        empty_field_ok = messagebox.askokcancel(title="Empty fields",
                                             message="You left some fields empty, are you sure you want to proceed.")
        if empty_field_ok:
            messagebox.askokcancel(title=website_data, message=f"These are the details entered: \n"
                                                       f"Email: {email_data} \n"
                                                       f"Password: {password_data} \n"
                                                       f"Is it ok to save?")

    else:
        messagebox.askokcancel(title=website_data, message=f"These are the details entered: \n"
                                                                   f"Email: {email_data} \n"
                                                                   f"Password: {password_data} \n"
                                                                   f"Is it ok to save?")
        try:
            with open("data.json", "r") as file:
                # Read old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", "w") as file:
                json.dump(new_data, file, indent=4)
        else:
            # Update data
            data.update(new_data)
            # Save data
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)
            website_input.focus()

# ---------------------------- SEARCH FUNCTION ------------------------------- #
def search_website():
    website_search = website_input.get()
    try:
        with open("data.json", "r") as sites:
            dictionary = json.load(sites)
            site_info = dictionary[website_search]
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    except KeyError:
        messagebox.showinfo(title="Error", message="No details for the website exist")
    else:
        email_from_search = site_info['Email']
        password_from_search = site_info['Password']
        messagebox.showinfo(title=website_search, message=f"Email: {email_from_search}\n"
                                                             f"Password: {password_from_search}")

# ---------------------------- UI SETUP ------------------------------- #
screen = Tk()
screen.title("Password Manager")
screen.config(pady=50, padx=50)

canvas = Canvas(width=200, height=200)
photo = PhotoImage(file="logo.png")
canvas.create_image(135, 100, image=photo)
canvas.grid(column=1, row=0)

# Labels
website_text = Label(text="Website:")
website_text.grid(column=0, row=1)
email_text = Label(text="Email/Username:")
email_text.grid(column=0, row=2)
password_text = Label(text="Password:", padx=0, pady=0)
password_text.grid(column=0, row=3)

# Entry
website_input = Entry(width=33)
website_input.grid(column=1, row=1)
website_input.focus()
email_input = Entry(width=57)
email_input.grid(column=1, row=2, columnspan=2)
email_input.insert(index=0, string="danielle.sahan.24@gmail.com")
password_input = Entry(width=33)
password_input.grid(column=1, row=3)

# Button
generate = Button(text="Generate Password", width=19, command=generate_password)
generate.grid(column=2, row=3)
add = Button(text="Add", width=49, command=save_data)
add.grid(column=1, row=4, columnspan=2)
search = Button(text="Search", width=19, command=search_website)
search.grid(column=2, row=1)

screen.mainloop()
