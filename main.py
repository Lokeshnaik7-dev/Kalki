import os
import json
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.video import Video
from kivy.uix.filechooser import FileChooserIconView
from chatbot import simple_bot_response

USER_DATA_FILE = "user_data.json"

# ---------------- USER AUTH ----------------
def load_users():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box = BoxLayout(orientation='vertical')
        self.email_input = TextInput(hint_text='Email', multiline=False)
        self.phone_input = TextInput(hint_text='Phone', multiline=False, input_filter='int')
        self.login_btn = Button(text='Login or Sign Up')
        self.login_btn.bind(on_press=self.login_user)

        self.box.add_widget(self.email_input)
        self.box.add_widget(self.phone_input)
        self.box.add_widget(self.login_btn)
        self.add_widget(self.box)

    def login_user(self, instance):
        email = self.email_input.text.strip()
        phone = self.phone_input.text.strip()
        users = load_users()
        users[email] = {'phone': phone}
        save_users(users)
        self.manager.current = 'main'

# ---------------- MAIN SCREEN ----------------
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.chat_input = TextInput(hint_text='Ask something...', multiline=False)
        self.chat_output = Label(text='Hello! Ask me anything.', size_hint_y=0.3)
        self.chat_btn = Button(text='Send', on_press=self.chat)

        self.video_btn = Button(text='Upload & Watch Video', on_press=self.go_to_video)

        layout.add_widget(self.chat_input)
        layout.add_widget(self.chat_btn)
        layout.add_widget(self.chat_output)
        layout.add_widget(self.video_btn)

        self.add_widget(layout)

    def chat(self, instance):
        msg = self.chat_input.text
        self.chat_output.text = simple_bot_response(msg)
        self.chat_input.text = ''

    def go_to_video(self, instance):
        self.manager.current = 'video'

# ---------------- VIDEO SCREEN ----------------
class VideoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.chooser = FileChooserIconView(path='.', filters=['*.mp4'])
        self.play_btn = Button(text='Play Selected Video', size_hint_y=0.1)
        self.play_btn.bind(on_press=self.play_video)
        self.video_player = Video(source='', state='stop', options={'eos': 'loop'}, size_hint_y=0.7)

        layout.add_widget(self.chooser)
        layout.add_widget(self.play_btn)
        layout.add_widget(self.video_player)

        self.add_widget(layout)

    def play_video(self, instance):
        selected = self.chooser.selection
        if selected:
            self.video_player.source = selected[0]
            self.video_player.state = 'play'

# ---------------- APP MANAGER ----------------
class AIApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(VideoScreen(name='video'))
        return sm

if __name__ == '__main__':
    AIApp().run()
