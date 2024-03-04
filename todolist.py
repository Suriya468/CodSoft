from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

# Function to add a task
def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        the_cursor.execute('INSERT INTO tasks VALUES (?)', (task_string,))
        list_update()
        task_field.delete(0, 'end')

# Function to update the task list
def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

# Function to delete a task
def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            the_cursor.execute('DELETE FROM tasks WHERE title = ?', (the_value,))
            messagebox.showinfo('Success', 'Task Deleted Successfully.')
    except:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

# Function to delete all tasks
def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box:
        while len(tasks) != 0:
            tasks.pop()
        the_cursor.execute('DELETE FROM tasks')
        list_update()
        messagebox.showinfo('Success', 'All Tasks Deleted Successfully.')

# Function to clear the task list
def clear_list():
    task_listbox.delete(0, 'end')

# Function to close the application
def close():
    messagebox.showinfo('Exiting', 'Thank you for using the To-Do List!')
    guiWindow.destroy()

# Function to retrieve tasks from the database
def retrieve_database():
    while len(tasks) != 0:
        tasks.pop()
    for row in the_cursor.execute('SELECT title FROM tasks'):
        tasks.append(row[0])

if __name__ == "__main__":
    # GUI initialization
    guiWindow = Tk()
    guiWindow.title("To-Do List")
    guiWindow.geometry("665x400+550+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#EFEFEF")

    # Database connection
    the_connection = sql.connect('Tasks.db')
    the_cursor = the_connection.cursor()
    the_cursor.execute('CREATE TABLE IF NOT EXISTS tasks (title TEXT)')

    tasks = []

    # UI components
    functions_frame = Frame(guiWindow, bg="#40627C")
    functions_frame.pack(side="top", expand=True, fill="both")

    task_label = Label(functions_frame, text="To-Do List\nAdd your tasks below:",
                       font=("Arial", 14, "bold"),
                       background="#40627C",
                       foreground="#FFFFFF")
    task_label.place(x=20, y=30)

    task_field = Entry(
        functions_frame,
        font=("Arial", 14),
        width=42,
        foreground="black",
        background="white",
    )
    task_field.place(x=180, y=30)

    add_button = Button(
        functions_frame,
        text="Add Task",
        width=15,
        bg='#4CAF50', font=("Arial", 12, "bold"),
        foreground="white",
        command=add_task,
    )
    del_button = Button(
        functions_frame,
        text="Remove Task",
        width=15,
        bg='#FF5733', font=("Arial", 12, "bold"),
        foreground="white",
        command=delete_task,
    )
    del_all_button = Button(
        functions_frame,
        text="Delete All",
        width=15,
        font=("Arial", 12, "bold"),
        bg='#FF5733',
        foreground="white",
        command=delete_all_tasks
    )

    exit_button = Button(
        functions_frame,
        text="Exit / Close",
        width=52,
        bg='#FF5733', font=("Arial", 12, "bold"),
        foreground="white",
        command=close
    )
    add_button.place(x=18, y=80)
    del_button.place(x=240, y=80)
    del_all_button.place(x=460, y=80)
    exit_button.place(x=17, y=330)

    task_listbox = Listbox(
        functions_frame,
        width=70,
        height=9,
        font=("Arial", 12),
        selectmode='SINGLE',
        background="#FFFFFF",
        foreground="#40627C",
        selectbackground="#FF8C00",
        selectforeground="WHITE"
    )
    task_listbox.place(x=17, y=140)

    # Retrieve tasks from the database and update the UI
    retrieve_database()
    list_update()

    # Start the GUI event loop
    guiWindow.mainloop()

    # Commit changes and close the database connection
    the_connection.commit()
    the_cursor.close()
