from ._anvil_designer import ItemTemplate18Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate18(ItemTemplate18Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        try:
            self.button_descro.text = self.item[1]   # si la liste a été construite car qcm existant
            self.visu = self.item[2]             # 3eme info  self.item["visu_qcm_par_stage"]
        except:
            self.button_descro.text = self.item["destination"]   # si la liste a été directement copiée de la table
            self.visu = self.item["visu_qcm_par_stage"]

    
    def button_descro_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.button_send.visible is False:
            self.button_send.visible = True
        else:
            self.button_send.visible = False

    def button_send_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.mother_form = get_open_form()
        # rajout de la clé/valeur ds le dictionaire des qcm du stage
        stage = self.mother_form.drop_down_types_stages.selected_value
        try:
            qcm_num = self.item[0]   # si la liste a été construite car qcm existant
        except:
            qcm_num = self.item["qcm_nb"]   # si la liste a été directement copiée de la table
        print(stage["code"])
        print(qcm_num)
        # self.visible contient la col "visu_qcm_par_stage" de table qcm descro ...
        #   ... pour la création de la clé des qcm pour un stage et s'il faut le visualiser ou pas 
        #   ... le qcm est visibleou pas dès l'accès du stgiaire au menu QCM
        anvil.server.call("modif_qcm_stage", qcm_num, self.button_descro.text ,stage, self.visu) 
