from ._anvil_designer import ItemTemplate1Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate1(ItemTemplate1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        row=app_tables.pre_requis.get(code_pre_requis=self.item)
        try:
            self.text_box_1.text = "  " + row['requis']
            self.button_annuler.tag = row['code_pre_requis']
        except:
            alert("Un code pré-requis n'existe plus")

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        # lecture du dico des pré requis ds table temp
        temp_row = app_tables.temp.search()[0]
        dico = temp_row['pre_r_pour_stage']
        code_stage = temp_row['code_stage']
        
        clef_a_annuler = self.button_annuler.tag
        try:
            del dico[clef_a_annuler]
        except:
            alert(clef_a_annuler, "n'existe plus")
            
        result = anvil.server.call("modif_pre_requis_codes_stages", code_stage, dico)
        #alert("Pré requis annulé")
        # réaffichage complet 
        open_form('Pre_R_pour_type_stage',code_stage)