from ._anvil_designer import MainTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
#import signup_for_AMS_Data
#from signup_for_AMS_Data.Form1 import Form1

class Main(MainTemplate):
    def __init__(self, nb=2, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

   
    def button_se_connecter_click(self, **event_args):
        """This method is called when the button is clicked"""
        """Will call the EXTERNAL MODULE DEPENDACY when the link is clicked"""
                
        import sign_up_for_AMS_Data
        from sign_up_for_AMS_Data.Form1 import Form1
               
        self.content_panel.clear()
        self.content_panel.add_component(Form1(), full_width_row=True)


