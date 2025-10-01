from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.button.button import MDButton
from kivymd.uix.pickers.datepicker.datepicker import MDDatePicker
from kivymd.uix.pickers.timepicker.timepicker import MDTimePicker
from datetime import datetime, timedelta
from kivy.metrics import dp
from kivy.app import App

Builder.load_string('''
<BookingScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: "10dp"
        padding: "10dp"

        MDTopAppBar:
            title: "Book Gardner"
            left_action_items: [["arrow-left", lambda x: root.manager.current = 'gardner_list']]
            elevation: 4

        MDCard:
            size_hint: None, None
            size: "320dp", "500dp"
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
                        id: gardner_name
                        text: "Book [Gardner Name]"
                        font_style: 'H6'
                        halign: 'center'
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDLabel:
                        id: rate
                        text: "Rate: $0/hr"
                        halign: 'center'
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDDropDownItem:
                        id: service_dropdown
                        text: "Select Service"
                        on_release: root.show_service_menu()

                    MDButton:
                        text: "Select Date"
                        size_hint_x: 1
                        style: "filled"
                        on_release: root.show_date_picker()

                    MDButton:
                        text: "Select Time"
                        size_hint_x: 1
                        style: "filled"
                        on_release: root.show_time_picker()

                    MDTextField:
                        id: duration
                        hint_text: "Duration (hours)"
                        helper_text: "Enter duration in hours"
                        helper_text_mode: "on_error"
                        input_filter: "int"

                    MDLabel:
                        id: total_price
                        text: "Total Price: $0"
                        halign: 'center'
                        size_hint_y: None
                        height: self.texture_size[1]

                    MDButton:
                        text: "BOOK NOW"
                        size_hint_x: 1
                        style: "filled"
                        on_release: root.confirm_booking()
''')

class BookingScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_date = None
        self.selected_time = None
        self.gardner_data = None
        self.selected_service = None
        
    def on_pre_enter(self):
        if self.gardner_data:
            self.ids.gardner_name.text = f"Book {self.gardner_data[2]} {self.gardner_data[3]}"
            self.ids.rate.text = f"Rate: ${self.gardner_data[4]}/hr"
            
    def show_service_menu(self):
        from database.models import DatabaseHelper
        db = DatabaseHelper()
        services = db.get_gardner_services(self.gardner_data[0])
        # TODO: Show service menu and handle selection
        
    def show_date_picker(self):
        date_dialog = MDDatePicker(
            min_date=datetime.now().date(),
            max_date=datetime.now().date() + timedelta(days=30),
        )
        date_dialog.bind(on_save=self.on_date_save)
        date_dialog.open()
        
    def on_date_save(self, instance, value, date_range):
        self.selected_date = value
        
    def show_time_picker(self):
        time_dialog = MDTimePicker()
        time_dialog.bind(time=self.on_time_save)
        time_dialog.open()
        
    def on_time_save(self, instance, time):
        self.selected_time = time
        
    def confirm_booking(self):
        if not all([self.selected_date, self.selected_time, 
                   self.selected_service, self.ids.duration.text]):
            return
            
        from database.models import DatabaseHelper
        db = DatabaseHelper()
        
        booking_datetime = datetime.combine(self.selected_date, self.selected_time)
        duration = int(self.ids.duration.text)
        
        try:
            app = App.get_running_app()
            booking_id = db.create_booking(
                client_id=app.current_user_id,  # Set in main.py after login
                gardner_id=self.gardner_data[0],
                service_id=self.selected_service,
                booking_date=booking_datetime,
                duration=duration
            )
            # TODO: Send push notification to gardner
            self.manager.current = 'bookings'
        except Exception as e:
            print(f"Booking error: {e}")  # Show error in UI