from ._anvil_designer import ItemTemplate15Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate15(ItemTemplate15Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
         # Any code you write here will run before the form opens.
        
        self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("row: ", self.f)
       
        self.text_box_subject.text = self.item['mail_subject']
        self.text_box_subject.tag.id = self.item.get_id() # je sauve l'id du modele mail row 
        self.text_area_text.text = self.item['mail_text']