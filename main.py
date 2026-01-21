from db import main_db
import flet as ft

def main(page: ft.Page):
    # print('Hello Flet')
    page.theme_mode = ft.ThemeMode.LIGHT

    task_list = ft.Column()

    def view_tasks(task_id, task_text, task_date):
        task_field = ft.TextField(read_only=True, value=task_text, expand=True)
        date_text = ft.Text(value=task_date, size=12, color="grey")


        def enable_edit(_):
            if task_field.read_only == True:
                task_field.read_only = False
            else:
                task_field.read_only = True



        edit_button = ft.IconButton(icon=ft.Icons.EDIT, on_click=enable_edit)

        def save_task(_):
            main_db.update_task(task_id=task_id, new_task=task_field.value)
            task_field.read_only = True 
            page.update()

        save_button = ft.IconButton(icon=ft.Icons.SAVE, on_click=save_task)

        return ft.Row([task_field, date_text, edit_button, save_button])

    def add_task_db(_):
        if task_input.value:
            task = task_input.value
            task_id, task_date = main_db.add_task(task=task)
            print(f'Задача {task} добавлена! Его ID - {task_id}')
            task_list.controls.append(view_tasks(task_id=task_id, task_text=task, task_date=task_date))
            task_input.value = None
            page.update

    task_input = ft.TextField(label="Введите задачу:", expand=True, on_submit=add_task_db)
    task_button = ft.IconButton(icon=ft.Icons.ADD, on_click=add_task_db)
    send_task = ft.Row([task_input, task_button])

    page.add(send_task, task_list)
    

if __name__ == '__main__':
    main_db.init_db()
    ft.run(main)