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
        # récupération de la forme mère par  self.f = get_open_form() en init
        self.f = get_open_form()   # récupération de la forme mère pour accéder aux fonctions et composents
        print("form mère atteingnable (en modif): ", self.f) 
        
        # Any code you write here will run before the form opens.
        row=app_tables.pre_requis.get(code_pre_requis=self.item)
        try:
            self.text_box_1.text = "  " + row['requis']
            self.button_annuler.tag = row['code_pre_requis']
        except:
            alert(("Un code pré-requis n'existe plus en table pre_requis" )
            #msg = (f"Un code pré-requis n'existe plus pour:  {row['requis']}")
            #print(msg)

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""

        # lecture du dico des pré requis ds table temp
        """
        temp_row = app_tables.temp.search()[0]    # A MODIFIER PAS BESOIN DE TEMP ! get_open_form
        code_stage = temp_row['code_stage']
        """
        code_stage = self.f.drop_down_code_stage.selected_value['code']
        dico = self.f.drop_down_code_stage.selected_value['pre_requis']
        clef_a_annuler = self.button_annuler.tag
        try:
            del dico[clef_a_annuler]
        except:
            alert(f"{clef_a_annuler} n'existe plus")
            
        result = anvil.server.call("modif_pre_requis_codes_stages", code_stage, dico)
        if result:
            r=alert("Voulez-vous enlever les pré-requis déjà affectés pour les stagiaires de ce type de stage ?",buttons=[("oui",True),("non",False)])
            if r :   # Oui
                anvil.server.call("del_1pr",clef_a_annuler,code_stage)
        # =======================================================       
        # réaffichage complet 
        open_form('Pre_R_pour_type_stage',code_stage)