from ._anvil_designer import ItemTemplate16Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate16(ItemTemplate16Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.image_doc.source = self.item[0]
        self.label_address_doc.text = self.item[1]
       
        
    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("form mère atteingnable (en modif): ", self.f) 
        
        self.list_attach = [] # réinitialisation de la liste pour le repeating panel
        del  self.f.dico_attachements[self.item]
        
        for clef, valeur in self.f.dico_attachements.items():
                self.f.list_attach.append((clef,valeur))  # transformation dict en liste pour le repeating panel
        
        self.f.repeating_panel_2.items = self.f.list_attach
