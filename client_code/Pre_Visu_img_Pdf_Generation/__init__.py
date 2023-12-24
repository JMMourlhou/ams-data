from ._anvil_designer import Pre_Visu_img_Pdf_GenerationTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Pre_Visu_img_Pdf_Generation(Pre_Visu_img_Pdf_GenerationTemplate):
    def __init__(self, file, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.image_1.source = file


   
