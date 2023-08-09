from ._anvil_designer import MainTemplate
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from fr_custom_signup.Form1 import Form1

class Main(MainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

   
    def button_se_connecter_click(self, **event_args):
        """This method is called when the button is clicked"""
        """Will call the EXTERNAL MODULE DEPENDACY when the link is clicked"""
        """" calling the external form, result in component"""
        
        #from .. import calling_signing_up
        #calling_signing_up.calling_form1(None)  #pas d'URL, h=None
        
        import fr_custom_signup
        from fr_custom_signup.Form1 import Form1
               
        self.content_panel.clear()
        self.content_panel.add_component(Form1(), full_width_row=True)


