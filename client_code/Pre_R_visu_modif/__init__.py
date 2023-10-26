from ._anvil_designer import Pre_R_visu_modifTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Pre_R_visu_modif(Pre_R_visu_modifTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

        # Pour pré requis déjà crée du repeating panel
        liste = list(app_tables.pre_requis.search())
        self.repeating_panel_1.items = liste

    def repeating_panel_1_show(self, **event_args):
        """This method is called when the RepeatingPanel is shown on the screen"""
        self.repeating_panel_1.tag = "repeat_panel"
