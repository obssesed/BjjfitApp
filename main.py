import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from sqlalchemy.orm import Session
from usuarios import registrar_usuario, autenticar_usuario, obtener_sesion
import re

kivy.require('2.3.0')


class RegistroLoginApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Campos de registro
        self.layout.add_widget(Label(text='Nombre de Usuario:'))
        self.nombre_usuario_input = TextInput(multiline=False)
        self.layout.add_widget(self.nombre_usuario_input)

        self.layout.add_widget(Label(text='Correo Electrónico:'))
        self.correo_input = TextInput(multiline=False)
        self.layout.add_widget(self.correo_input)

        self.layout.add_widget(Label(text='Teléfono:'))
        self.telefono_input = TextInput(multiline=False)
        self.layout.add_widget(self.telefono_input)

        self.layout.add_widget(Label(text='Contraseña:'))
        self.contrasenya_input = TextInput(password=True, multiline=False)
        self.layout.add_widget(self.contrasenya_input)

        # Botón de registro
        self.registro_button = Button(
            text='Registrarse', on_press=self.registrar_usuario)
        self.layout.add_widget(self.registro_button)

        # Botón de inicio de sesión
        self.login_button = Button(
            text='Iniciar Sesión', on_press=self.iniciar_sesion)
        self.layout.add_widget(self.login_button)

        # ID del usuario autenticado
        self.usuario_id = None

        return self.layout

    def validar_email(self, email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email)

    def validar_contrasenya(self, contrasenya):
        if len(contrasenya) < 9:
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', contrasenya):
            return False
        return True

    def validar_telefono(self, telefono):
        if len(telefono) != 9:
            return False
        return True

    def registrar_usuario(self, instance):
        if not self.nombre_usuario_input.text or not self.correo_input.text or not self.telefono_input.text or not self.contrasenya_input.text:
            self.mostrar_popup("Error", "Todos los campos son obligatorios.")
            return

        if not self.validar_email(self.correo_input.text):
            self.mostrar_popup("Error", "El correo electrónico no es válido.")
            return

        if not self.validar_contrasenya(self.contrasenya_input.text):
            self.mostrar_popup(
                "Error", "La contraseña debe tener más de 8 caracteres y al menos un carácter especial.")
            return

        if not self.validar_telefono(self.telefono_input.text):
            self.mostrar_popup(
                "Error", "El número de teléfono que has introducido es incorrecto.")
            return

        db: Session = obtener_sesion()
        nuevo_usuario = registrar_usuario(
            nombre_usuario=self.nombre_usuario_input.text,
            correo_electronico=self.correo_input.text,
            telefono=self.telefono_input.text,
            contrasenya=self.contrasenya_input.text,
            db=db
        )
        self.mostrar_popup(
            "Registro exitoso", f"Usuario {nuevo_usuario.nombre_usuario} registrado.")

    def iniciar_sesion(self, instance):
        db: Session = obtener_sesion()
        usuario = autenticar_usuario(
            nombre_usuario=self.nombre_usuario_input.text,
            contrasenya=self.contrasenya_input.text,
            db=db
        )
        if usuario:
            self.usuario_id = usuario.id  # Guardar el ID del usuario autenticado
            self.mostrar_popup("Inicio de sesión exitoso",
                               f"Bienvenido, {usuario.nombre_usuario}! (ID: {self.usuario_id})")
        else:
            self.mostrar_popup("Error", "Credenciales incorrectas.")

    def mostrar_popup(self, titulo, mensaje):
        popup = Popup(title=titulo, content=Label(
            text=mensaje), size_hint=(0.8, 0.4))
        popup.open()


if __name__ == '__main__':
    RegistroLoginApp().run()
