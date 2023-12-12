import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

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

        # Button to view summary
        view_summary_button = tk.Button(root, text="View Summary", command=self.view_summary)
        view_summary_button.grid(row=5, column=0, columnspan=3, pady=(10, 0))

        # Data variables for tasks and expenses
        self.tasks = []
        self.expenses = []

    def setup_task_frame(self, frame):
        tk.Label(frame, text="Task Management", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=(10, 20))

        tasks = []

        def add_task():
            task_name = self.task_name_entry.get()
            deadline = self.deadline_entry.get()

            task = {"name": task_name, "deadline": deadline}
            self.tasks.append(task)

            result_label.config(text=f"Task '{task_name}' added successfully!")


        def view_tasks():
            if not tasks:
                result_label.config(text="No tasks to display.")
            else:
                sorted_tasks = self.quicksort(tasks)
                result_label.config(text="Tasks sorted by deadline:")
                for idx, task in enumerate(sorted_tasks, start=1):
                    result_label.config(text=f"{idx}. {task['name']} - Deadline: {task['deadline']}")

        tk.Label(frame, text="Task Name:").grid(row=1, column=0, pady=(0, 5))
        self.task_name_entry = tk.Entry(frame)
        self.task_name_entry.grid(row=1, column=1, pady=(0, 5))

        tk.Label(frame, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, pady=(0, 5))
        self.deadline_entry = tk.Entry(frame)
        self.deadline_entry.grid(row=2, column=1, pady=(0, 5))

        add_button = tk.Button(frame, text="Add Task", command=add_task)
        add_button.grid(row=3, column=0, pady=(10, 0))

        view_button = tk.Button(frame, text="View Tasks", command=view_tasks)
        view_button.grid(row=3, column=1, pady=(10, 0))

        result_label = tk.Label(frame, text="")
        result_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    def setup_budget_frame(self, frame):
        tk.Label(frame, text="Budget Management", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=(10, 20))

        self.budget = tk.StringVar()
        self.expenses = []

        def add_expense():
            expense_name = self.expense_name_entry.get()
            expense_amount = self.expense_amount_entry.get()

            expense = {"name": expense_name, "amount": float(expense_amount)}
            self.expenses.append(expense)

            self.result_label.config(text=f"Expense '{expense_name}' added successfully!")

        def view_expenses():
            if not self.expenses:
                self.result_label.config(text="No expenses to display.")
            else:
                total_expenses = sum(expense['amount'] for expense in self.expenses)
                self.result_label.config(text="Expenses:")
                for idx, expense in enumerate(self.expenses, start=1):
                    self.result_label.config(text=f"{idx}. {expense['name']} - Amount: {expense['amount']}")

                self.result_label.config(text=f"\nTotal Expenses: {total_expenses}")
                remaining_budget = float(self.budget.get()) - total_expenses
                self.result_label.config(text=f"Remaining Budget: {remaining_budget}")

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

        view_button = tk.Button(frame, text="View Expenses", command=view_expenses)
        view_button.grid(row=4, column=1, pady=(10, 0))

        self.result_label = tk.Label(frame, text="")
        self.result_label.grid(row=5, column=0, columnspan=2, pady=(10, 0))


    def quicksort(self, tasks):
        if len(tasks) <= 1:
            return tasks
        else:
            pivot = tasks.pop()

            less_than_pivot = []
            greater_than_pivot = []

            for task in tasks:
                if task['deadline'] < pivot['deadline']:
                    less_than_pivot.append(task)
                else:
                    greater_than_pivot.append(task)

            return self.quicksort(less_than_pivot) + [pivot] + self.quicksort(greater_than_pivot)

    def view_summary(self):
        # Create a new window for summary
        summary_window = tk.Toplevel(self.root)
        summary_window.title("TaskBud: Summary")

        # Task Management frame in the summary window
        task_frame = ttk.Frame(summary_window)
        task_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(task_frame, text="Task Summary", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=3, pady=(10, 20))

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


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskBudgetManagerApp(root)
    root.mainloop()
