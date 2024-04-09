from ._anvil_designer import ItemTemplate6Template
from anvil import *

import anvil.server

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from ....import Pre_R_doc_name        # Pour générer un nouveau nom au document chargé
from ....Pre_Visu_img_Pdf import Pre_Visu_img_Pdf   #pour afficher un document avant de le télécharger

class ItemTemplate6(ItemTemplate6Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        txt2 = self.item['item_requis']['code_pre_requis']
        txt1 = self.item['item_requis']['requis']
        self.label_1.text = txt1 +" / "+ txt2
        self.image_1.source = self.item['doc1']              # DIPLAY L'image haute qualité 
        try:
            media = self.item['doc1'].name
            self.button_visu.visible = True
        except:
            pass
        
        self.stage_num =   self.item['stage_num'] 
        self.item_requis = self.item['item_requis']
        self.email =       self.item['stagiaire_email']
    
    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        # nouveau nom doc SANS extension
        new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse 
        #print("new file name: ",new_file_name)
        
        # Type de fichier ?
        path_parent, file_name, file_extension = anvil.server.call('path_info', str(file.name))

        """
        thumb_file = None
        # si 'file' est jpg, je l'affiche directement 
        if file_extension == ".jpg":
            print("JPG loaded")
            new_file_name = new_file_name + ".jpg" # rajout extension
            thumb_file =  anvil.image.generate_thumbnail(file, 640)
        """  
        if file_extension == ".jpg":
            self.image_1.source = file
            # Sauvegarde du 'file' jpg
            result = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file, new_file_name, ".jpg") 
            if result == True:
                print(f"Fichier de jpg en jpg, sauvé")
            else:
                self.button_visu.visible = True  
                
        if file_extension == ".pdf":      
            # Sauvegarde du 'file'
            result = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file,  new_file_name, ".pdf") 
            if result == False:
                alert("Fichier PDF non sauvé")   
            else:
                print("Fichier PDF sauvé")
                  
            # génération du JPG à partir du pdf
            liste_images = anvil.server.call('pdf_into_jpg', self.stage_num, self.item_requis, self.email, new_file_name)
            #extraction 1ere image de la liste (il peut y avoir plusieurs pages)
            print("nb d'images jpg crées par pdf_into_jpg:", len(liste_images))
            file = liste_images[0]
            #thumb_file =  anvil.image.generate_thumbnail(file, 640)
            # renvoi en écriture des images générées ds table
            file_ext = ".jpg"
            new_file_name = new_file_name + ".jpg"
            print("new_file_name ",new_file_name)
            result = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file, new_file_name, ".jpg")
            if result != True:
                alert("Fichier jpg non sauvé") 
            self.image_1.source = file
            self.button_visu.visible = True    
            
    def button_visu_click(self, **event_args):
        """This method is called when the button is clicked"""
        # nouveau nom doc
        new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse
        # si doc type jpg ds table
        if self.image_1.source != "":
            self.button_visu.visible = True
            from ....Pre_Visu_img_Pdf import Pre_Visu_img_Pdf  # pour visu du doc
            open_form('Pre_Visu_img_Pdf', self.image_1.source, new_file_name, self.stage_num, self.email, self.item_requis, origine="admin")
        





