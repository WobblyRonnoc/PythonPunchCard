import mysql.connector
from datetime import datetime
import sys
import configparser

# Read the database connection details from the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

db_config = {
    'host': config.get('database', 'host'),
    'user': config.get('database', 'user'),
    'password': config.get('database', 'password'),
    'database': config.get('database', 'database')
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


def clock_in():
    time_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_query = 'INSERT INTO clock (time_in) VALUES (%s)'
    cursor.execute(insert_query, (time_in,))
    conn.commit()
    print("Clocked in at:", time_in)


def clock_out():
    time_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_query = 'UPDATE clock SET time_out=%s WHERE id=(SELECT MAX(id) FROM clock)'
    cursor.execute(update_query, (time_out,))
    conn.commit()
    print("Clocked out at:", time_out)


# Get the clock-in or clock-out choice from command-line argument
if len(sys.argv) != 2:
    print("Invalid number of arguments. Usage: python clock.py [in|out]")
    sys.exit(1)

choice = sys.argv[1]

if choice == 'in':
    clock_in()
elif choice == 'out':
    clock_out()
else:
    print("Invalid choice!")

# Close the database connection
conn.close()
