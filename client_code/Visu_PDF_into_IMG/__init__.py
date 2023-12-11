from ._anvil_designer import Visu_PDF_into_IMGTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Visu_PDF_into_IMG(Visu_PDF_into_IMGTemplate):
    def __init__(self,  images, add_border: bool=False, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        list = [{
        'image': im,
        'page_number': page_number + 1,
        'display_page_numbers': len(images) > 1,
        'add_border': add_border,
        } for page_number, im in enumerate(images)]
    
        self.images.items = list

    def Retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Pre_R_pour_stagiaire_admin import Pre_R_pour_stagiaire_admin
        open_form('Pre_R_pour_stagiaire_admin',num_stage="107")
