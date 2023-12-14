from ._anvil_designer import ItemTemplate6Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate6(ItemTemplate6Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.text_area_1.text = self.item['item_requis']['requis']
        self.image_1.source = self.item['thumb_doc1']              # DIPLAY L'image basse qualité (640 x 640)

    
    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file != None:
            stage_num =   self.item['stage_num']
            item_requis = self.item['item_requis']
            email =       self.item['stagiaire_email']

            # Type de fichier ?
            path_parent, file_name, file_extension = anvil.server.call('path_info', str(file.name))
            
            thumb_file = None
            if file_extension != ".pdf":
                thumb_file =  anvil.image.generate_thumbnail(file, 640)
                
            # Sauvegarde du 'file' (qu'il soit img ou pdf)
            result, liste_images = anvil.server.call('modify_pre_r_par_stagiaire', stage_num, item_requis, email, file, file_extension, thumb_file) 
            if result == False:
                alert("Fichier non sauvé")                

            # si 'file' est pdf, je l'affiche au format jpg
            if file_extension == ".pdf":
                #liste_images = anvil.server.call('pdf_into_images', stage_num, item_requis, email)
                #extraction 1ere image de la liste (il peut y avoir plusieurs pages)
                file = liste_images[0]
                thumb_file =  anvil.image.generate_thumbnail(file, 640)    
            self.image_1.source = file

            # A créer le click sur l'image:
            #from ....Visu_PDF_into_IMG.ImageItem import ImageItem
            #open_form('Visu_PDF_into_IMG', images=liste_images, add_border=True)
          
            result = anvil.server.call('modify_pre_r_par_stagiaire', stage_num, item_requis, email, file, thumb_file)
            
            

    
    def button_tele_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        file = self.image_1.source
        result = anvil.server.call("print_pdf", file)
        anvil.media.download(result)
