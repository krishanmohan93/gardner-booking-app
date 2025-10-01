from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list.list import MDList
from kivymd.uix.card import MDCard
from kivymd.uix.button.button import MDButton
from kivy.metrics import dp
from plyer import gps
from datetime import datetime

Builder.load_string('''
<GardnerListScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        spacing: "10dp"
        padding: "10dp"

        MDTopAppBar:
            title: "Available Gardners"
            left_action_items: [["menu", lambda x: app.open_menu()]]
            elevation: 4

        MDTextField:
            id: search
            hint_text: "Search Gardners..."
            mode: "rectangle"
            size_hint_x: .9
            pos_hint: {"center_x": .5}
            on_text: root.filter_gardners(self.text)

        ScrollView:
            MDList:
                id: gardner_list

        MDButton:
            icon: "map-marker"
            style: "filled"
            pos_hint: {"center_x": .85, "center_y": .1}
            on_release: root.show_nearby_gardners()
''')

class GardnerListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_gardners()
        
    def load_gardners(self):
        from database.models import DatabaseHelper
        db = DatabaseHelper()
        gardners = db.get_gardner_list()
        
        gardner_list = self.ids.gardner_list
        gardner_list.clear_widgets()
        
        for gardner in gardners:
            item = MDCard(
                orientation='vertical',
                size_hint_y=None,
                height=dp(60),
                padding=dp(8)
            )
            item.bind(on_release=lambda x, g=gardner: self.show_gardner_details(g))
            label = Builder.load_string(f'''
MDLabel:
    text: "{gardner[2]} {gardner[3]} - ${gardner[4]}/hr"
    halign: "left"
''')
            item.add_widget(label)
            gardner_list.add_widget(item)
            
    def filter_gardners(self, search_text):
        # Filter the gardner list based on search text
        for item in self.ids.gardner_list.children:
            if search_text.lower() in item.text.lower():
                item.opacity = 1
            else:
                item.opacity = 0
                
    def show_nearby_gardners(self):
        try:
            gps.configure(on_location=self.on_location)
            gps.start()
        except:
            print("GPS not available")  # Show error in UI
            
    def on_location(self, **kwargs):
        lat = kwargs.get('lat', 0)
        lon = kwargs.get('lon', 0)
        # TODO: Filter gardners by distance using lat/lon
        gps.stop()
        
    def show_gardner_details(self, gardner):
        # Navigate directly to booking screen
        self.manager.get_screen('booking').gardner_data = gardner
        self.manager.current = 'booking'