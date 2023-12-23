from ._anvil_designer import ItemTemplate3Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
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
        self.text_box_1.text = self.item['item_requis']['requis']
        self.image_1.source = self.item['thumb_doc1']              # DIPLAY L'image basse qualité (640 x 640)

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file != None:
    
            stage_num =   self.item['stage_num']
            item_requis = self.item['item_requis']
            email =       self.item['stagiaire_email']

            # nouveau nom doc
            new_file_name = Pre_R_doc_name.doc_name_creation(stage_num, item_requis, email)   # extension non incluse 
            
            # Type de fichier ?
            path_parent, file_name, file_extension = anvil.server.call('path_info', str(file.name))

            thumb_file = None
            if file_extension != ".pdf":
                thumb_file =  anvil.image.generate_thumbnail(file, 640)
                new_file_name = new_file_name + ".jpg"
            # Sauvegarde du 'file' (qu'il soit img ou pdf)
            
            result, liste_images = anvil.server.call('modify_pre_r_par_stagiaire', stage_num, item_requis, email, file, file_extension, thumb_file, new_file_name) 
            if result == False:
                alert("Fichier non sauvé")                   


    def button_tele_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        file_name="img_stagiaire.pdf"
        file = self.image_1.source
        result = anvil.server.call("print_pdf", file, file_name)
        anvil.media.download(result)


