from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from screens.login import LoginScreen
from screens.register import RegisterScreen
from screens.gardner_list import GardnerListScreen
from screens.booking import BookingScreen

# Firebase will be added later
# import firebase_admin
# from firebase_admin import credentials, messaging

class GardnerBookingApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_user_id = None
        # Firebase setup commented for testing
        # self.setup_firebase()
        
    def setup_firebase(self):
        # Initialize Firebase for notifications - disabled for testing
        pass
        
    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.theme_style = "Light"
        
        # Set window size for desktop testing
        Window.size = (360, 640)  # Typical mobile phone size
        
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register'))
        sm.add_widget(GardnerListScreen(name='gardner_list'))
        sm.add_widget(BookingScreen(name='booking'))
        
        return sm
        
    def send_notification(self, token, title, body):
        # Firebase notifications disabled for testing
        print(f"Would send notification: {title} - {body} to {token}")
        pass

if __name__ == '__main__':
    GardnerBookingApp().run()