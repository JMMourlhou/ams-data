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
            alert("Un code texte n'existe plus en table Texte_formulaire")
            #msg = (f"Un code pré-requis n'existe plus pour:  {row['requis']}")
            #print(msg)
            
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous vraiment effacer ce code ?",dismissible=False,buttons=[("oui",True),("non",False)])
        if r :   # oui
            """
            result = anvil.server.call("del_text_formulaire", self.item)
            if result is not True:
                alert("Erreur: Effacement non effectué !")
                return
            alert("Effacement effectué !")
            """
        open_form("Text_formulaires_MAJ_table")
        
    def button_modif_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous vraiment modifier ce code ?",buttons=[("oui",True),("non",False)])
        sov_old_text = self.item['text']
        sov_old_code = self.item['code']
        sov_old_obligation = self.item['obligation']
        if r :   # oui
            """
            # 1 modif text_formulaire
            result = anvil.server.call("modif_text_formulaire", self.item, self.text_box_1.text, self.text_box_2.text, self.check_box_1.checked)
            if result is not True:
                alert("ERREUR, Modification non effectuée !")
                return
            alert("Modification effectuée !")
            """
        else:   # non
            self.text_box_1.text = sov_old_code
            self.text_box_2.text = sov_old_text
            self.radio_button_1 = sov_old_obligation
        self.button_modif.visible = False
        
    def text_box_2_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.button_modif.visible = True

    def check_box_1_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.visible = True
