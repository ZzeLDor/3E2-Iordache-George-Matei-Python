import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import db
import tkinter as tk
from datetime import datetime, time

person_list = []

def load_persons():
    conn = db.start_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT id, "fName", "lName" FROM public."Persons"')
            rows = cursor.fetchall()

            person_list.clear()
            listbox_participants.delete(0, tk.END)

            for row in rows:
                p_id = row[0]
                full_name = f"{row[1]} {row[2]}"
                person_list.append((p_id, full_name))
                listbox_participants.insert(tk.END, full_name)
        except Exception as e:
            print(f"Error loading persons: {e}")
        finally:
            conn.close()


def save_meeting():
    title = entry_title.get().strip()
    desc = entry_desc.get().strip()
    try:
        date_str_start = cal_start.entry.get()
        date_start = datetime.strptime(date_str_start, '%Y-%m-%d').date()

        date_str_end = cal_end.entry.get()
        date_end = datetime.strptime(date_str_end, '%Y-%m-%d').date()

        time_start = time(int(spin_start_h.get()), int(spin_start_m.get()))
        time_end = time(int(spin_end_h.get()), int(spin_end_m.get()))

        dt_start = datetime.combine(date_start, time_start)
        dt_end = datetime.combine(date_end, time_end)
    except ValueError:
        Messagebox.show_error("Invalid Date or Time format.", "Format Error")
        return
    if not title:
        Messagebox.show_warning("Please enter a Title.", "Missing Data")
        return
    if dt_start > dt_end:
        Messagebox.show_error("End time must be AFTER Start time.", "Time Error")
        return
    selected_indices = listbox_participants.curselection()
    if not selected_indices:
        Messagebox.show_warning("Please select at least one participant.", "Warning")
        return

    participant_ids = [person_list[i][0] for i in selected_indices]
    conn = db.start_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                    INSERT INTO public."Meetings" (title, description, start, "end", participants)
                    VALUES (%s, %s, %s, %s, %s)
                    """
            cursor.execute(query, (title, desc, dt_start, dt_end, participant_ids))
            conn.commit()
            Messagebox.show_info("Meeting scheduled successfully!", "Success")
            entry_title.delete(0, tk.END)
            entry_desc.delete(0, tk.END)
            listbox_participants.selection_clear(0, tk.END)

        except Exception as e:
            conn.rollback()
            Messagebox.show_error(f"Error: {e}", "Database Error")
        finally:
            conn.close()
    else:
        Messagebox.show_error("Could not connect to the database.", "Error")


window = ttk.Window(themename="flatly")
window.title("Schedule Meeting")
window.geometry("530x845+%d+%d" % (window.winfo_screenwidth() / 2 - 265, window.winfo_screenheight() / 2 - 422))

main_frame = ttk.Frame(window, padding=20)
main_frame.pack(fill=BOTH, expand=True)

ttk.Label(main_frame, text="Meeting Title:", font=("Helvetica", 10, "bold")).pack(anchor="w")
entry_title = ttk.Entry(main_frame)
entry_title.pack(fill=X, pady=(0, 10))

ttk.Label(main_frame, text="Description:", font=("Helvetica", 10, "bold")).pack(anchor="w")
entry_desc = ttk.Entry(main_frame)
entry_desc.pack(fill=X, pady=(0, 15))

frame_start_group = ttk.Labelframe(main_frame, text="Start Date & Time", padding=10, bootstyle="info")
frame_start_group.pack(fill=X, pady=5)

cal_start = ttk.DateEntry(frame_start_group, dateformat='%Y-%m-%d', bootstyle="info")
cal_start.pack(side=LEFT, padx=(0, 10))

spin_start_h = ttk.Spinbox(frame_start_group, from_=0, to=23, width=3, format="%02.0f")
spin_start_h.set(10)
spin_start_h.pack(side=LEFT)
ttk.Label(frame_start_group, text=":").pack(side=LEFT, padx=2)
spin_start_m = ttk.Spinbox(frame_start_group, from_=0, to=59, width=3, format="%02.0f")
spin_start_m.set(00)
spin_start_m.pack(side=LEFT)

frame_end_group = ttk.Labelframe(main_frame, text="End Date & Time", padding=10, bootstyle="warning")
frame_end_group.pack(fill=X, pady=10)

cal_end = ttk.DateEntry(frame_end_group, dateformat='%Y-%m-%d', bootstyle="warning")
cal_end.pack(side=LEFT, padx=(0, 10))

spin_end_h = ttk.Spinbox(frame_end_group, from_=0, to=23, width=3, format="%02.0f")
spin_end_h.set(10)
spin_end_h.pack(side=LEFT)
ttk.Label(frame_end_group, text=":").pack(side=LEFT, padx=2)
spin_end_m = ttk.Spinbox(frame_end_group, from_=0, to=59, width=3, format="%02.0f")
spin_end_m.set(00)
spin_end_m.pack(side=LEFT)

ttk.Label(main_frame, text="Select Participants:", font=("Helvetica", 10, "bold")).pack(
    anchor="w", pady=(15, 5))

listbox_participants = tk.Listbox(main_frame, selectmode=tk.MULTIPLE, height=8, relief=FLAT, borderwidth=1)
listbox_participants.pack(fill=X)

btn_save = ttk.Button(main_frame, text="Schedule Meeting", command=save_meeting, bootstyle="success", width=20)
btn_save.pack(pady=25)

load_persons()
window.mainloop()
