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
        
        liste = list(app_tables.qcm.search())
        self.repeating_panel_1.items = liste
        nb_questions = len(liste)
        self.text_box_num = nb_questions + 1
        
        