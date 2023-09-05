from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        alert("form1")
        #xy_panel = XYPanel(width=400, height=400)

        btn = Button(text="Click me!", background="white", foreground="black")
        self.xy_panel.add_component(btn, x=1, y=1)
        
        img = Image(source="_/theme/Logo%20F%20S%20small_transparent.png")
        self.xy_panel.add_component(img, x=1, y=100, width=200)