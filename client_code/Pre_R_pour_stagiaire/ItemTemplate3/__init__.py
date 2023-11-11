from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemTemplate3(ItemTemplate3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.text_box_1.text = self.item['item_requis']['requis']
        self.image_1.tag.stage_num = self.item['stage_num']
        self.image_1.tag.item_requis = self.item['item_requis']
        

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        
        c = FileLoader()
        if c.file != None:
            self.my_image.source = c.file
                        
            thumb_file = anvil.image.generate_thumbnail(file, 320)
          
            #self.button_validation.visible = True
            result = anvil.server.call('modify_pre_r_pour_stagiaire', file, thumb_file)

    def button_valid_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass
