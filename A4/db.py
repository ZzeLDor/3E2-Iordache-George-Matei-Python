import psycopg2


def start_connection():
    try:
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="1234", host="localhost", port="5432")
        print("Connected.")
        return conn
    except Exception as e:
        print("Not connected:")
        print(e)
        return None


connection = start_connection()
cursor = connection.cursor()
try:
    cursor.execute('SELECT count(*) FROM public."Persons"')
    cursor.execute('SELECT count(*) FROM public."Meetings"')
except Exception as e:
    print("Error reading tables:")
    print(e)
else:
    print("Initialisation done. All tables read successfully.")

cursor.close()
connection.close()
