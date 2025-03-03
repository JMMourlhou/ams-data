from ._anvil_designer import ItemTemplate24Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate24(ItemTemplate24Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.text_box_1.text = self.item['type']
        self.text_box_2.text = self.item['code']
        self.text_box_3.text = self.item['msg_0']
        self.text_box_4.text = self.item['msg_1']
        self.text_area_1.text = self.item['text_initial']
        self.check_box_1.checked = self.item['mot_clef_setup']
        
        self.sov_text_box_1 = self.item['type']
        self.sov_text_box_2 = self.item['code']
        self.sov_text_box_3 = self.item['msg_0']
        self.sov_text_box_4 = self.item['msg_1']
        self.sov_text_area_1 = self.item['text_initial']
        self.sov_check_box_1 = self.item['mot_clef_setup']
        
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert("Voulez-vous vraiment effacer ce lieu ?",dismissible=False,buttons=[("oui",True),("non",False)])
        if r :   # oui
            result,nb,liste = anvil.server.call("del_lieu", self.item, self.item['lieu'])
            if result is not True:
                detail=[]
                for stage in liste:
                    detail.append(stage['numero'])
                alert(f"Effacement non effectué, ce lieu est utilisé dans {nb} stage(s) :\nStage(s): {detail}")
                return
            alert("Effacement effectué !")
        open_form("Lieux_MAJ_table")

    def text_box_1_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.button_modif.visible = True

    def button_modif_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Text_box_1 (type evnt) non vide
        if self.text_box_1.text == "" or len(self.text_box_1.text) < 5:
            alert("Entrez un type d'évenement clair (> à 5 caractères")
            self.text_box_1.focus()
            return
            
        # Text_box_2 (code) non vide et sup au nb 
        if self.text_box_2.text == "":
            alert("Entrez un code !")
            self.text_box_2.focus()
            return

        # J'empêche de modifier les 3 premiers codes
        nb = int(self.text_box_2.text)
        if nb < 3:
            alert("Entrez un code supérieur à 3 !")
            self.text_box_2.focus()
            return
            
        # Text_box_3 (msg 0)non vide
        if self.text_box_3.text == "" or len(self.text_box_3.text) < 6:
            alert("Entrez le message qui apparaîtra dans le 1er menu ! (au moins 6 caractères)")
            self.text_box_3.focus()
            return
            
        # Text_box_4 (msg 1)non vide
        if self.text_box_4.text == "" or len(self.text_box_4.text) < 6:
            alert("Entrez le message qui apparaîtra dans le 2eme menu ! (au moins 6 caractères)")
            self.text_box_4.focus()
            return   
            
        r=alert("Voulez-vous vraiment modifier ce type d'évenement ?",buttons=[("oui",True),("non",False)])
        if r :   # oui
            nb = int(self.text_box_2.text)
            result = anvil.server.call("modif_type_evnt", self.item, self.text_box_1.text,
                                                                nb,
                                                                self.text_box_3.text,
                                                                self.text_box_4.text,
                                                                self.text_area_1.text,
                                                                self.check_box_1.checked               
                                      )
            if result is not True:
                alert("ERREUR, Modification non effectuée !")
                return
            alert("Modification effectuée !")
            
        else:   # non
            self.text_box_1.text = self.sov_text_box_1 
            self.text_box_2.text = self.sov_text_box_2
            self.text_box_3.text = self.sov_text_box_3 
            self.text_box_4.text = self.sov_text_box_4
            self.text_area_1.text = self.sov_text_area_1 
            self.check_box_1.checked = self.sov_check_box_1 
        
        self.button_modif.visible = False
