from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.button.button import MDButton
from kivymd.uix.textfield.textfield import MDTextField
from kivy.metrics import dp

Builder.load_string('''
<RegisterScreen>:
    MDCard:
        size_hint: None, None
        size: "320dp", "550dp"
        pos_hint: {"center_x": .5, "center_y": .5}
        padding: 25
        spacing: 25
        orientation: 'vertical'

        ScrollView:
            do_scroll_x: False
            do_scroll_y: True

            MDBoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: "12dp"
                padding: "12dp"

                MDLabel:
                    text: "Register"
                    font_style: 'H5'
                    halign: 'center'
                    size_hint_y: None
                    height: self.texture_size[1]

                MDTextField:
                    id: username
                    hint_text: "Username"
                    helper_text_mode: "on_error"
                    required: True

                MDTextField:
                    id: email
                    hint_text: "Email"
                    helper_text_mode: "on_error"
                    required: True

                MDTextField:
                    id: password
                    hint_text: "Password"
                    helper_text_mode: "on_error"
                    password: True
                    required: True

                MDTextField:
                    id: confirm_password
                    hint_text: "Confirm Password"
                    helper_text_mode: "on_error"
                    password: True
                    required: True

                MDTextField:
                    id: first_name
                    hint_text: "First Name"
                    helper_text_mode: "on_error"

                MDTextField:
                    id: last_name
                    hint_text: "Last Name"
                    helper_text_mode: "on_error"

                MDTextField:
                    id: phone
                    hint_text: "Phone Number"
                    helper_text_mode: "on_error"

                MDSegmentedButton:
                    id: user_type
                    size_hint_x: 1
                    md_bg_color: "lightgrey"
                    selected_color: "blue"
                    MDSegmentedButtonItem:
                        text: "Client"
                        selected: True
                    MDSegmentedButtonItem:
                        text: "Gardner"

                MDButton:
                    text: "REGISTER"
                    size_hint_x: 1
                    style: "filled"
                    on_release: root.register()

                MDButton:
                    text: "Already have an account? Login here"
                    size_hint_x: 1
                    style: "text"
                    on_release: root.manager.current = 'login'
''')

class RegisterScreen(MDScreen):
    def register(self):
        username = self.ids.username.text
        email = self.ids.email.text
        password = self.ids.password.text
        confirm_password = self.ids.confirm_password.text
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        phone = self.ids.phone.text
        user_type = 'gardner' if self.ids.user_type.selected_item_text == 'Gardner' else 'client'
        
        if not all([username, email, password, confirm_password]):
            return
            
        if password != confirm_password:
            self.ids.confirm_password.error = True
            return
            
        # TODO: Add proper password hashing
        from database.models import DatabaseHelper
        db = DatabaseHelper()
        
        try:
            user_id = db.add_user(
                username=username,
                email=email,
                password_hash=password,  # Should be hashed in production
                user_type=user_type,
                first_name=first_name,
                last_name=last_name,
                phone=phone
            )
            self.manager.current = 'login'
        except Exception as e:
            print(f"Registration error: {e}")  # Should show error in UI