# C-R-U-D

tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL
    )    
"""

# Create  - Создание записи
insert_task =  'INSERT INTO tasks (task, date) VALUES (?, ?)'

# Read  - Просмотр записей
select_task = 'SELECT id, task FROM tasks'

# Update  - Обновить запись
update_task = 'UPDATE tasks SET task = ? WHERE id = ?'

# Delete  - Удаление записи
delete_task = 'DELETE FROM tasks WHERE id = ?'