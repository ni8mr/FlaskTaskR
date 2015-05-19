# project/db_creating.py

import sqlite3
from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as conn:

    # getting a cursor object for using to execute SQL commands
    c = conn.cursor()

    # creating the table
    c.execute("""CREATE TABLE tasks
             (task_id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT NOT NULL, due_date TEXT NOT NULL,
             priority INTEGER NOT NULL, status INTEGER NOT NULL)""")

    # inserting dummy data into the table
    c.execute('INSERT INTO tasks(name, due_date, priority, status)'
              'VALUES("Finish this tutorial", "05/25/2015", 10, 1)')

    c.execute('INSERT INTO tasks(name, due_date, priority, status)'
              'VALUES("Finish reading about web developement with python", "05/25/2015", 10, 1)'
              )

    
