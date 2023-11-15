from ._anvil_designer import Pre_R_pour_stagiaireTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global user_pr
user_pr = anvil.users.get_user()

class Pre_R_pour_stagiaire(Pre_R_pour_stagiaireTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        global user_pr
        if user_pr:
            self.label_1.text = "Documents à fournir pour " + user_pr['prenom'] + " " + user_pr['nom']
            # Drop down stages inscrits du user
            liste0 = app_tables.stagiaires_inscrits.search(user_email=user_pr)
            print("nb; ", len(liste0))
            liste_drop_d = []
            for row in liste0:
                #lecture fichier père stage
                stage=app_tables.stages.get(numero=row['stage']['numero'])
                #lecture fichier père type de stage
                type=app_tables.codes_stages.get(code=stage['code']['code'])
                liste_drop_d.append((type['code']+"  du "+str(stage['date_debut']), row))
            print(liste_drop_d)
            self.drop_down_code_stage.items = liste_drop_d

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main')

    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        row_stagiaire_inscrit = self.drop_down_code_stage.selected_value   # Stage sélectionné du user ds drop_down (row table stagiaire inscrit)
        
        # lecture fichier père stages
        row_stage = app_tables.stages.get(numero=row_stagiaire_inscrit['stage']['numero'])
        # lecture des pré requis pour ce stage et pour ce stagiaire
        global user_pr
        liste_pr = app_tables.pre_requis_stagiaire.search(stagiaire_email=user_pr,
                                                         stage_num=row_stage
                                                         )
        self.repeating_panel_1.items = liste_pr
        
