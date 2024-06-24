import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ttkbootstrap import Style
from view_write_wordpass import run_password_manager
from image_icon_paths import icon_path, image_path, wordpass, myname

def login(event=None):
    entered_username = username_entry.get()
    entered_password = password_entry.get()
    
    # Check if both username and password match
    if entered_username == myname and entered_password == wordpass:
        root.destroy()  # Close the login window
        open_main_application()
    else:
        login_status_label.config(text="Invalid Username or Password", fg="red")

def open_main_application():
    if __name__ == "__main__":
        run_password_manager()

def cancel():
    root.destroy()

# Create the main Tkinter window for login
root = tk.Tk()
root.title("Login")
root.iconbitmap(icon_path)
root.geometry("235x250")

# Create a style object with 'litera' theme
style = Style(theme='litera')
# Configure the style for TButton
style.configure('TButton', font=('Segoe UI', 10, 'bold'))

# Load and display image
add_path = "logo.png"
full_path = image_path + add_path
image = Image.open(full_path)
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

# Username label and entry
username_label = tk.Label(root, text="Username:")
username_label.grid(row=1, column=0, padx=10, pady=5)
username_entry = tk.Entry(root)
username_entry.grid(row=1, column=1, padx=10, pady=5)
username_entry.focus()  # Set focus to username entry by default

# Password label and entry
password_label = tk.Label(root, text="Password:")
password_label.grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=5)

# Bind Enter key to login function
root.bind('<Return>', login)

# Login button
login_button = ttk.Button(root, text="Login", command=login, style="TButton.Outline")
login_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="WE")

# Cancel button
cancel_button = ttk.Button(root, text="Cancel", command=cancel, style="TButton.Outline")
cancel_button.grid(row=4, column=0, columnspan=2, padx=10, pady=1, sticky="WE")

# Label to show login status
login_status_label = tk.Label(root, text="", fg="red")
login_status_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
