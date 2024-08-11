from ._anvil_designer import ItemTemplate13Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate13(ItemTemplate13Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.text_box_1.text = self.item['requis']

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass
