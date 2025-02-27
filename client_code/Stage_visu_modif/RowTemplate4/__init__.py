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
        #lecture fichier users, à partir du mail, pour avoir le prénom, mail, tel
        self.stagiaire_row=app_tables.users.get(q.fetch_only("nom","prenom","email","tel"),
                                            email=self.item['user_email']['email']
                                            )
        self.text_box_3.text = self.item['name'].capitalize()+" "+self.stagiaire_row["prenom"].capitalize()
        self.text_box_1.text = self.item['user_email']['email']
        self.text_box_2.text = self.stagiaire_row['tel']
        self.check_box_form_satis.checked = self.item['enquete_satisf']
        self.check_box_form_suivi.checked = self.item['enquete_suivi']
   
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
        r=alert("Enlever ce stagiaire de ce stage ?",dismissible=False,buttons=[("Non",False),("Oui",True)])
        if r :   #oui   
            stage_row = self.item["stage"]
            txt_msg = anvil.server.call("del_stagiaire", self.stagiaire_row, stage_row)   # module serveur "add_stagiaire"
            alert(txt_msg)
            # réaffichage par initialisation de la forme mère 
            open_form('Stage_visu_modif', stage_row['numero']) # réinitialisation de la fenêtre

    def check_box_form_satis_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        stagiaire_row=self.item    # formulaire de satisf rempli T/F
        txt_msg = anvil.server.call("init_formulaire_satis_stagiaire", stagiaire_row, self.check_box_form_satis.checked)   # module serveur "add_stagiaire"
        alert(txt_msg)
        
   
    def check_box_form_suivi_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        stagiaire_row=self.item   # formulaire de suivi rempli T/F
        txt_msg = anvil.server.call("init_formulaire_suivi_stagiaire", stagiaire_row, self.check_box_form_suivi.checked)   # module serveur "add_stagiaire"
        alert(txt_msg)
        
     