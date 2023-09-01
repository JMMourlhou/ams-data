from ._anvil_designer import Visu_1_stageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media                               # pour le pdf standard
#from ..templates import order_pdf,simple_pdf     # fast pdf
#from fast_pdf import order_pdf,simple_pdf

class Visu_1_stage(Visu_1_stageTemplate):
    def __init__(self, num_stage, intitule, pdf_mode=False, **properties):    #si pdf_mode=True ouverture pour pdf
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.num_stage = num_stage
        self.intitule = intitule
        if pdf_mode == True:
            self.button_annuler.visible = False
            self.button_pdf.visible = False
        
        #lecture du fichier père stages
        stage_row = app_tables.stages.get(numero=int(num_stage))    
        self.repeating_panel_1.items = app_tables.stagiaires_inscrits.search(stage=stage_row)
        
        self.label_titre.text = "Stagiaires, stage " +intitule+" (" +num_stage+ ")"
        self.task = anvil.server.call('run_bg_task',num_stage, intitule)

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form('Visu_stages')

    def button_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        with anvil.server.no_loading_indicator:
            media_object = anvil.server.call('run_bg_task',self.num_stage, self.intitule)
        anvil.media.download(media_object)
    
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        order_doc = order_pdf.get_doc()
        order_doc.preview()



       
        
                                                                        
                                                                 