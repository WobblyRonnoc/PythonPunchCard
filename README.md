# PythonPunchCard
Keep track of hours using punch-in/out timestamps and insert to an SQL DB
<hr>

## Setup:


Create the database:
```MySQL
CREATE DATABASE my_time_sheet;
USE my_time_sheet;

CREATE TABLE Entries (
    id INT UNIQUE PRIMARY KEY AUTO_INCREMENT,
    start_time DATETIME,
    end_time DATETIME
);
```
<br>

Create a file `config.ini` in the same directory as `clock.py`. Fill in your connection info here.

```ini
[database]
host = localhost
user = your_username
password = your_password
database = your_database
port = port_number
```
<hr>

## How to use:
Pass `clock.py` the argument `in` or `out` to insert a timestamp into the DB.

> C:\> Python clock.py in
> 
>Clocked in at: 2023-07-14 11:25:07


> C:\> Python clock.py out
> 
> Clocked out at: 2023-07-14 4:45:28

## Alternative Use:
included `.bat` files will run `clock.py` `in` / `out`.

> Note: at the moment they echo the timestamp in a terminal window then pause. 


<br>
<hr>

## Known Issues:
* Clocking out only updates the most recent clock in row
* lack of error handling
* package imports are not mentioned yet
