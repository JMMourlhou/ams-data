from ._anvil_designer import ItemTemplate21Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate21(ItemTemplate21Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.button_date.text = self.item['date']
        self.button_lieu.text = self.item['lieu_text']

    def button_date_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def button_lieu_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass
