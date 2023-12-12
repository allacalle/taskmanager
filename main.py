from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

class TaskManagerApp(App):
    def build(self):
        root_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)

        # Área de entrada de tarea
        self.task_input = TextInput(hint_text='Ingrese una tarea...', multiline=False, size_hint=(1, None), height=30)
        root_layout.add_widget(self.task_input)

        # Botones y área de tareas
        button_area = BoxLayout(orientation='horizontal', spacing=5)
        add_button = Button(text='Agregar Tarea', on_press=self.show_priority_buttons)
        clear_button = Button(text='Limpiar Tareas', on_press=self.clear_tasks)
        toggle_history_button = Button(text='Mostrar Historial', on_press=self.toggle_history)
        button_area.add_widget(add_button)
        button_area.add_widget(clear_button)
        button_area.add_widget(toggle_history_button)
        root_layout.add_widget(button_area)

        # Área de tareas con GridLayout y barra de desplazamiento
        self.task_list_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.task_list_layout.bind(minimum_height=self.task_list_layout.setter('height'))
        self.task_list_scrollview = ScrollView(size_hint=(1, 0.5))
        self.task_list_scrollview.add_widget(self.task_list_layout)
        root_layout.add_widget(Label(text='Tareas Pendientes', size_hint_y=None, height=30))
        root_layout.add_widget(self.task_list_scrollview)

        # Área de historial con GridLayout y barra de desplazamiento
        self.history_layout = GridLayout(cols=1, spacing=20, size_hint_y=None, padding=5)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        self.history_scrollview = ScrollView(size_hint=(1, 0.5))
        self.history_scrollview.add_widget(self.history_layout)
        root_layout.add_widget(Label(text='Historial de Tareas Completadas', size_hint_y=None, height=30))
        root_layout.add_widget(self.history_scrollview)

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

            self.task_list_scrollview.scroll_y = 0  # Scroll al principio

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
        task_label.color = (0, 0, 1, 1)  # Cambia el color a azul para indicar que está completada

        # Mover solo el label al historial
        self.task_list_layout.remove_widget(task_label.parent)
        self.history_layout.add_widget(Label(text=task_label.text))

    def delete_task(self, task_label):
        # Borra la tarea solo si está en la lista de tareas pendientes
        task_layout = task_label.parent
        if task_layout in self.task_list_layout.children:
            self.task_list_layout.remove_widget(task_layout)

    def clear_tasks(self, instance):
        self.task_list_layout.clear_widgets()

    def toggle_history(self, instance):
        # Cambiar la visibilidad del historial
        self.history_scrollview.height = 0 if self.history_scrollview.height > 0 else 300

if __name__ == '__main__':
    TaskManagerApp().run()
