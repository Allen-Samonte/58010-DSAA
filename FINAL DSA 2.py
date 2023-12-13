import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import sqlite3
import os
import datetime

class TaskBudgetManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskBud: Task and Budget Buddy")

        # Load and resize the logo
        logo_path = "TaskBud.png"
        logo_image = Image.open(logo_path)
        logo_image = logo_image.resize((400, 400))
        logo_photo = ImageTk.PhotoImage(logo_image)

        logo_label = tk.Label(root, image=logo_photo)
        logo_label.image = logo_photo
        logo_label.grid(row=0, column=0, columnspan=3, pady=(10, 0))

        # Notebook to switch between Task and Budget tabs
        notebook = ttk.Notebook(root)
        notebook.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Task Management tab
        task_frame = ttk.Frame(notebook)
        notebook.add(task_frame, text="Task Management")
        self.setup_task_frame(task_frame)

        # Budget Management tab
        budget_frame = ttk.Frame(notebook)
        notebook.add(budget_frame, text="Budget Management")
        self.setup_budget_frame(budget_frame)

        # Button to delete the database
        delete_database_button = tk.Button(root, text="Delete Database", command=self.delete_database)
        delete_database_button.grid(row=6, column=0, columnspan=3, pady=(10, 0))

        # Data variables for tasks and expenses
        self.tasks = []
        self.expenses = []

        # SQLite database setup
        self.conn = sqlite3.connect("task_budget.db")
        self.create_task_table()
        self.create_expense_table()

    def create_task_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,deadline TEXT)''')
        self.conn.commit()

    def create_expense_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,amount REAL)''')
        self.conn.commit()

    def insert_task(self, name, deadline):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO tasks (name, deadline) VALUES (?, ?)', (name, deadline))
        self.conn.commit()

    def insert_expense(self, name, amount):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO expenses (name, amount) VALUES (?, ?)', (name, amount))
        self.conn.commit()

    def setup_task_frame(self, frame):
        tk.Label(frame, text="Task Management", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=(10, 20))

        def add_task():
            task_name = self.task_name_entry.get()
            deadline = self.deadline_entry.get()

            try:
                # Attempt to parse the deadline in the specified format
                deadline_obj = datetime.datetime.strptime(deadline, "%m-%d-%Y").date()
            except ValueError:
                # Display an error message for invalid date format
                messagebox.showerror("Error", "Invalid date format. Please use MM-DD-YYYY.")
                return

            self.insert_task(task_name, deadline)
            self.tasks.append({"name": task_name, "deadline": deadline})

            result_label.config(text=f"Task '{task_name}' added successfully!")

        tk.Label(frame, text="Task Name:").grid(row=1, column=0, pady=(0, 5))
        self.task_name_entry = tk.Entry(frame)
        self.task_name_entry.grid(row=1, column=1, pady=(0, 5))

        tk.Label(frame, text="Deadline (MM-DD-YYYY):").grid(row=2, column=0, pady=(0, 5))
        self.deadline_entry = tk.Entry(frame)
        self.deadline_entry.grid(row=2, column=1, pady=(0, 5))

        add_button = tk.Button(frame, text="Add Task", command=add_task)
        add_button.grid(row=3, column=0, pady=(10, 0))

        # Button to View Summary
        view_summary_button = tk.Button(frame, text="View Summary", command=self.view_summary)
        view_summary_button.grid(row=3, column=1, pady=(10, 0))

        result_label = tk.Label(frame, text="")
        result_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    def setup_budget_frame(self, frame):
        tk.Label(frame, text="Budget Management", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=(10, 20))

        self.budget = tk.StringVar()

        def add_expense():
            expense_name = self.expense_name_entry.get()
            expense_amount = self.expense_amount_entry.get()

            self.insert_expense(expense_name, float(expense_amount))
            self.expenses.append({"name": expense_name, "amount": float(expense_amount)})

            self.result_label.config(text=f"Expense '{expense_name}' added successfully!")

        tk.Label(frame, text="Monthly Budget:").grid(row=1, column=0, pady=(0, 5))
        budget_entry = tk.Entry(frame, textvariable=self.budget)
        budget_entry.grid(row=1, column=1, pady=(0, 5))

        tk.Label(frame, text="Expense Name:").grid(row=2, column=0, pady=(0, 5))
        self.expense_name_entry = tk.Entry(frame)
        self.expense_name_entry.grid(row=2, column=1, pady=(0, 5))

        tk.Label(frame, text="Expense Amount:").grid(row=3, column=0, pady=(0, 5))
        self.expense_amount_entry = tk.Entry(frame)
        self.expense_amount_entry.grid(row=3, column=1, pady=(0, 5))

        add_button = tk.Button(frame, text="Add Expense", command=add_expense)
        add_button.grid(row=4, column=0, pady=(10, 0))

        # Button to View Summary
        view_summary_button = tk.Button(frame, text="View Summary", command=self.view_summary)
        view_summary_button.grid(row=4, column=1, pady=(10, 0))

        self.result_label = tk.Label(frame, text="")
        self.result_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))

    def view_summary(self):
        # Create a new window for summary
        summary_window = tk.Toplevel(self.root)
        summary_window.title("TaskBud: Summary")

        # Task Management frame in the summary window
        task_frame = ttk.Frame(summary_window)
        task_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(task_frame, text="Task Summary", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=(10, 20))

        # Retrieve tasks from the database and sort by deadline using quicksort
        cursor = self.conn.cursor()
        cursor.execute('SELECT name, deadline FROM tasks')
        self.tasks = [{"name": name, "deadline": deadline} for name, deadline in cursor.fetchall()]
        self.quick_sort(self.tasks, 0, len(self.tasks) - 1, key=lambda x: datetime.datetime.strptime(x['deadline'], '%m-%d-%Y'))

        # Display tasks
        if not self.tasks:
            tk.Label(task_frame, text="No tasks to display.").grid(row=1, column=0)
        else:
            for idx, task in enumerate(self.tasks, start=1):
                task_label = tk.Label(task_frame, text=f"{idx}. {task['name']} - Deadline: {task['deadline']}")
                task_label.grid(row=idx, column=0)

        # Budget Management frame in the summary window
        budget_frame = ttk.Frame(summary_window)
        budget_frame.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(budget_frame, text="Budget Summary", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=(10, 20))

        # Retrieve expenses from the database
        cursor.execute('SELECT name, amount FROM expenses')
        self.expenses = [{"name": name, "amount": amount} for name, amount in cursor.fetchall()]

        # Display expenses
        if not self.expenses:
            tk.Label(budget_frame, text="No expenses to display.").grid(row=1, column=0)
        else:
            total_expenses = sum(expense['amount'] for expense in self.expenses)
            for idx, expense in enumerate(self.expenses, start=1):
                expense_label = tk.Label(budget_frame, text=f"{idx}. {expense['name']} - Amount: {expense['amount']}")
                expense_label.grid(row=idx, column=0)

            total_label = tk.Label(budget_frame, text=f"\nTotal Expenses: {total_expenses}")
            total_label.grid(row=idx + 1, column=0)

            remaining_budget = float(self.budget.get()) - total_expenses
            remaining_label = tk.Label(budget_frame, text=f"Remaining Budget: {remaining_budget}")
            remaining_label.grid(row=idx + 2, column=0)

    def delete_database(self):
        # Display a confirmation message before proceeding
        confirmation = messagebox.askyesno("Delete Database", "Are you sure you want to delete the database?")
        if confirmation:
            # Close the current connection
            self.conn.close()

            # Delete the database file
            try:
                os.remove("task_budget.db")
                messagebox.showinfo("Delete Database", "Database deleted successfully.")
            except FileNotFoundError:
                messagebox.showwarning("Delete Database", "Database file not found.")
            except Exception as e:
                messagebox.showerror("Delete Database", f"An error occurred: {e}")

            # Reconnect to a new database
            self.conn = sqlite3.connect("task_budget.db")
            self.create_task_table()
            self.create_expense_table()

    def quick_sort(self, arr, low, high, key):
        if low < high:
            # Find the pivot index after partitioning
            pi = self.partition(arr, low, high, key)

            # Recursively sort the elements before and after the pivot
            self.quick_sort(arr, low, pi - 1, key)
            self.quick_sort(arr, pi + 1, high, key)

    def partition(self, arr, low, high, key):
        pivot = arr[high]
        i = low - 1

        for j in range(low, high):
            if key(arr[j]) <= key(pivot):
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def __del__(self):
        # Close the database connection when the app is closed
        self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskBudgetManagerApp(root)
    root.mainloop()
