# main7.py
import flet as ft
import sqlite3
from datetime import datetime

DB_NAME = "tasks.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0,
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_task_db(title):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(
        "INSERT INTO tasks (title, done, created_at) VALUES (?, 0, ?)",
        (title, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_tasks_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, title, done FROM tasks ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows


def update_task_status(task_id, done):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET done=? WHERE id=?", (done, task_id))
    conn.commit()
    conn.close()


def clear_completed_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE done = 1")
    conn.commit()
    conn.close()


def main(page: ft.Page):
    page.title = "TODO | Автоочистка"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    init_db()

    tasks_column = ft.Column(spacing=10)

    def load_tasks():
        tasks_column.controls.clear()
        for task_id, title, done in get_tasks_db():
            checkbox = ft.Checkbox(
                label=title,
                value=bool(done),
                on_change=lambda e, tid=task_id: toggle_task(e, tid),
            )
            tasks_column.controls.append(checkbox)
        page.update()

    def toggle_task(e, task_id):
        update_task_status(task_id, int(e.control.value))

    def add_task(e):
        if task_input.value.strip():
            add_task_db(task_input.value.strip())
            task_input.value = ""
            load_tasks()

    def clear_done(e):
        clear_completed_tasks()
        load_tasks()

    task_input = ft.TextField(
        hint_text="Новая задача",
        expand=True,
        on_submit=add_task,
    )

    add_button = ft.IconButton(icon=ft.icons.ADD, on_click=add_task)

    clear_button = ft.ElevatedButton(
        "Очистить выполненные",
        icon=ft.icons.DELETE_FOREVER,
        bgcolor=ft.colors.RED_400,
        on_click=clear_done,
    )

    page.add(
        ft.Text("Умный TODO-лист", size=22, weight=ft.FontWeight.BOLD),
        ft.Row([task_input, add_button]),
        clear_button,
        ft.Divider(),
        tasks_column,
    )

    load_tasks()


ft.app(target=main)
