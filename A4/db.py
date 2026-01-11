import psycopg2

def create_connection():
    try:
        conn = psycopg2.connect(dbname="postgres",user="postgres",password="1234",host="localhost",port="5432")
        print("Connected.")
        return conn
    except Exception as e:
        print("Not connected: ")
        print(e)
        return None

connection = create_connection()
cursor = connection.cursor()
try:
    cursor.execute('SELECT count(*) FROM public."Persons"')
    print("Persons checked. Number of entries:", cursor.fetchone()[0])
    cursor.execute('SELECT count(*) FROM public."Meetings"')
    print("Meetings checked. Number of entries:", cursor.fetchone()[0])
except Exception as e:
    print("Error reading tables:")
    print(e)

cursor.close()
connection.close()
print("Connection closed.")