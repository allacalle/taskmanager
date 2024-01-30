# Dependencies
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import datetime

# Import the Database class from the database file
from database import Database

# Initialize database instance
db = Database()

# Define a custom box layout for the dialog content
class DialogContent(MDBoxLayout):
    """Opens a dialog box to get the task from the user."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set the initial text of the date field to the current date
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    def show_date_picker(self):
        """Opens the date picker."""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """Callback function for saving the selected date."""
        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)

# Define a custom list item for tasks with checkboxes
class ListItemWithCheckbox(TwoLineAvatarIconListItem):
    """Custom list item."""
    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # Store the primary key to link list items with database entries
        self.pk = pk

    def mark(self, check, the_list_item):
        """Mark the task as complete or incomplete."""
        if check.active == True:
            self.text = '[s]'+the_list_item.text+'[/s]'
            # Mark the task as complete in the database
            db.mark_task_as_complete(the_list_item.pk)
        else:
            # Mark the task as incomplete in the database
            the_list_item.text = str(db.mark_task_as_incomplete(the_list_item.pk))
        db.con.commit()

    def delete_item(self, the_list_item):
        """Delete the task."""
        # Remove the task from the UI
        self.parent.remove_widget(the_list_item)
        # Delete the task from the database
        db.delete_task(the_list_item.pk)
        db.con.commit()
    
    ###New
    #def set_completed(self, completed):
        #Set the real status of the task
     #   if completed:
      #      self.text = '[s]'+ self.text + '[/s]'
       # else:
        #    self.text = str(self.text)
        #self.ids.check.active = completed

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    """Custom left container for checkboxes."""
    pass

# Main App class
class MainApp(MDApp):
    task_list_dialog = None

    def build(self):
        """Build method called when constructing the application."""
        # Set the theme to a preferred palette
        self.theme_cls.primary_palette = "Orange"
        
    def show_task_dialog(self):
        """Show the task dialog to add tasks."""
        if not self.task_list_dialog:
            # If the dialog does not exist, create a new one with custom content
            self.task_list_dialog = MDDialog(
                title="Create Task",
                type="custom",
                content_cls=DialogContent(),
            )
        # Open the task dialog
        self.task_list_dialog.open()
   

    def on_start(self):
        """Load saved tasks and add them to the MDList widget on application start."""
        try:
            # Get completed and incompleted tasks from the database
            completed_tasks, incompleted_tasks = db.get_tasks()

            # Add incompleted tasks to the UI
            if incompleted_tasks != []:
                for task in incompleted_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0],text=task[1], secondary_text=task[2])
                    self.root.ids.container.add_widget(add_task)

            # Add completed tasks to the UI
            if completed_tasks != []:
                for task in completed_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0], text='[s]'+task[1]+'[/s]', secondary_text=task[2])
                    add_task.ids.check.active = True  # Mantendrá la casilla de verificación activa para tareas completadas
                    self.root.ids.container.add_widget(add_task)

        except Exception as e:
            print(e)
            pass

    def close_dialog(self, *args):
        """Close the current dialog."""
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date):
        """Add a task to the list of tasks."""
        # Create a new task in the database
        created_task = db.create_task(task.text, task_date)

        # Return the created task details and create a list item
        self.root.ids['container'].add_widget(ListItemWithCheckbox(pk=created_task[0], text='[b]'+created_task[1]+'[/b]', secondary_text=created_task[2]))
        
        # Clear the task input field
        task.text = ''
    
    def on_stop(self):
        # Guardar el estado de las tareas antes de cerrar la aplicación
        try:
            # Commit de todos los cambios pendientes en la base de datos
            db.con.commit()
        except Exception as e:
            print(f"Error al realizar commit: {e}")

        finally:
            # Cerrar la conexión a la base de datos
            db.close_db_connection()



# Main entry point for the application
if __name__ == '__main__':
    app = MainApp()
    app.run()
