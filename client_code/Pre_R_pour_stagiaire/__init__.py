from ._anvil_designer import Pre_R_pour_stagiaireTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Pre_R_pour_stagiaire(Pre_R_pour_stagiaireTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        user=anvil.users.get_user()
        if user:
            print(user['email'])
            # Drop down stages inscrits
            liste0 = app_tables.stagiaires_inscrits.search(user_email=user)
            liste_drop_d = []
            for row in liste0:
                #lecture fichier père stage
                stage=app_tables.stages.get(numero=row['stage']['numero'])
                #lecture fichier père type de stage
                type=app_tables.codes_stages.get(code=stage['code']['code'])
                liste_drop_d.append((type['code']+"  du "+str(stage['date_debut']), row))
            print(liste_drop_d)
            self.drop_down_code_stage.items = liste_drop_d
            #self.drop_down_code_stage.items = [(r['stage'], r) for r in app_tables.stagiaires_inscrits.search() if ['user_email'] == user['email']]
            

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main')

    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        pass
