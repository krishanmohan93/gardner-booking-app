from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.button.button import MDButton
from kivymd.uix.textfield.textfield import MDTextField
from kivy.metrics import dp

Builder.load_string('''
<LoginScreen>:
    MDCard:
        size_hint: None, None
        size: "320dp", "450dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        padding: 25
        spacing: 25
        orientation: 'vertical'

        MDLabel:
            text: "Gardner Booking"
            font_style: 'H5'
            halign: 'center'
            size_hint_y: None
            height: self.texture_size[1]
            pos_hint: {"center_x": .5}

        MDTextField:
            id: username
            hint_text: "Username"
            helper_text_mode: "on_error"
            required: True

        MDTextField:
            id: password
            hint_text: "Password"
            helper_text_mode: "on_error"
            password: True
            required: True

        MDButton:
            text: "LOGIN"
            size_hint_x: 1
            style: "filled"
            on_release: root.login()

        MDButton:
            text: "Don't have an account? Register here"
            size_hint_x: 1
            style: "text"
            on_release: root.manager.current = 'register'
''')

class LoginScreen(MDScreen):
    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        
        if not username or not password:
            return
            
        # TODO: Implement login logic with database
        from database.models import DatabaseHelper
        db = DatabaseHelper()
        user = db.get_user(username=username)
        
        if user and self.verify_password(password, user[3]):  # Index 3 is password_hash
            self.manager.current = 'home'
        else:
            self.ids.username.error = True
            self.ids.password.error = True
            
    def verify_password(self, password, password_hash):
        # TODO: Implement proper password verification
        return password == password_hash  # For demo only, use proper hashing in production