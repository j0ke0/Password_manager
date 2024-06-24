import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from image_icon_paths import basedata, icon_path
from ttkbootstrap import Style

def run_password_manager():
    def get_database_path():
        return basedata  # Replace with actual database path

    def display_data(tree):
        try:
            # Connect to SQLite database
            db_path = get_database_path()
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            # Fetch all data from passwords table
            c.execute("SELECT * FROM passwords")
            rows = c.fetchall()

            # Clear existing treeview data
            for row in tree.get_children():
                tree.delete(row)

            # Insert fetched data into treeview
            for row in rows:
                # Display password as '***' instead of actual password
                row_data = list(row)
                row_data[2] = '*****'  # Assuming password is in the third column (index 2)
                tree.insert('', tk.END, values=row_data)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching data: {e}", icon='error')

        finally:
            # Close connection
            if conn:
                conn.close()

    def add_data_window():
        add_window = tk.Toplevel(root)
        add_window.title("Add Accounts")
        add_window.iconbitmap(icon_path)
        add_window.grab_set()  # Grab the focus for this window

        style = Style(theme='litera')
        style.configure('TButton', font=('Segoe UI', 10, 'bold'))
        add_window.geometry("230x175")

        bold_font = ('TkDefaultFont', 10, 'bold')

        tk.Label(add_window, text="Username:", font=bold_font).grid(row=0, column=0, padx=5, pady=5, sticky='e')
        tk.Label(add_window, text="Password:", font=bold_font).grid(row=1, column=0, padx=5, pady=5, sticky='e')
        tk.Label(add_window, text="Website:", font=bold_font).grid(row=2, column=0, padx=5, pady=5, sticky='e')
        tk.Label(add_window, text="Remarks:", font=bold_font).grid(row=3, column=0, padx=5, pady=5, sticky='e')

        username_entry = tk.Entry(add_window)
        username_entry.grid(row=0, column=1, padx=10, pady=5)
        password_entry = tk.Entry(add_window, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=5)
        website_entry = tk.Entry(add_window)
        website_entry.grid(row=2, column=1, padx=10, pady=5)
        remarks_entry = tk.Entry(add_window)
        remarks_entry.grid(row=3, column=1, padx=10, pady=5)

        def submit_data():
            username = username_entry.get()
            password = password_entry.get()
            website = website_entry.get()
            remarks = remarks_entry.get()

            if username and password and website and remarks:
                # Check password length
                if len(password) < 3:
                    messagebox.showerror("Error", "Password must be at least 3 characters long.")
                    return

                # Exchange first and last characters of password if length is >= 2
                if len(password) >= 2:
                    password = password[-1] + password[1:-1] + password[0]

                try:
                    conn = sqlite3.connect(basedata)
                    c = conn.cursor()
                    c.execute("INSERT INTO passwords (username, hashed_password, website, remarks) VALUES (?, ?, ?, ?)",
                              (username, password, website, remarks))
                    conn.commit()
                    messagebox.showinfo("Success", "Entry added successfully.", icon='info')
                    display_data(tree)
                    add_window.destroy()
                except sqlite3.Error as e:
                    messagebox.showerror("Error", f"Error adding data: {e}")
                finally:
                    if conn:
                        conn.close()
            else:
                messagebox.showerror("Error", "Please fill in all fields.")

        submit_button = ttk.Button(add_window, text="Submit", command=submit_data, style='Outline.TButton', width=9)
        submit_button.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        cancel_button = ttk.Button(add_window, text="Cancel", command=add_window.destroy, style='Outline.TButton', width=9)
        cancel_button.grid(row=4, column=1, padx=12, pady=5, sticky="e")

    def edit_data():
        try:
            selected_item = tree.selection()[0]  # Get the selected item in the treeview
            item_values = tree.item(selected_item)['values']  # Get the values of the selected item

            # Create an edit window
            edit_window = tk.Toplevel(root)
            edit_window.title("View & Edit Entry")
            edit_window.iconbitmap(icon_path)
            edit_window.geometry("230x175")

            bold_font = ('TkDefaultFont', 10, 'bold')

            tk.Label(edit_window, text="Username:", font=bold_font).grid(row=0, column=0, padx=5, pady=5, sticky='e')
            tk.Label(edit_window, text="Password:", font=bold_font).grid(row=1, column=0, padx=5, pady=5, sticky='e')
            tk.Label(edit_window, text="Website:", font=bold_font).grid(row=2, column=0, padx=5, pady=5, sticky='e')
            tk.Label(edit_window, text="Remarks:", font=bold_font).grid(row=3, column=0, padx=5, pady=5, sticky='e')

            username_entry = tk.Entry(edit_window)
            username_entry.grid(row=0, column=1, padx=5, pady=5)
            username_entry.insert(0, item_values[1])  # Populate with current username

            password_entry = tk.Entry(edit_window, show="*")
            password_entry.grid(row=1, column=1, padx=5, pady=5)
            password_entry.insert(0, item_values[2])  # Populate with current password
            password_entry.config(state='readonly')  # Make the password field read-only

            website_entry = tk.Entry(edit_window)
            website_entry.grid(row=2, column=1, padx=5, pady=5)
            website_entry.insert(0, item_values[3])  # Populate with current website

            remarks_entry = tk.Entry(edit_window)
            remarks_entry.grid(row=3, column=1, padx=5, pady=5)
            remarks_entry.insert(0, item_values[4])  # Populate with current remarks

            def update_data():
                new_username = username_entry.get()
                new_password = password_entry.get()
                new_website = website_entry.get()
                new_remarks = remarks_entry.get()

                if new_username and new_password and new_website and new_remarks:
                    try:
                        conn = sqlite3.connect(basedata)
                        c = conn.cursor()
                        c.execute("UPDATE passwords SET username=?, hashed_password=?, website=?, remarks=? WHERE ID=?",
                                  (new_username, new_password, new_website, new_remarks, item_values[0]))
                        conn.commit()
                        messagebox.showinfo("Success", "Entry updated successfully.")
                        display_data(tree)
                        edit_window.destroy()
                    except sqlite3.Error as e:
                        messagebox.showerror("Error", f"Error updating data: {e}")
                    finally:
                        if conn:
                            conn.close()
                else:
                    messagebox.showerror("Error", "Please fill in all fields.")

            submit_button = ttk.Button(edit_window, text="Update", command=update_data, style='Outline.TButton', width=9)
            submit_button.grid(row=4, column=0, padx=10, pady=10, sticky="e")

            cancel_button = ttk.Button(edit_window, text="Cancel", command=edit_window.destroy, style='Outline.TButton', width=9)
            cancel_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")

        except IndexError:
            messagebox.showerror("Error", "Please select an item to edit.")

    def delete_data():
        try:
            selected_item = tree.selection()[0]  # Get the selected item in the treeview
            item_values = tree.item(selected_item)['values']  # Get the values of the selected item

            # Display confirmation dialog
            confirm = messagebox.askokcancel("Confirm Deletion", f"Are you sure you want to delete ID {item_values[0]}?")
            if confirm:
                # Connect to SQLite database
                db_path = get_database_path()
                conn = sqlite3.connect(db_path)
                c = conn.cursor()

                # Delete item from database
                c.execute("DELETE FROM passwords WHERE ID=?", (item_values[0],))
                conn.commit()

                # Close connection
                conn.close()

                # Remove item from treeview
                tree.delete(selected_item)
                messagebox.showinfo("Deleted", f"Deleted ID {item_values[0]} successfully.")

        except IndexError:
            messagebox.showerror("Error", "Please select an item to delete.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")

    def view_wordpased():
        try:
            selected_item = tree.selection()[0]  # Get the selected item in the treeview
            item_values = tree.item(selected_item)['values']  # Get the values of the selected item

            # Fetch the full password from the database
            db_path = get_database_path()
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute("SELECT hashed_password FROM passwords WHERE ID=?", (item_values[0],))
            fetched_password = c.fetchone()[0]
            conn.close()

            # Exchange the first and last characters
            if len(fetched_password) >= 2:
                exchanged_password = fetched_password[-1] + fetched_password[1:-1] + fetched_password[0]
            else:
                exchanged_password = fetched_password  # If password length is less than 2, no exchange

            # Display the exchanged password in a Toplevel window with a Text widget
            view_password_window = tk.Toplevel(root)
            view_password_window.title("View Password")

            view_password_window.iconbitmap(icon_path)

            style = Style(theme='litera')
            # Configure the style for TButton
            style.configure('TButton', font=('Segoe UI', 10, 'bold'))

            # Create a Text widget to display the password
            password_text = tk.Text(view_password_window, height=1, width=30)
            password_text.insert(tk.END, exchanged_password)
            password_text.pack(padx=10, pady=10)
            password_text.config(state=tk.DISABLED)  # Disable editing of the text widget

            # Function to copy password to clipboard
            def copy_to_clipboard():
                root.clipboard_clear()
                root.clipboard_append(exchanged_password)
                root.update()

            # Button to copy password to clipboard
            copy_button = ttk.Button(view_password_window, text="Copy to Clipboard", command=copy_to_clipboard, style='Outline.TButton')
            copy_button.pack(pady=10)

        except IndexError:
            messagebox.showerror("Error", "Please select an item to view the password.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error fetching password: {e}")

    def exit_app():
        root.destroy()  # Close the Tkinter application

    # Create tkinter window
    root = tk.Tk()
    root.title("Password Manager")
    root.iconbitmap(icon_path)

    style = Style(theme='litera')
    # Configure the style for TButton
    style.configure('TButton', font=('Segoe UI', 10, 'bold'))

    # Create Treeview widget
    tree = ttk.Treeview(root, columns=('ID', 'Username', 'Password', 'Website', 'Remarks'), show='headings')

    # Define columns and column headings
    columns = ('ID', 'Username', 'Password', 'Website', 'Remarks')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Segoe UI', 9, 'bold'))

    # Display the Treeview using grid
    tree.grid(row=0, column=0, columnspan=4, padx=10, pady=2)

    # Load data into the Treeview
    display_data(tree)

    # Create frame for buttons
    button_frame = tk.Frame(root)
    button_frame.grid(row=1, column=0, columnspan=4, padx=10, pady=2)

    add_button = ttk.Button(button_frame, text="Add Entries", width=15, command=add_data_window, style='Outline.TButton')
    add_button.grid(row=0, column=0, padx=12, pady=3)

    edit_button = ttk.Button(button_frame, text="View or Edit", width=15, command=edit_data, style='Outline.TButton')
    edit_button.grid(row=0, column=2, padx=12, pady=3)

    delete_button = ttk.Button(button_frame, text="Delete", width=15, command=delete_data, style='Outline.TButton')
    delete_button.grid(row=0, column=1, padx=12, pady=3)

    wordpass_button = ttk.Button(button_frame, text="View Password", width=15, command=view_wordpased, style='Outline.TButton')
    wordpass_button.grid(row=0, column=3, padx=12, pady=3)

    exit_button = ttk.Button(button_frame, text="Exit", width=15, command=exit_app, style='Outline.TButton')
    exit_button.grid(row=0, column=4, padx=12, pady=3)

    # Start the tkinter main loop
    root.mainloop()
