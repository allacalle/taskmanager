from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup

class TaskManagerApp(App):
    def build(self):
        self.task_list_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)
        self.task_input = TextInput(hint_text='Ingrese una tarea...', multiline=False, size_hint=(1, None), height=30)

        add_button = Button(text='Agregar Tarea', on_press=self.show_priority_buttons, size_hint=(1, None), height=44)
        clear_button = Button(text='Limpiar Tareas', on_press=self.clear_tasks, size_hint=(1, None), height=44)

        root_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)
        root_layout.add_widget(self.task_input)
        root_layout.add_widget(add_button)
        root_layout.add_widget(clear_button)
        root_layout.add_widget(self.task_list_layout)

        return root_layout

    def show_priority_buttons(self, instance):
        content = BoxLayout(orientation='vertical', spacing=10)
        urgent_button = Button(text='Urgente', on_press=lambda x: self.add_task('Urgente', self.task_input.text),
                               background_color=(1, 0, 0, 1))  # Rojo
        medium_button = Button(text='Media', on_press=lambda x: self.add_task('Media', self.task_input.text),
                               background_color=(1, 1, 0, 1))  # Amarillo
        low_button = Button(text='Baja', on_press=lambda x: self.add_task('Baja', self.task_input.text),
                            background_color=(0, 1, 0, 1))  # Verde

        content.add_widget(urgent_button)
        content.add_widget(medium_button)
        content.add_widget(low_button)

        self.popup = Popup(title='Seleccionar Prioridad', content=content, size_hint=(None, None), size=(300, 200))
        self.popup.open()

    def add_task(self, priority, task_text):
        if task_text:
            color = self.get_priority_color(priority)

            task_label = Label(text=f'- {task_text}', color=color, size_hint_y=None, height=30)
            complete_button = Button(text='Completar', on_press=lambda x, label=task_label: self.complete_task(label), size_hint=(0.2, 1))
            delete_button = Button(text='Eliminar', on_press=lambda x, label=task_label: self.delete_task(label), size_hint=(0.2, 1))
            task_layout = BoxLayout(orientation='horizontal', spacing=5, size_hint_y=None, height=40)
            task_layout.add_widget(task_label)
            task_layout.add_widget(complete_button)
            task_layout.add_widget(delete_button)

            self.task_list_layout.add_widget(task_layout)
            self.task_input.text = ''

            # Ajustar la altura del ScrollView
            self.task_list_layout.height = len(self.task_list_layout.children) * (task_layout.height + 5)

            self.popup.dismiss()  # Cerrar la pantalla emergente después de agregar la tarea

    def get_priority_color(self, priority):
        if priority == 'Urgente':
            return (1, 0, 0, 1)  # Rojo
        elif priority == 'Media':
            return (1, 1, 0, 1)  # Amarillo
        elif priority == 'Baja':
            return (0, 1, 0, 1)  # Verde
        else:
            return (1, 1, 1, 1)  # Blanco (por defecto)

    def complete_task(self, task_label):
        task_label.color = (0, 0, 0, 1)  # Cambia el color a negro para indicar que está completada

    def delete_task(self, task_layout):
        self.task_list_layout.remove_widget(task_layout)

    def clear_tasks(self, instance):
        self.task_list_layout.clear_widgets()

if __name__ == '__main__':
    TaskManagerApp().run()
