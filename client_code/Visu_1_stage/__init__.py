from ._anvil_designer import Visu_1_stageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Visu_1_stage(Visu_1_stageTemplate):
    def __init__(self, num_stage, intitule, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        
        # Any code you write here will run before the form opens.
        
        
        #lecture du fichier père stages
        stage_row = app_tables.stages.get(numero=int(num_stage))    
        
        self.repeating_panel_1.items = app_tables.stagiaires_inscrits.search(stage=stage_row)
        
        
        self.label_titre.text = "Stagiaires, stage " +intitule+" (" +num_stage+ ")"

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        #from ..Main import Main
        #open_form('Main')
        open_form('Visu_stages')

    def button_annuler_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_annuler_click()

       
        
                                                                        
                                                                 