import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from sqlalchemy.orm import Session
from database import obtener_sesion
from database import Clase, Reserva

kivy.require('2.0.0')


class ClasesApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.cargar_clases()

        return self.layout

    def cargar_clases(self):
        db: Session = obtener_sesion()
        # Obtener todas las clases de la base de datos
        clases = db.query(Clase).all()

        for clase in clases:
            self.layout.add_widget(Label(text=f"Clase: {clase.tipo_clase}"))
            self.layout.add_widget(
                Label(text=f"Descripción: {clase.descripcion}"))
            self.layout.add_widget(Label(text=f"Horario: {clase.horario}"))
            btn_reservar = Button(text="Reservar Clase")
            btn_reservar.bind(on_press=lambda instance,
                              clase=clase: self.reservar_clase(clase))
            self.layout.add_widget(btn_reservar)

    def reservar_clase(self, clase):
        # Aquí deberías pasar el ID del usuario que está autenticado
        usuario_id = 1  # Cambiar por el ID real del usuario autenticado
        db: Session = obtener_sesion()
        nueva_reserva = Reserva(usuario_id=usuario_id, clase_id=clase.id)
        db.add(nueva_reserva)
        db.commit()

        self.mostrar_popup("Reserva Exitosa",
                           f"Has reservado la clase: {clase.tipo_clase}")

    def mostrar_popup(self, titulo, mensaje):
        popup = Popup(title=titulo, content=Label(
            text=mensaje), size_hint=(0.8, 0.4))
        popup.open()


if __name__ == '__main__':
    ClasesApp().run()
