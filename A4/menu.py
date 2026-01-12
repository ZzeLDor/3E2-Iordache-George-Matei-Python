import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import DateEntry
from ttkbootstrap.dialogs import Messagebox
import db
import sys
import subprocess

def get_participant_names(conn, participant_ids):
    if not participant_ids:
        return "None"

    try:
        cursor = conn.cursor()
        query = 'SELECT "fName", "lName" FROM public."Persons" WHERE id = ANY(%s)'
        cursor.execute(query, (participant_ids,))
        rows = cursor.fetchall()

        names = [f"{r[0]} {r[1]}" for r in rows]
        return ", ".join(names)
    except Exception:
        return "Error loading names"

def load_meetings():
    selected_date_str = date_picker.entry.get()
    for item in tree.get_children():
        tree.delete(item)

    conn = db.start_connection()
    if conn:
        try:
            cursor = conn.cursor()

            query = """
                    SELECT id, title, start, "end", participants
                    FROM public."Meetings"
                    WHERE start::date = %s
                    ORDER BY start ASC \
                    """
            cursor.execute(query, (selected_date_str,))
            rows = cursor.fetchall()

            if not rows:
                lbl_status.config(text="No meetings found for this day.", bootstyle="warning")
                return

            for row in rows:
                m_title = row[1]
                m_start = row[2].strftime("%H:%M")
                m_end = row[3].strftime("%H:%M")
                p_ids = row[4]

                p_names = get_participant_names(conn, p_ids)

                tree.insert("", "end", values=(m_start, m_end, m_title, p_names))

            status_text = "Found %d meeting" % len(rows)
            if len(rows) > 1:
                status_text += "s"
            status_text += " for this day."
            lbl_status.config(text=status_text, bootstyle="success")

        except Exception as e:
            Messagebox.show_error(f"Error: {e}","Error")
        finally:
            conn.close()


def open_add_person():
    subprocess.Popen([sys.executable, "add_person.py"])


def open_schedule():
    subprocess.Popen([sys.executable, "schedule_meeting.py"])

def start():
    load_meetings()
    window.mainloop()


window = ttk.Window(themename="flatly")
window.title("Meeting Scheduler - Main Menu")
window.geometry("960x600+%d+%d" % (window.winfo_screenwidth() / 2 - 480, window.winfo_screenheight() / 2 - 300))

frame_top = ttk.Frame(window, padding=10)
frame_top.pack(fill=X)

ttk.Label(frame_top, text="Meeting Scheduler", font=("Helvetica", 18, "bold")).pack(side=LEFT)

btn_add = ttk.Button(frame_top, text="+ Add Person", bootstyle="info", command=open_add_person)
btn_add.pack(side=RIGHT, padx=5)

btn_sched = ttk.Button(frame_top, text="+ Schedule Meeting", bootstyle="success", command=open_schedule)
btn_sched.pack(side=RIGHT, padx=5)

ttk.Separator(window).pack(fill=X, pady=5)

frame_date = ttk.Frame(window, padding=10)
frame_date.pack(fill=X)

ttk.Label(frame_date, text="Select Date to View:").pack(side=LEFT, padx=5)
date_picker = DateEntry(frame_date, dateformat="%Y-%m-%d", width=15)
date_picker.pack(side=LEFT, padx=5)

btn_show = ttk.Button(frame_date, text="Show Meetings", command=load_meetings, bootstyle="primary")
btn_show.pack(side=LEFT, padx=10)

lbl_status = ttk.Label(frame_date, text="Ready", bootstyle="secondary")
lbl_status.pack(side=LEFT, padx=20)

frame_table = ttk.Frame(window, padding=10)
frame_table.pack(fill=BOTH, expand=True)

cols = ("start", "end", "title", "participants")
tree = ttk.Treeview(frame_table, columns=cols, show="headings", height=15)

tree.heading("start", text="Start")
tree.column("start", width=80)

tree.heading("end", text="End")
tree.column("end", width=80)

tree.heading("title", text="Meeting Title")
tree.column("title", width=200)

tree.heading("participants", text="Participants")
tree.column("participants", width=300)

scrollbar = ttk.Scrollbar(frame_table, orient=VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)
tree.pack(side=LEFT, fill=BOTH, expand=True)

start()