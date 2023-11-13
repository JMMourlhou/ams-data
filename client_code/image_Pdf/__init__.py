from ._anvil_designer import image_PdfTemplate
from anvil import *
#import anvil.server
#import anvil.google.auth, anvil.google.drive
#from anvil.google.drive import app_files
#import anvil.users
#import anvil.tables as tables
#import anvil.tables.query as q
#from anvil.tables import app_tables

class image_Pdf(image_PdfTemplate):
    def __init__(self, file, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.image_1.source = file