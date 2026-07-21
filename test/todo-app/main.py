from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox


APP_TITLE = "Todo App"
DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks() -> list[str]:
    if not DATA_FILE.exists():
        return []
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, list):
            return [str(item) for item in data]
    except (OSError, json.JSONDecodeError):
        pass
    return []


def save_tasks(tasks: list[str]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


class TodoApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("420x520")
        self.minsize(360, 420)

        self.tasks = load_tasks()

        self._build_ui()
        self._refresh_list()

    def _build_ui(self) -> None:
        root = tk.Frame(self, padx=12, pady=12)
        root.pack(fill="both", expand=True)

        title = tk.Label(root, text=APP_TITLE, font=("Segoe UI", 18, "bold"))
        title.pack(anchor="w", pady=(0, 12))

        entry_row = tk.Frame(root)
        entry_row.pack(fill="x", pady=(0, 10))

        self.task_var = tk.StringVar()
        self.task_entry = tk.Entry(entry_row, textvariable=self.task_var, font=("Segoe UI", 11))
        self.task_entry.pack(side="left", fill="x", expand=True)
        self.task_entry.bind("<Return>", lambda _event: self.add_task())

        add_btn = tk.Button(entry_row, text="Add", command=self.add_task, width=8)
        add_btn.pack(side="left", padx=(8, 0))

        list_frame = tk.Frame(root)
        list_frame.pack(fill="both", expand=True)

        self.listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, font=("Segoe UI", 11))
        scrollbar = tk.Scrollbar(list_frame, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)

        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        button_row = tk.Frame(root)
        button_row.pack(fill="x", pady=(10, 0))

        tk.Button(button_row, text="Complete", command=self.complete_task).pack(side="left", expand=True, fill="x")
        tk.Button(button_row, text="Delete", command=self.delete_task).pack(side="left", expand=True, fill="x", padx=8)
        tk.Button(button_row, text="Clear Done", command=self.clear_done).pack(side="left", expand=True, fill="x")

        self.status_var = tk.StringVar(value="Ready")
        status = tk.Label(root, textvariable=self.status_var, anchor="w", fg="#555")
        status.pack(fill="x", pady=(10, 0))

    def _refresh_list(self) -> None:
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)
        self.status_var.set(f"{len(self.tasks)} task(s)")

    def _selected_index(self) -> int | None:
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo(APP_TITLE, "Please select a task first.")
            return None
        return int(selection[0])

    def add_task(self) -> None:
        task = self.task_var.get().strip()
        if not task:
            return
        self.tasks.append(task)
        save_tasks(self.tasks)
        self.task_var.set("")
        self._refresh_list()

    def complete_task(self) -> None:
        index = self._selected_index()
        if index is None:
            return
        task = self.tasks[index]
        if task.startswith("Done: "):
            return
        self.tasks[index] = f"Done: {task}"
        save_tasks(self.tasks)
        self._refresh_list()
        self.listbox.selection_set(index)

    def delete_task(self) -> None:
        index = self._selected_index()
        if index is None:
            return
        del self.tasks[index]
        save_tasks(self.tasks)
        self._refresh_list()

    def clear_done(self) -> None:
        before = len(self.tasks)
        self.tasks = [task for task in self.tasks if not task.startswith("Done: ")]
        if len(self.tasks) == before:
            return
        save_tasks(self.tasks)
        self._refresh_list()


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
