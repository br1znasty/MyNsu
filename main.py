from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout

#v 0.0.1.1

class MainApp(App):
    def build(self):
        labels = [Label(text="Hello World!!!!!", size_hint=(1, 1), pos_hint={"center_x": .9, "center_y": .9})]
        buttons = [Button(text="GoodBye", font_size=14, size_hint=(1, 1), pos_hint={"center_x": .1, "center_y": .9})]

        fl = FloatLayout(size=(300, 300))
        for i in buttons:
            fl.add_widget(i)
        fl.add_widget(labels[0])
        return fl

if __name__ == "__main__":
    MainApp().run()