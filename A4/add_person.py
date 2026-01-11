import tkinter as tk
from tkinter import messagebox
import psycopg2
import db
import re

def save_person():
    f_name = entry_fname.get().strip()
    l_name = entry_lname.get().strip()
    email = entry_email.get().strip().lower()

    if not f_name or not l_name or not email:
        messagebox.showwarning("Warning", "Please fill in all fields.")
        return
    if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", email):
        messagebox.showwarning("Warning", "Please enter a valid email address.")
        return

    conn = db.create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                    INSERT INTO public."Persons" ("fName", "lName", email)
                    VALUES (%s, %s, %s) \
                    """
            cursor.execute(query, (f_name, l_name, email))
            conn.commit()
            messagebox.showinfo("Success", f"Added {f_name} {l_name}!")
            entry_fname.delete(0, tk.END)
            entry_lname.delete(0, tk.END)
            entry_email.delete(0, tk.END)
        except psycopg2.IntegrityError:
            conn.rollback()
            messagebox.showerror("Error", "That email already exists!")
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Error: {e}")
        finally:
            conn.close()
    else:
        messagebox.showerror("Error", "Could not connect to the database.")

window = tk.Tk()
window.title("Add New Person")
window.geometry("300x250")

tk.Label(window, text="First Name:").pack(pady=5)
entry_fname = tk.Entry(window)
entry_fname.pack()

tk.Label(window, text="Last Name:").pack(pady=5)
entry_lname = tk.Entry(window)
entry_lname.pack()

tk.Label(window, text="Email:").pack(pady=5)
entry_email = tk.Entry(window)
entry_email.pack()

btn_save = tk.Button(window, text="Save Person", command=save_person)
btn_save.pack(pady=20)

window.mainloop()