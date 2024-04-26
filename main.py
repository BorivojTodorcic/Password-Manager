import tkinter as tk
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- CONSTANTS ----------------------------------- #

IMG_PATH = "./lock.png"
DATA_PATH_JSON = "./passwords.json"
EMAIL = "test_email@hotmail.com"
LABEL_FONT = ("Arial", 12, "bold")
FONT = ("Arial", 12,)
L_BLUE = "#219EBC"
D_BLUE = "#023047"
GOLD = "#FFB703"

# ---------------------------- SEARCH PASSWORDS ---------------------------- #

def search_passwords():
    """Searches the .json file containing the login details for the specified website name"""

    website = web_entry.get()

    try:
        with open(DATA_PATH_JSON, "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        # Returns message box if the .json file does not exist
        tk.messagebox.showerror(message="No passwords saved.")

    else:
        # Checks if the requested website name is in the file
        if website in data:
            # Returns login credentials if the website is in the file
            website_dict = data[website]
            req_email = website_dict["email"]
            req_password = website_dict["password"]
            tk.messagebox.showinfo(message=f"Website:\n{website}\n\nEmail:\n{req_email}\n\nPassword:\n{req_password}")

        else:
            # Returns error message if the login credentials are not found
            tk.messagebox.showerror(message=f"No passwords saved for {website}.")

# ---------------------------- PASSWORD GENERATOR -------------------------- #

def generate_password():
    """Generates a random password and inserts it into the password data field"""

    # Deletes any pre-existing data in the password data field
    pass_entry.delete(0, tk.END)

    # Generates a random password containing alphanumerical characters and special characters
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # Randomly selects a number for the respecitve character group
    nr_letters = randint(6, 8)
    nr_symbols = randint(1, 4)
    nr_numbers = randint(1, 4)

    # Randomly selects the characters from the lists
    password_list = []
    password_list.extend([choice(letters) for char in range(nr_letters)])
    password_list.extend([choice(symbols) for char in range(nr_symbols)])
    password_list.extend([choice(numbers) for char in range(nr_numbers)])

    # Shuffles the password order
    shuffle(password_list)
    password = "".join(password_list)

    # Saves the generated password to the clipboard and inserts it into the entry widget
    pyperclip.copy(password)
    pass_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():
    """Saves the current login credentials to the .json file"""

    # Retrieves the data from the respective data entry fields
    website = web_entry.get()
    email = email_entry.get()
    password = pass_entry.get()
    
    message = f"Are these details correct?\n\nWebsite:\n{website}\n\nEmail:\n{email}\n\nPassword:\n{password}"
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) != 0 and len(email) != 0 and len(password) != 0:

        # Asks the user to confirm they are happy with the details
        confirm = tk.messagebox.askokcancel(message=message)

        if confirm:
            # Stores the data in a .json file
            try:
                with open(DATA_PATH_JSON, "r") as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                # Creates a new file if the .json file does not exist
                # Saves the data to the new .json file
                with open(DATA_PATH_JSON, "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                # If file exists, this updates data from the file with the new data
                data.update(new_data)

                # Saves the new data to the .json file
                with open(DATA_PATH_JSON, "w") as data_file:
                    json.dump(data, data_file, indent=4)

            finally:
                # Clears the data from the entry boxes regardless of the outcome
                web_entry.delete(0, tk.END)
                pass_entry.delete(0, tk.END)

    else:
        # Presents the user with a warning message if any field is left empty
        tk.messagebox.showwarning(message="Please do not leave any fields empty!")

# ---------------------------- UI SETUP ------------------------------------ #

# Creates new tkinter window
window = tk.Tk()
window.title("Password Manager")
window.config(padx=60, pady=60, bg=L_BLUE)

canvas = tk.Canvas(width=200, height=200, bg=L_BLUE, highlightthickness=0)
lock_img = tk.PhotoImage(file=IMG_PATH)
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=0, column=1)

# Labels
web_label = tk.Label(text="Website:", bg=L_BLUE, fg=D_BLUE, font=LABEL_FONT)
web_label.grid(row=1, column=0, sticky=tk.W)

email_label = tk.Label(text="Email / Username:", bg=L_BLUE, fg=D_BLUE, font=LABEL_FONT)
email_label.grid(row=2, column=0, sticky=tk.W)

pass_label = tk.Label(text="Password:", bg=L_BLUE, fg=D_BLUE, font=LABEL_FONT)
pass_label.grid(row=3, column=0, sticky=tk.W)


# Entries
web_entry = tk.Entry(bg="white", fg="black", highlightthickness=0, insertbackground="black")
web_entry.config(font=FONT)
web_entry.grid(row=1, column=1, sticky=tk.W + tk.E, padx=2.5, pady=2.5)
web_entry.focus()

email_entry = tk.Entry(bg="white", fg="black", highlightthickness=0, insertbackground="black")
email_entry.config(font=FONT)
email_entry.insert(0, string=EMAIL)
email_entry.grid(row=2, column=1, columnspan=2, sticky=tk.W + tk.E, padx=2.5, pady=2.5)

pass_entry = tk.Entry(bg="white", fg="black", highlightthickness=0, insertbackground="black")
pass_entry.config(font=FONT, width=15)
pass_entry.grid(row=3, column=1, sticky=tk.W + tk.E, padx=2.5, pady=2.5)


# Buttons
search_button = tk.Button(text="Search", font=FONT, highlightbackground=L_BLUE, command=search_passwords, width=17)
search_button.grid(row=1, column=2, sticky= tk.E, padx=2.5, pady=2.5)

pass_gen_button = tk.Button(text="Generate Password", font=FONT, highlightbackground=L_BLUE, command=generate_password, width=17)
pass_gen_button.grid(row=3, column=2, sticky= tk.E, padx=2.5, pady=2.5)

add_button = tk.Button(text="Save Credentials", font=FONT, highlightbackground=L_BLUE, command=save_data)
add_button.grid(row=4, column=1, columnspan=2, sticky= tk.W + tk.E, padx=2.5, pady=2.5)


window.mainloop()
