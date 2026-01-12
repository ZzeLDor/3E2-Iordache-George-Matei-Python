import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import psycopg2
import db
import re

def save_person():
    f_name = entry_fname.get().strip()
    l_name = entry_lname.get().strip()
    email = entry_email.get().strip().lower()

    if not f_name or not l_name or not email:
        Messagebox.show_warning("Please fill in all fields.", "Warning")
        return
    if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email):
        Messagebox.show_warning("Please enter a valid email address.", "Warning")
        return

    conn = db.start_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                    INSERT INTO public."Persons" ("fName", "lName", email)
                    VALUES (%s, %s, %s) 
                    """
            cursor.execute(query, (f_name, l_name, email))
            conn.commit()
            Messagebox.show_info("Added {f_name} {l_name}!", f"Success")
            entry_fname.delete(0, END)
            entry_lname.delete(0, END)
            entry_email.delete(0, END)
        except psycopg2.IntegrityError:
            conn.rollback()
            Messagebox.show_error("That email already exists!", "Error")
        except Exception as e:
            conn.rollback()
            Messagebox.show_error(f"Error: {e}", "Database Error")
        finally:
            conn.close()
    else:
        Messagebox.show_error("Could not connect to the database.", "Error")

def start():
    window.mainloop()

window = ttk.Window(themename="flatly")
window.title("Add New Person")
window.geometry("300x410+%d+%d" % (window.winfo_screenwidth() / 2 - 150, window.winfo_screenheight() / 2 - 205))

container = ttk.Frame(window, padding=20)
container.pack(fill=BOTH, expand=True)

ttk.Label(container, text="First Name:").pack(pady=(0, 5), anchor="w")
entry_fname = ttk.Entry(container)
entry_fname.pack(fill=X, pady=(0, 10))

ttk.Label(container, text="Last Name:").pack(pady=(0, 5), anchor="w")
entry_lname = ttk.Entry(container)
entry_lname.pack(fill=X, pady=(0, 10))

ttk.Label(container, text="Email:").pack(pady=(0, 5), anchor="w")
entry_email = ttk.Entry(container)
entry_email.pack(fill=X, pady=(0, 10))

btn_save = ttk.Button(container, text="Save Person", command=save_person, bootstyle=SUCCESS)
btn_save.pack(pady=20, fill=X)

start()