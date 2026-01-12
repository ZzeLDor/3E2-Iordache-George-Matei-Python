"""
ICS import helper for the Meeting Scheduler.

Parses an .ics file and inserts events into "Meetings".
"""
from ics import Calendar

import db


def importc(filepath):
    """
    Import events from an .ics file into the database.

    Parses the file at *filepath*, converts events to meeting rows, and
    inserts them into "Meetings". Returns (True, message) on
    success or (False, error_message) on failure.
    """
    conn = db.start_connection()
    if not conn:
        return False, "Database connection failed"
    count = 0
    try:
        with open(filepath, 'r') as f:
            c = Calendar(f.read())

        cursor = conn.cursor()
        for event in c.events:
            title = event.name
            desc = event.description if event.description else "Imported"
            dt_start = event.begin.datetime
            dt_end = event.end.datetime

            query = """
                    INSERT INTO public."Meetings" (title, description, start, "end", participants)
                    VALUES (%s, %s, %s, %s, %s) \
                    """
            cursor.execute(query, (title, desc, dt_start, dt_end, []))
            count += 1

        conn.commit()
        return True, f"Successfully imported {count} meetings"

    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        conn.close()
