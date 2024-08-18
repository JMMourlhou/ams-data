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
        from ..Pre_R_MAJ_table import Pre_R_MAJ_table
        open_form("Pre_R_MAJ_table")

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
        self.button_maj_pr.visible = False
        self.button_gestion_pre_requis.visible = False
        liste = app_tables.stages.search(q.fetch_only("code"),
                                                     tables.order_by("code_txt", ascending=True),
                                                     tables.order_by("date_debut", ascending=True)
                                        )
        liste_dp=[]
        for stage in liste:
            if stage['numero']<1000:  # si stage type stagiaire, je rajoute la date
                liste_dp.append((stage['code']['code']+" du "+str(stage['date_debut']),stage))
            else:                     # si stage type formateur, je ne rajoute pas la date
                liste_dp.append((stage['code']['code'],stage))  
        self.drop_down_code_stage.items = liste_dp 
        self.column_panel_pr_par_personne.visible = True 
        
    # STAGE SELECTIONNE, INITIALISATION DU DROP DOWN DES PERSONNES DS CE STAGE (stagiaires inscrits)
    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        self.stage_row = self.drop_down_code_stage.selected_value
        self.drop_down_personnes.items = [
                                           (r["name"]+" "+r["prenom"], r) for r in app_tables.stagiaires_inscrits.search(q.fetch_only("stage","user_email"),
                                                                                                                        tables.order_by("name", ascending=True),
                                                                                                                        numero=self.stage_row['numero']
                                                                                                                         )
                                         ]
        self.drop_down_personnes.visible = True
        
        

    def drop_down_personnes_change(self, **event_args):
        """This method is called when an item is selected"""
        stagiaire_inscrit_row = self.drop_down_personnes.selected_value
        from ..Pre_R_pour_1_stagiaire import Pre_R_pour_1_stagiaire
        open_form('Pre_R_pour_1_stagiaire',stagiaire_inscrit_row)

    def button_mails_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Mail_subject_attach_txt import Mail_subject_attach_txt
        open_form("Mail_subject_attach_txt",[],"")

    def button_create_qcm_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..QCM_visu_modif import QCM_visu_modif
        open_form("QCM_visu_modif_Main")
 
