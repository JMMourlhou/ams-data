from ._anvil_designer import ItemTemplate5Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate5(ItemTemplate5Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.button_1.text=self.item['name'].capitalize()+" "+self.item['prenom']
        
        # search des pré-requis de chaque tagiaire de ce stage en SERVEUR
        #     Pour lecture fichier père users: user row
        #     Pour lecture fichier père stages: stage row
        liste_pr = anvil.server.call('preparation_liste_pour_panels_pr', self.item['user_email'], self.item['stage'])
        #list(liste_pr).sort(key=lambda x: x["item_requis"]["code_pre_requis"])      # TRI par code pré requis 
        self.repeating_panel_1.items = liste_pr

    def button_1_click(self, **event_args):          # Click sur le BT nom/prénom pour voir ses pré requis
        """This method is called when the button is clicked"""
        if self.repeating_panel_1.visible == True:
            self.repeating_panel_1.visible = False
        else:
            self.repeating_panel_1.visible = True
            
