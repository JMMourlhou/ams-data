from ._anvil_designer import RowTemplate4Template
from anvil import *

import anvil.server

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate4(RowTemplate4Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        #lecture fichier users, à partir du mail, pour avoir le prénom
        stagiaire_row=app_tables.users.get(email=self.item['user_email']['email'])
        self.text_box_3.text = self.item['name'].capitalize()+" "+stagiaire_row["prenom"].capitalize()
        self.text_box_1.text = self.item['user_email']['email']
        self.text_box_2.text = stagiaire_row['tel']
        self.button_delete.tag.stagiaire_row = stagiaire_row    # pour le récupérer si bt del clicked
        stage_row=app_tables.stages.get(numero=self.item['stage']['numero'])
        self.button_delete.tag.stage_row = stage_row             # pour le récupérer si bt del clicked

    def text_box_3_focus(self, **event_args):
        """This method is called when the text area gets focus"""
        mel = self.item['user_email']['email']  
        num_stage = self.item["stage"]['numero']
        from ...Saisie_info_apres_visu import Saisie_info_apres_visu
        open_form('Saisie_info_apres_visu', mel, num_stage, intitule="")

    def text_box_1_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        self.text_box_3_focus()

    def text_box_2_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        self.text_box_3_focus()


    def bt_delete(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Enlever ce stagiaire ?",buttons=[("Non",False),("Oui",True)])
        if r :   #oui   
            stage_row = self.button_delete.tag.stage_row
            stagiaire_row = self.button_delete.tag.stagiaire_row
            txt_msg = anvil.server.call("del_stagiaire", stagiaire_row, stage_row)   # module serveur "add_stagiaire"
            alert(txt_msg)
            open_form('Stage_visu_modif',"visu_stages", stage_row['numero']) # réinitialisation de la fenêtre
        
     