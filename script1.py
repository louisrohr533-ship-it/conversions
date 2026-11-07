from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup

# --- CODE PIN DE L'APPLICATION ---
APP_PIN = "2580"

# --- ÉCRAN DE VERROUILLAGE ---
class LockScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)
        self.pin_input = TextInput(hint_text="Entrez le code PIN", password=True, multiline=False)
        submit_btn = Button(text="Accéder", size_hint_y=None, height=50)
        submit_btn.bind(on_press=self.check_pin)
        layout.add_widget(Label(text="🔒 Application sécurisée"))
        layout.add_widget(self.pin_input)
        layout.add_widget(submit_btn)
        self.add_widget(layout)

    def check_pin(self, instance):
        if self.pin_input.text == APP_PIN:
            self.manager.current = "notes"
        else:
            popup = Popup(title="Erreur",
                          content=Label(text="Code PIN incorrect !"),
                          size_hint=(0.7, 0.4))
            popup.open()

# --- ÉCRAN DES NOTES ---
class NotesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        self.notes_input = TextInput(hint_text="Écris tes notes ici...", multiline=True)
        save_btn = Button(text="Sauvegarder", size_hint_y=None, height=50)
        save_btn.bind(on_press=self.save_notes)
        morpion_btn = Button(text="Jouer au Morpion", size_hint_y=None, height=50)

        layout.add_widget(self.notes_input)
        layout.add_widget(save_btn)
        layout.add_widget(morpion_btn)
        self.add_widget(layout)

    def save_notes(self, instance):
        content = self.notes_input.text
        popup = Popup(title="Notes sauvegardées",
                      content=Label(text=f"Tu as sauvegardé:\n{content}"),
                      size_hint=(0.7, 0.5))
        popup.open()

# --- ÉCRAN MORPION ---
class MorpionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board = [''] * 9
        layout = BoxLayout(orientation='vertical', spacing=5, padding=5)
        self.buttons = []
        for i in range(3):
            row = BoxLayout()
            for j in range(3):
                idx = i*3 + j
                btn = Button(text='', font_size=40)
                btn.bind(on_press=lambda btn, idx=idx: self.make_move(idx))
                self.buttons.append(btn)
                row.add_widget(btn)
            layout.add_widget(row)
        self.status_label = Label(text="X commence!", size_hint_y=None, height=40)
        back_btn = Button(text="Retour aux notes", size_hint_y=None, height=50)
        back_btn.bind(on_press=lambda x: self.manager.current = "notes")
        layout.add_widget(self.status_label)
        layout.add_widget(back_btn)
        self.add_widget(layout)
        self.turn = 'X'

    def make_move(self, idx):
        if self.board[idx] == '':
            self.board[idx] = self.turn
            self.buttons[idx].text = self.turn
            if self.check_winner(self.turn):
                self.status_label.text = f"{self.turn} a gagné!"
            else:
                self.turn = 'O' if self.turn == 'X' else 'X'
                self.status_label.text = f"Tour de {self.turn}"

    def check_winner(self, player):
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if self.board[a]==self.board[b]==self.board[c]==player:
                return True
        return False

# --- GESTION DES ÉCRANS ---
sm = ScreenManager()
sm.add_widget(LockScreen(name="lock"))
sm.add_widget(NotesScreen(name="notes"))
sm.add_widget(MorpionScreen(name="morpion"))

class MyApp(App):
    def build(self):
        return sm

if __name__ == "__main__":
    MyApp().run()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
