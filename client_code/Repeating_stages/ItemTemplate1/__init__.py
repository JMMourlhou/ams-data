from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate1(ItemTemplate1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        
        # lecture fichier père code stages
        kod = self.item['type']
        code_stage = app_tables.codes_stages.get(code=kod)
        
        self.stage.text = code_stage
        self.date_deb.text = self.item['date_debut']
        self.date_fin.text = self.item['date_fin']

    def stage_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        
