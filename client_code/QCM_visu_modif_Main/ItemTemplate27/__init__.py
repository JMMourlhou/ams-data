from ._anvil_designer import ItemTemplate27Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate27(ItemTemplate27Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        try:
            self.button_descro.text = str(self.item[0]) + " - " + self.item[1]   # si la liste a été construite car qcm existant
            self.sov_qcm_nb = str(self.item[0])
        except:
            # si la liste a été directement copiée de la table 
            self.button_descro.text = str(self.item['qcm_nb']) + " - " +  self.item["destination"]      # (dict du stage choisi était encore vide)
            self.sov_qcm_nb = str(self.item['qcm_nb'])
            
    def button_descro_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.button_send.visible is False:
            self.button_send.visible = True
        else:
            self.button_send.visible = False

    def button_send_click(self, **event_args):
        """This method is called when the button is clicked"""
        # écriture du nouveau qcm enfant dans le dictionaire
        # self.sov_qcm_nb contient le qcm à ajouter dans le dico
