from db import main_db
import flet as ft 

def main(page: ft.Page):
    # print('Hello Flet')
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column(spacing=25)

    filter_type = 'all'


    def load_tasks():
        task_list.controls.clear()
        for task_id, task_text, completed in main_db.get_task(filter_type):
            task_list.controls.append(view_tasks(task_id=task_id, task_text=task_text, completed=completed))

    def view_tasks(task_id, task_text, completed=None):
        task_field = ft.TextField(read_only=True, value=task_text, expand=True)

        checkbox = ft.Checkbox(value=bool(completed), on_change=lambda e: toggle_task(task_id=task_id, is_completed=e.control.value))

        def enable_edit(_):
            if task_field.read_only == True:
                task_field.read_only = False
            else:
                task_field.read_only = True

        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        def delete_task(_):
            main_db.delete_task(task_id)
            task_list.controls.remove(task_row)
            page.update()

        delete_button = ft.IconButton(icon=ft.Icons.DELETE, icon_color=ft.Colors.RED, on_click=delete_task)

        task_row = ft.Row([checkbox, task_field, edit_button, save_button, delete_button])

        return task_row
    

    def toggle_task(task_id, is_completed):
        print(is_completed)
        main_db.update_task(task_id=task_id, completed=int(is_completed))
        load_tasks()

    def add_task_db(_):
        if task_input.value:
            task = task_input.value
            task_id = main_db.add_task(task=task)
            print(f'Задача {task} добавлена! Его ID - {task_id}')
            task_list.controls.append(view_tasks(task_id=task_id, task_text=task))
            task_input.value = None

    task_input = ft.TextField(label="Введите задачу:", expand=True, on_submit=add_task_db)
    task_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_task_db)

    def clear_completed(_):
        main_db.delete_completed_tasks()
        load_tasks()
        page.update()

    clear_button = ft.ElevatedButton("Очистить выполненные", icon=ft.Icons.DELETE_SWEEP, on_click=clear_completed)

    def set_filter(filter_value):
        nonlocal filter_type
        filter_type = filter_value
        load_tasks()

    filter_buttons = ft.Row([
        ft.ElevatedButton('Все задачи', on_click=lambda e: set_filter('all'), icon=ft.Icons.ALL_INBOX, icon_color=ft.Colors.BLACK),
        ft.ElevatedButton('В работе', on_click=lambda e: set_filter('uncompleted'), icon=ft.Icons.WATCH, icon_color=ft.Colors.RED),
        ft.ElevatedButton('Готово', on_click=lambda e: set_filter('completed'), icon=ft.Icons.CHECK_BOX, icon_color=ft.Colors.GREEN)
    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)

    def clear_completed(_):
        main_db.delete_completed_tasks()
        load_tasks()
        page.update()

    clear_button = ft.ElevatedButton("Очистить выполненные", icon=ft.Icons.DELETE_SWEEP, on_click=clear_completed)


    send_task = ft.Row([task_input, task_button])

    page.add(send_task, filter_buttons, clear_button, task_list)
    load_tasks()



if __name__ == '__main__':
    main_db.init_db()
    ft.run(main)
