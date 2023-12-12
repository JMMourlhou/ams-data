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
            self.image_1.source = file
            
            path_parent, file_name, file_extension = anvil.server.call('path_info', str(file.name))
            thumb_file = None
            if file_extension != ".pdf":
                thumb_file =  anvil.image.generate_thumbnail(file, 640)
            stage_num =   self.item['stage_num']
            item_requis = self.item['item_requis']
            email =       self.item['stagiaire_email']
            result = anvil.server.call('modify_pre_r_par_stagiaire', stage_num, item_requis, email, file, thumb_file)
            
            if file_extension == ".pdf":
                #alert("pdf")
                pdf_images = anvil.server.call('get_example_pdf_as_images', stage_num, item_requis, email)
                from ....Visu_PDF_into_IMG.ImageItem import ImageItem
                open_form('Visu_PDF_into_IMG', images=pdf_images, add_border=True)
                
    def button_tele_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        file = self.image_1.source
        result = anvil.server.call("print_pdf", file)
        anvil.media.download(result)
