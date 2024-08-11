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
        self.text_box_2.text = self.item['code_pre_requis']
        self.text_box_1.text = self.item['requis']

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous vraiment effacer ce pré-requis ?",buttons=[("oui",True),("non",False)])
        if r :   # oui
            alert("oui")

    def text_box_1_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.button_modif.visible = True

    def text_box_2_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.button_modif.visible = True

    def button_modif_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous vraiment modifier l'intitulé ?",buttons=[("oui",True),("non",False)])
        sov_old_pr = self.item['requis']
        if r :   # oui
            result, nb = anvil.server.call("modif_pr", self.item, self.text_box_1.text, self.text_box_2.text)
            if result is not True:
                alert("ERREUR, Modification non effectuée !")
                return
            alert(f"Modification effectuée sur {nb} pré-requis des Stagiaires!")
            
        else:   # non
            self.text_box_1.text = sov_old_pr
        self.button_modif.visible = False

    
            