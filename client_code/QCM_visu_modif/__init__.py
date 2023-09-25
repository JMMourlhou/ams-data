from ._anvil_designer import QCM_visu_modifTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class QCM_visu_modif(QCM_visu_modifTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

        # Pour les lignes QCM déjà crée du repeating panel 
        liste = list(app_tables.qcm.search())
        self.repeating_panel_1.items = liste
        nb_questions = len(liste)

        
 

    def file_loader_photo_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        #self.image_photo.source = file
        thumb_pic = anvil.image.generate_thumbnail(file, 320)
        self.image_photo.source = thumb_pic
        self.button_validation.visible = True


        


        
        