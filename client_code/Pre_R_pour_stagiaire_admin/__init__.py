from ._anvil_designer import Pre_R_pour_stagiaire_adminTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
#global user_pr
#user_pr = anvil.users.get_user()

class Pre_R_pour_stagiaire_admin(Pre_R_pour_stagiaire_adminTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.label_1.text = "Gestion des pré-Requis"
        # Drop down stages 
        liste0 = app_tables.stages.search(tables.order_by("date_debut", ascending=False))
        print("nb; ", len(liste0))
        liste_drop_d = []
        for row in liste0:
            #lecture fichier père type de stage
            type=app_tables.codes_stages.get(code=row['code']['code'])
            liste_drop_d.append((type['code']+"  du "+str(row['date_debut']), row))
        print(liste_drop_d)
        self.drop_down_code_stage.items = liste_drop_d

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main')

    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        row_stage = self.drop_down_code_stage.selected_value   # Stage sélectionné du user ds drop_down (row table stagiaire inscrit)

        # lecture des stagiaires de ce stage
        liste_stagiaires = app_tables.stagiaires_inscrits.search(stage=row_stage
                                                         )
        self.repeating_panel_1.items = liste_stagiaires
