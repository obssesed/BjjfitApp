import kivy
from kivy.app import App
from kivy.uix.label import Label


class TestApp(App):
    def build(self):
        return Label(text='¡Hola, Kivy!')


if __name__ == '__main__':
    TestApp().run()
