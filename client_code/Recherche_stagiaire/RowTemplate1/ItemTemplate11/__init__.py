from ._anvil_designer import ItemTemplate11Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ....import Pre_R_doc_name        # Pour générer un nouveau nom au document chargé

class ItemTemplate11(ItemTemplate11Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.                              Bt docs requis cliqué
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.email = self.item['stagiaire_email']
        self.item_requis = self.item['item_requis']
        self.stage_num = self.item['stage_num']
        txt2 = self.item['item_requis']['code_pre_requis']
        txt1 = self.item['item_requis']['requis']
        self.label_1.text = txt1 +" / "+ txt2
        self.image_1.source = self.item['doc1']              # DIPLAY L'image haute qualité 

    def button_visu_click(self, **event_args):
        """This method is called when the button is clicked"""
        # nouveau nom doc
        new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse
        # si doc type jpg ds table
        if self.image_1.source != "":
            self.button_visu.visible = True
            from ....Pre_Visu_img_Pdf import Pre_Visu_img_Pdf  # pour visu du doc
            open_form('Pre_Visu_img_Pdf', self.image_1.source, new_file_name, self.stage_num, self.email, self.item_requis, origine="recherche")

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file != None:  #pas d'annulation en ouvrant choix de fichier
            self.image_1.source = file
            # nouveau nom doc SANS extension
            new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse 
            # Sauvegarde du 'file' jpg
            result = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file, new_file_name, ".jpg") 
            if result == True:
                #print(f"Fichier {new_file_name} de jpg en jpg, sauvé")
                print(f"Fichier de jpg en jpg, sauvé")

                
