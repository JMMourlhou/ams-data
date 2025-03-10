from ._anvil_designer import ItemTemplate19Template
from anvil import *
import anvil.server
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
        self.check_box_start_visu.checked = self.item[2]
        
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
        result = anvil.server.call("del_qcm_stage", qcm_num,stage) 
        if result is True:
            alert("Modification des Qcm pour ce stage effectuée\n... et\nRépercution sur les stagiaires impliqués")
        else:
            alert("Erreur pour la modification des Qcm de ce stage !")
            
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
        if self.check_box_visu.checked is False:
            r=alert("Ce QCM ne sera pas visible, est-ce OK ?",dismissible=False, buttons=[("oui",True),("non",False)])
            if not r :   #Non
                return
        self.save_qcm()

    def text_box_p_pass_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.text_box_p_pass_lost_focus()
        
    def text_box_p_pass_lost_focus(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        # Taux de succès
        try:
            test = int(self.text_box_p_pass.text)   # simple test 
        except:
            alert("Le taux de succès doit être un chiffre !")
            return
            
        self.taux = int(self.text_box_p_pass.text)   
        if self.taux <50 or self.taux >100:
            alert("Le taux de succès doit être un entier compris entre 50 et 100 !")
            return
        self.save_qcm()   
            
    def text_box_next_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        self.text_box_next_lost_focus()
        
    def text_box_next_lost_focus(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        # next qcm
        self.f = get_open_form()
        nb_qcm = self.f.label_nb_qcm.text
        try:
            test = int(self.text_box_next.text)
        except:
            alert("Le numéro du prochain QCM doit être un chiffre !")
            return
            
        self.next_qcm = int(self.text_box_next.text)
        if self.next_qcm <0 or self.next_qcm > nb_qcm:
            alert(f"Le numéro du prochain QCM doit être un entier compris entre 0 (pas de prochain) et {nb_qcm} !") 
            return
        self.save_qcm()
        
    def check_box_start_visu_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.check_box_start_visu.checked is False:
            r=alert("Ce QCM sera visible quand le stagiare aura validé les qcm précédants, est-ce OK ?",dismissible=False, buttons=[("oui",True),("non",False)])
            if not r :   #Non
                return
        self.save_qcm()
    
    def save_qcm(self): 
        anvil.server.call("modif_qcm_descro_pour_un_stage",self.item[0], self.check_box_visu.checked, self.text_box_p_pass.text, self.text_box_next.text, self.check_box_start_visu.checked)



 
