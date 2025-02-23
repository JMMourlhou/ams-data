from ._anvil_designer import ItemTemplate23Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate23(ItemTemplate23Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # récupération de la forme mère par  self.f = get_open_form() en init
        self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("form mère atteingnable (en modif): ", self.f) 
        
        # Any code you write here will run before the form opens.
        row=app_tables.texte_formulaires.get(code=self.item)
        try:
            self.text_box_1.text = "  " + row['code']
            self.text_box_2.text = "  "  + row['text']
            self.check_box_1.checked = row['obligation']
            self.button_annuler.tag = row['code']
        except:
            alert("Un code pré-requis n'existe plus en table pre_requis")
            #msg = (f"Un code pré-requis n'existe plus pour:  {row['requis']}")
            #print(msg)