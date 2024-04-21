from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
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
            #msg = (f"Un code pré-requis n'existe plus pour:  {row['requis']}")
            #print(msg)

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
        r=alert("Voulez-vous enlever les pré-requis déjà affectés pour les stagiaires ?",buttons=[("oui",True),("non",False)])
        if r :   # Oui
            #lecture du fichier père stages
            stage_row = app_tables.codes_stages.get(code=code_stage)
            #lecture du pré_requis à enlever
            pr = app_tables.pre_requis.get(requis=clef_a_annuler)
            # lecture des stages et pr impliqués
            liste = app_tables.pre_requis_stagiaire.search(code = stage_row,
                                                           item_requis = pr
                                                          )
            # Pour chq stagiaire, lecture du dico
            for pr_stagiaire in liste:
                #lecture du dico
                pr_stagiaire.delete()
                
                
        # réaffichage complet 
        open_form('Pre_R_pour_type_stage',code_stage)