from ._anvil_designer import Visu_1_stageTemplate
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media                               # pour le pdf standard

global pdf_mode
pdf_mode=False

class Visu_1_stage(Visu_1_stageTemplate):
    def __init__(self, num_stage, intitule, pdf_mode=False, **properties):    #si pdf_mode=True ouverture pour pdf
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.num_stage = num_stage
        self.intitule = intitule
        self.pdf_mode = pdf_mode
        if self.pdf_mode == True:
            self.button_annuler.visible = False
            self.button_pdf.visible = False
            self.button_trombi.visible = False
        
        #lecture du fichier père stages
        stage_row = app_tables.stages.get(numero=int(num_stage))    
        self.repeating_panel_1.items = app_tables.stagiaires_inscrits.search(
            tables.order_by("name", ascending=True),
            stage=stage_row
        )
        """ Je peux créer une liste à partir de l'objet créé par search ( avec list() )
             et accéder ensuite à chaque row et column:
             
        list1=list(app_tables.stagiaires_inscrits.search(
            tables.order_by("name", ascending=True),
            stage=stage_row
        ))
        
        print(list1)
        print(list1[0]['name'])     row 1, column 'nom'
        """

        cod = stage_row["code"]['code']
        date = str(stage_row["date_debut"].strftime("%d/%m/%Y"))
        self.label_titre.text = "Fiches stagiaires" + cod + " du " + date + "   (num " +num_stage+")"

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form('Visu_stages')

    def button_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        with anvil.server.no_loading_indicator:
            media_object = anvil.server.call('run_bg_task',self.num_stage, self.intitule)
        "lecture du media object que j'ai stocké en server module"
        stage_row = app_tables.stages.get(numero=int(self.num_stage))
        if not stage_row:   
            print("stage non trouvé à partir de num_stages server module: Stagiaires_list_pdf")
        else:
            anvil.media.download(stage_row["list_media"])

    def button_trombi_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_trombi import Visu_trombi
        open_form('Visu_trombi',self.num_stage, self.intitule)




       
        
                                                                        
                                                                 