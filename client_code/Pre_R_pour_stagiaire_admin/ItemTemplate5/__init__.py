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
        # lecture fichier père users 
        user_row=app_tables.users.get(q.fetch_only("nom","prenom"),
                                      email=self.item['user_email']['email'])
        self.button_1.text=self.item['name'].capitalize()+" "+user_row['prenom']
        
        # lecture du fichier des pré requis pour ce stagiaire
        # lecture fichier père stages
        row_stage = app_tables.stages.get(numero=self.item['stage']['numero'])
        liste_pr = app_tables.pre_requis_stagiaire.search(
                                                         stagiaire_email=user_row,        # user
                                                         stage_num=row_stage               # stage
                                                         )
        
        list(liste_pr).sort(key=lambda x: x["item_requis"]["code_pre_requis"])      # TRI par code pré requis 
        self.repeating_panel_1.items = liste_pr

    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.repeating_panel_1.visible == True:
            self.repeating_panel_1.visible = False
        else:
            self.repeating_panel_1.visible = True
            
