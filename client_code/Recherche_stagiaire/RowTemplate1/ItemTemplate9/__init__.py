from ._anvil_designer import ItemTemplate9Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate9(ItemTemplate9Template):                             # bt Historique a été cliqué
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        
        self.button_detail_histo.text = self.item['stage']['code']['code'] +" du " + str(self.item['stage']['date_debut'])