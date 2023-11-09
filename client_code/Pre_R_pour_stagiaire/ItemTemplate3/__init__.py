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

    def file_loader_2_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        thumb_pic = anvil.image.generate_thumbnail(file, 640)
        self.image_1.source = thumb_pic
        #self.button_validation.visible = True