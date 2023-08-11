from ._anvil_designer import Menu_inscriptionTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import calling_signing_up

class Menu_inscription(Menu_inscriptionTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.title.text = "Bienvenue !"
        
        # Any code you write here will run before the form opens.

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        """Will call the EXTERNAL MODULE DEPENDACY when the link is clicked"""
                
        import sign_up_for_AMS_Data
        from sign_up_for_AMS_Data.Form1 import Form1
        #self.column_panel_header.visible = False
        self.content_panel.clear()
        self.content_panel.add_component(Form1(), full_width_row=True)

