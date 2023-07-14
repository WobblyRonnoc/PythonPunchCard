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
    'database': config.get('database', 'database'),
    'port': config.get('database', 'port')
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()


def clock_in():
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    insert_query = 'INSERT INTO clock (start_time) VALUES (%s)'
    cursor.execute(insert_query, (start_time,))
    conn.commit()
    print("Clocked in at:", start_time)


def clock_out():
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    update_query = '''
        UPDATE clock AS c1
        JOIN (SELECT MAX(id) AS max_id FROM clock) AS c2
        SET c1.end_time = %s
        WHERE c1.id = c2.max_id
    '''
    cursor.execute(update_query, (end_time,))
    conn.commit()
    print("Clocked out at:", end_time)


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
