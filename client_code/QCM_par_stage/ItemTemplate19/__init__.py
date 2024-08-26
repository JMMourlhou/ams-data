from ._anvil_designer import ItemTemplate19Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate19(ItemTemplate19Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        """
        try:
            self.button_descro.text = str(self.item[0]) + " - " + self.item[1]   # si la liste a été construite car qcm existant
            self.check_box_visu.checked = self.item[3]
            self.text_box_p_pass.text = self.item[4]
            self.text_box_next.text = self.item[5]
        except:
            self.button_descro.text = self.item["destination"]   # si la liste a été directement copiée de la table
            self.check_box_visu.checked = self.item["visible"]
            self.text_box_p_pass.text = self.item["taux_success"]
            self.text_box_next.text = self.item["next_qcm"]
        """
        self.button_descro.text = str(self.item[0]) + " - " + self.item[1]   # la liste a été construite car qcm existant
        self.check_box_visu.checked = self.item[3]
        self.text_box_p_pass.text = self.item[4]
        self.text_box_next.text = self.item[5]
        
    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.f = get_open_form()
        
        # rajout de la clé/valeur ds le dictionaire des qcm du stage
        stage = self.f.drop_down_types_stages.selected_value
        try:
            qcm_num = self.item[0]   # si la liste a été construite car qcm existant
        except:
            qcm_num = self.item["qcm_nb"]   # si la liste a été directement copiée de la table
        print(stage["code"])
        print(qcm_num)
        # self.visible contient la col "visu_qcm_par_stage" de table qcm descro ...
        #   ... pour la création de la clé des qcm pour un stage et s'il faut le visualiser ou pas 
        #   ... le qcm est visibleou pas dès l'accès du stgiaire au menu QCM
        anvil.server.call("del_qcm_stage", qcm_num,stage) 
        
        self.button_del.visible = False
        self.f.drop_down_types_stages_change()

    def button_descro_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.button_del.visible is False:
            self.button_del.visible = True
        else:
            self.button_del.visible = False

    def check_box_visu_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        pass

    def text_box_p_pass_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        pass

    def text_box_next_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        pass

  
 
