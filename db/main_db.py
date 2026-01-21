from config import path_db
from db import queries 
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.tasks_table)
    # cursor.execute('select * from tasks')
    conn.commit()
    conn.close()


def add_task(task):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(queries.insert_task, (task, date_now))
    conn.commit()
    
    task_id = cursor.lastrowid
    conn.close()
    return task_id, date_now


def update_task(task_id, new_task):
    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()
    cursor.execute(queries.update_task, (new_task, task_id))
    conn.commit()
    conn.close()
    