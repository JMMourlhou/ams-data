from ._anvil_designer import ItemTemplate30Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate30(ItemTemplate30Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # Any code you write here will run before the form opens.
        self.text_box_2.text = self.item['value']
        self.text_box_1.text = self.item['name']
        self.text_box_3.text = self.item['Commentaires']
        
        self.sov_old_name = self.item['name']
        self.sov_old_value = self.item['value']
        self.sov_old_commentaires = self.item['Commentaires']