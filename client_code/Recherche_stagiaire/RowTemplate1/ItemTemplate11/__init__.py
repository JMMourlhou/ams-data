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
        #txt2 = self.item['item_requis']['code_pre_requis']
        txt2 = self.item['code_txt']
        #txt1 = self.item['item_requis']['requis']
        txt1 = self.item['requis_txt']
        self.label_1.text = txt1 +" / "+ txt2
        if self.item['doc1'] is not None:
            self.image_1.source = self.item['doc1']              # DIPLAY L'image haute qualité 
            self.button_del.visible = True
            self.button_visu.visible = True
            self.file_loader_1.visible = False
        else:
            self.button_del.visible = False
            self.button_visu.visible = False
            self.file_loader_1.visible = True

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
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
            # nouveau nom doc SANS extension
            new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse 
            print("new file name: ",new_file_name)
            
            # Type de fichier ?
            path_parent, file_name, file_extension = anvil.server.call('path_info', str(file.name))
            print("ext: ",file_extension)

            """
            thumb_file = None
            # si 'file' est jpg, je l'affiche directement 
            if file_extension == ".jpg":
                print("JPG loaded")
                new_file_name = new_file_name + ".jpg" # rajout extension
                thumb_file =  anvil.image.generate_thumbnail(file, 640)
            """  
            if file_extension == ".jpg" or file_extension == ".JPG":
                self.image_1.source = file
                # Sauvegarde du 'file' jpg
                result = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file, new_file_name, ".jpg") 
                if result is True:
                    print("Fichier de jpg en jpg, sauvé")
                    self.button_visu.visible = True  
                    self.button_del.visible = True
                else:
                    alert("Fichier de jpg non sauvé")
                    self.button_visu.visible = False  
                    self.button_del.visible = False
                    
            if file_extension == ".pdf":      
               
                # Sauvegarde du 'file'
                result = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file,  new_file_name, ".pdf") 
                if result is False:
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
                new_file_name = new_file_name + ".jpg"
                #print("new_file_name ",new_file_name)
                result = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file, new_file_name, ".jpg")
                if result is not True:
                    alert("Fichier jpg non sauvé") 
                self.image_1.source = file

                self.button_del.visible = True
                self.button_visu.visible = True 
                self.file_loader_1.visible = False

    def button_del_click(self, **event_args):
        """This method is called when the button is clicked"""
        result = anvil.server.call('pr_stagiaire_del',self.email, self.stage_num, self.item_requis )
        if result:
            self.image_1.source = None
            self.button_visu.visible = False
            self.button_del.visible = False
            self.file_loader_1.visible = True
        else:
            alert("Pré Requis non enlevé")

                
