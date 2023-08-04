import sys
import configparser
import datetime
import mysql.connector


# current time as a datetime object
def get_current_time():
    return datetime.datetime.now()


# current time as a formatted string 
def format_time(time_obj):
    return time_obj.strftime("%Y-%m-%d %H:%M:%S")


def punch_in(db_cursor):
    start_time = get_current_time()
    insert_query = 'INSERT INTO work_hours (date,punch_in) VALUES (CURRENT_DATE,%s)'
    db_cursor.execute(insert_query, (start_time,))
    print(f"Punched in at {format_time(start_time)}")


def punch_out(db_cursor):
    end_time = get_current_time()
    update_query = '''
        UPDATE work_hours AS c1
        JOIN (SELECT MAX(id) AS max_id FROM work_hours) AS c2
        SET c1.punch_out = %s
        WHERE c1.id = c2.max_id
    '''
    db_cursor.execute(update_query, (end_time,))
    print(f"Punched out at {format_time(end_time)}")


def view_hours(db_cursor):
    select_query = "SELECT * FROM time_sheet"
    db_cursor.execute(select_query)
    for row in db_cursor.fetchall():
        punch_in_time = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S")
        punch_out_time = datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S") if row[3] else None
        print(f"Punch In: {format_time(punch_in_time)}, Punch Out: {format_time(punch_out_time)}")


def undo_punch_out(db_cursor):
    update_query = '''
        UPDATE work_hours AS c1
        JOIN (SELECT MAX(id) AS max_id FROM work_hours WHERE punch_out IS NOT NULL) AS c2
        SET c1.punch_out = NULL
        WHERE c1.id = c2.max_id
    '''
    db_cursor.execute(update_query)
    print("Last punch-out undone.")


def undo_punch_in(db_cursor):
    delete_query = '''
        DELETE FROM work_hours
        WHERE id = (SELECT MAX(id) FROM work_hours)
    '''
    db_cursor.execute(delete_query)


# get the amount of time worked so far


# check if there is a punch-in without a punch-out
def is_punched_in(db_cursor):
    select_query = "SELECT * FROM work_hours where punch_out is NULL"
    db_cursor.execute(select_query)
    return db_cursor.fetchone() is not None


def get_hours_today(db_cursor):
    select_query = "SELECT * FROM daily_hours WHERE day = CURRENT_DATE"
    db_cursor.execute(select_query)
    row = db_cursor.fetchone()
    return row[1] if row else 0


def get_hours_this_week(db_cursor):
    select_query = "SELECT * FROM weekly_hours WHERE week_start = DATE_SUB(current_date, INTERVAL (DAYOFWEEK(current_date) - 1) DAY)"
    db_cursor.execute(select_query)
    row = db_cursor.fetchone()
    return row[1] if row else 0


def get_punch_time(db_cursor):
    select_query = "SELECT CONCAT(TIMESTAMPDIFF(HOUR, punch_in_time, NOW()), ':', TIMESTAMPDIFF(MINUTE, punch_in_time, NOW())) AS time_since_punch_in FROM time_sheet WHERE punch_out_time IS NULL; "
    db_cursor.execute(select_query)
    row = db_cursor.fetchone()
    return row[0] if row else 0


# --------------------------------------------------------------
# -----------------------INTERACTIVE MODE-----------------------
# --------------------------------------------------------------

# interactive mode for viewing hours (use argument 'view' to view hours)
def main(db_cursor):
    print("Time Tracking Application".center(50, '-'))
    if is_punched_in(db_cursor):
        print("out: Punch out\n"
              "status: Display current punch status and hours worked today\n"
              "week: Display hours worked this week\n"
              "exit: Exit the program\n")
    else:
        print("in: Punch in\n"
              "status: Display current punch status and hours worked today\n"
              "week: Display hours worked this week\n"
              "exit: Exit the program\n")
    while True:
        command = input("\nEnter command: ").lower()
        if command == "exit":
            print("Exiting...")
            break

        elif command == "help":
            print("\tCommands:\n"
                  "\tin: punch in\n"
                  "\tout: punch out\n"
                  "\tstatus: Display current punch status and hours worked today\n"
                  "\tweek: Display hours worked this week\n")

        elif command == "status":
            if is_punched_in(db_cursor):
                # time since punch in
                print(f"\tCurrent Session: {get_punch_time(db_cursor)}\n"
                      f"\tHours Today: {get_hours_today(db_cursor)}\n"
                      f"\tCurrent Time: {format_time(get_current_time())}\n")
            else:
                print(f"\tPunched out\n"
                      f"\tCurrent Time: {format_time(get_current_time())}\n"
                      f"\tHours Today: {get_hours_today(db_cursor)}")

        elif command == "week":
            print(f"\tHours worked this week: {get_hours_this_week(db_cursor)}")

        elif command == "in":
            punch_in(db_cursor)
            conn.commit()
        elif command == "out":
            punch_out(db_cursor)
            conn.commit()


# ------------------------------------------------------------
# ----------------------- MAIN PROGRAM -----------------------
# ------------------------------------------------------------


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

# Get the work_hours-in or work_hours-out choice from command-line argument
if len(sys.argv) != 2:
    print("Invalid number of arguments. Usage: python work_hours.py [in|out]")
    sys.exit(1)

choice = sys.argv[1]

if choice == 'in':
    punch_in(cursor)
    conn.commit()  # Commit the changes after each punch-in/punch-out operation
elif choice == 'out':
    punch_out(cursor)
    conn.commit()  # Commit the changes after each punch-in/punch-out operation
elif choice == '-i':
    main(cursor)
else:
    print("Invalid choice!")

# Close the database connection
conn.close()
