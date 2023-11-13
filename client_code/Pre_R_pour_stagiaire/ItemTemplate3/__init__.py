from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media


class ItemTemplate3(ItemTemplate3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.text_box_1.text = self.item['item_requis']['requis']
        self.image_1.source = self.item['thumb_doc1']
        self.button_valid.tag.stage_num = self.item['stage_num']
        self.button_valid.tag.item_requis = self.item['item_requis']
        self.button_valid.tag.email = self.item['stagiaire_email']
        

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file != None:
            self.image_1.source = file
            self.button_valid.visible = True


    def button_valid_click(self, **event_args):
        """This method is called when the button is clicked"""
        file =        self.image_1.source 
        thumb_file =  anvil.image.generate_thumbnail(file, 320)
        stage_num =   self.button_valid.tag.stage_num
        item_requis = self.button_valid.tag.item_requis
        email =       self.button_valid.tag.email
        print("file ",file)
        print("thumb_file ",thumb_file)
        print("stage_num ", stage_num)
        print("email ", email)
     
        result = anvil.server.call('modify_pre_r_par_stagiaire', stage_num, item_requis, email, file, thumb_file)

    def button_tele_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        
        file = self.image_1.source
        alert(file)
        result = anvil.server.call("print_pdf", file)
        anvil.media.download(result)


