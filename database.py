import sqlite3

class Database:
    def __init__(self):
        # Initialize the database connection and cursor
        self.con = sqlite3.connect('todo.db')
        self.cursor = self.con.cursor()
        # Create the 'tasks' table if it does not exist
        self.create_task_table()

    '''CREATE the Tasks TABLE'''
    def create_task_table(self):
        # Create the 'tasks' table with columns: id, task, due_date, completed
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tasks(id integer PRIMARY KEY AUTOINCREMENT, task varchar(50) NOT NULL, due_date varchar(50), completed BOOLEAN NOT NULL CHECK (completed IN (0, 1)))")
    
    '''CREATE A Task'''
    def create_task(self, task, due_date=None):
        self.cursor.execute("INSERT INTO tasks(task, due_date, completed) VALUES(?, ?, ?)", (task, due_date, 0))
        self._try_commit()
        print("Guardando tarea creada en la BBDD")
        # Getting the last entered item to add in the list
        created_task = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE task = ? and completed = 0", (task,)).fetchall()
        return created_task[-1]

    
    '''READ / GET the tasks'''
    def get_tasks(self):
        # Retrieve all complete and incomplete tasks from the 'tasks' table
        complete_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 1").fetchall()
        incomplete_tasks = self.cursor.execute("SELECT id, task, due_date FROM tasks WHERE completed = 0").fetchall()
        return incomplete_tasks, complete_tasks

    '''UPDATING the tasks status'''
    def mark_task_as_complete(self, taskid):
        # Update the 'completed' status of a task to 1 (complete)
        print(f"Marking task {taskid} as complete")
        self.cursor.execute("UPDATE tasks SET completed=1 WHERE id=?", (taskid,))
        self._try_commit()
        print("Task marked as complete successfully.")


    def mark_task_as_incomplete(self, taskid):
        # Update the 'completed' status of a task to 0 (incomplete)
        print(f"Marking task {taskid} as incomplete")
        self.cursor.execute("UPDATE tasks SET completed=0 WHERE id=?", (taskid,))
        self._try_commit()
        print("Task marked as complete successfully.")


        # Return the task text
        task_text = self.cursor.execute("SELECT task FROM tasks WHERE id=?", (taskid,)).fetchall()
        return task_text[0][0]

    '''Deleting the task'''
    def delete_task(self, taskid):
        # Delete a task from the 'tasks' table
        self.cursor.execute("DELETE FROM tasks WHERE id=?", (taskid,))
        self._try_commit()
        print("Task {taskid} delete successfully")

    '''Closing the connection '''
    def close_db_connection(self):
        # Close the database connection
        self._try_commit()
        self.con.close()


    def _try_commit(self):
        try:
            self.con.commit()
        except Exception as e:
            print(f"Error al realizar commit: {e}")
