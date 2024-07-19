from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
from ...import Pre_R_doc_name        # Pour générer un nouveau nom au document chargé

class ItemTemplate3(ItemTemplate3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.text_box_1.text = self.item['requis_txt']
        
        if self.item['doc1'] is not None:    # Si doc existant
            self.image_1.source = self.item['thumb']              # DIPLAY L'image thumb
            self.button_del.visible = True
            self.button_visu.visible = True
        else:
            self.button_del.visible = False            
            try:     # si pas de doc en table, erreur
                #media = self.item['doc1'].name
                self.button_visu.visible = False
            except:
                pass
        
        self.stage_num =   self.item['stage_num']        # Row stage
        self.item_requis = self.item['item_requis']      # Row Item requis
        self.email =       self.item['stagiaire_email']  # Row user

    def file_loader_1_change(self, file, **event_args):
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
            # nouveau nom doc SANS extension
            new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse 
            print("new file name: ",new_file_name)
            
            # Type de fichier ?
            path_parent, file_name, file_extension = anvil.server.call('path_info', str(file.name))

            if file_extension == ".jpg" or file_extension == ".jpeg" or file_extension == ".bmp"or file_extension == ".gif":
                
                # Sauvegarde du 'file' jpg
                #result, thumb = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file, new_file_name, ".jpg") 
                result, thumb = anvil.server.call('modify_pre_r_par_stagiaire', self.item, file, new_file_name, ".jpg") 
                self.image_1.source = thumb
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
                print("new_file_name ",new_file_name)
                result = anvil.server.call('modify_pre_r_par_stagiaire', self.stage_num, self.item_requis, self.email, file, new_file_name, ".jpg")
                if result is not True:
                    alert("Fichier jpg non sauvé") 
                self.image_1.source = file

                self.button_del.visible = True
                self.button_visu.visible = True     


    def button_visu_click(self, **event_args):
        """This method is called when the button is clicked"""
        # nouveau nom doc
        new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse
        # si doc type jpg ds table
        if self.image_1.source != "":
            self.button_visu.visible = True
            from ...Pre_Visu_img_Pdf import Pre_Visu_img_Pdf  # pour visu du doc
            open_form('Pre_Visu_img_Pdf', self.item["doc1"], new_file_name, self.stage_num, self.email, self.item_requis, origine="stagiaire")

    def button_del_click(self,  **event_args):
        """This method is called when the button is clicked"""
        result = anvil.server.call('pr_stagiaire_del',self.email, self.stage_num, self.item_requis )
        if result:
            self.image_1.source = None
            self.button_visu.visible = False
            self.button_del.visible = False
            self.file_loader_1.visible = True
        else:
            alert("Pré Requis non enlevé")
