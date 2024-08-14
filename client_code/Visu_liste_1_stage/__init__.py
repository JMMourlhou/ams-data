from ._anvil_designer import Visu_liste_1_stageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media                               # pour le pdf standard

global pdf_mode
pdf_mode=False

class Visu_liste_1_stage(Visu_liste_1_stageTemplate):
    def __init__(self, num_stage, intitule, pdf_mode=False, **properties):    #si pdf_mode=True ouverture pour pdf
        print("pdf_mode ", pdf_mode)
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.f = get_open_form()
        
        self.num_stage = num_stage
        self.intitule = intitule
        self.pdf_mode = pdf_mode
        if self.pdf_mode is True:                 # mode pdf renderer
            self.button_annuler.visible = False
            self.button_trombi.visible = False
        
        #lecture du fichier père stages
        stage_row = app_tables.stages.get(  q.fetch_only("code_txt"),
                                            numero=int(num_stage))    
        stagiaires_liste =  app_tables.stagiaires_inscrits.search(   q.fetch_only("name", "prenom", 
                                                                                  user_email=q.fetch_only()),
                                                                    tables.order_by("name", ascending=True),
                                                                    stage=stage_row
                                                                )
        self.repeating_panel_1.items = stagiaires_liste
        """ Je peux créer une liste à partir de l'objet créé par search ( avec list() )
             et accéder ensuite à chaque row et column:
             
        list1=list(app_tables.stagiaires_inscrits.search(
            tables.order_by("name", ascending=True),
            stage=stage_row
        ))
        
        print(list1)
        print(list1[0]['name'])     row 1, column 'nom'
        """

        cod = stage_row["code_txt"]
        date = str(stage_row["date_debut"].strftime("%d/%m/%Y"))
        self.label_titre.text = "Fiches stagiaires " + cod + " du " + date + "   (num " +num_stage+")"

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form(self.f)

    def button_trombi_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_trombi import Visu_trombi
        open_form('Visu_trombi',self.num_stage, self.intitule)

