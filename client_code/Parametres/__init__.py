from ._anvil_designer import ParametresTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Parametres(ParametresTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.

    def button_maj_pr_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Table_Pre_R_MAJ import Table_Pre_R_MAJ
        open_form("Table_Pre_R_MAJ")

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99) 

    def button_gestion_pre_requis_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Pre_R_pour_type_stage import Pre_R_pour_type_stage
        open_form('Pre_R_pour_type_stage')

    # PRE REQUIS PERSONNALISé SELECTIONNé, INITIALISATION de DROP DOWN DE TOUS LES STAGES EXISTANTS
    def button_gestion_pre_requis_personnel_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.drop_down_code_stage.items = [(r['code']['code']+' du '+str(r['date_debut']), r) for r in app_tables.stages.search(q.fetch_only("code"),
                                                                                                                                tables.order_by("code_txt", ascending=True),
                                                                                                                                tables.order_by("date_debut", ascending=True)
                                                                                                                               )]
        self.column_panel_pr_par_personne.visible = True  

    # STAGE SELECTIONNE, INITIALISATION DU DROP DOWN DES PERSONNES DS CE STAGE (stagiaires inscrits)
    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        self.stage_row = self.drop_down_code_stage.selected_value
        self.drop_down_personnes.items = [
                                           (r["name"]+" "+r["prenom"], r) for r in app_tables.stagiaires_inscrits.search(q.fetch_only("stage","user_email"),
                                                                                                                        tables.order_by("name", ascending=True),
                                                                                                                        stage_txt=self.stage_row["code"]['code']
                                                                                                                         )
                                         ]
        
        

    def drop_down_personnes_change(self, **event_args):
        """This method is called when an item is selected"""
        stagiaire_inscrit_row = self.drop_down_personnes.selected_value
        from ..Pre_R_pour_1_stagiaire import Pre_R_pour_1_stagiaire
        open_form('Pre_R_pour_1_stagiaire',stagiaire_inscrit_row)
 
