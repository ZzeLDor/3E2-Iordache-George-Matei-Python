"""
ICS export helper for the Meeting Scheduler.

Exports meetings for a given date to an .ics file.
"""
from ics import Calendar, Event

import db


def exportc(date_str, filepath):
    """
    Export meetings on *date_str* to *filepath* as an .ics calendar.

    Accesses "Meetings" for meetings on the given date, builds an
    ics.Calendar with Event objects, writes the serialized calendar to
    *filepath*, and returns (True, message) on success or (False, error).
    """
    conn = db.start_connection()
    if not conn:
        return False, "Database connection failed"
    try:
        cursor = conn.cursor()
        query = """
                SELECT title, description, start, "end"
                FROM public."Meetings"
                WHERE start::date = %s \
                """
        cursor.execute(query, (date_str,))
        rows = cursor.fetchall()

        if not rows:
            return False, "No meetings found for this date"

        c = Calendar()
        for row in rows:
            e = Event()
            e.name = row[0]
            e.description = row[1] if row[1] else ""
            e.begin = row[2]
            e.end = row[3]
            c.events.add(e)

        with open(filepath, 'w') as f:
            f.write(c.serialize())

        return True, f"Successfully exported this date's meetings"

    except Exception as e:
        return False, str(e)
    finally:
        conn.close()
