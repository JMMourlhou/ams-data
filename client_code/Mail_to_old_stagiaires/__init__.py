from ._anvil_designer import Mail_to_old_stagiairesTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Mail_to_old_stagiaires(Mail_to_old_stagiairesTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # lecture de tous les anciens stagiaires
        self.liste_old_stagiaires = app_tables.stagiaires_histo.search()
        self.repeating_panel_1.items = self.liste_old_stagiaires

    def button_mailing_click(self, **event_args):
        """This method is called when the button is clicked"""
        liste_email = []
        for stagiaire in self.liste_old_stagiaires:
            #lecture table user
            liste_email.append((stagiaire["mail"], stagiaire["prenom"]))
            
        # 'formul' indique l'origine, ici 'formulaire de satisfaction'
        open_form("Mail_subject_attach_txt",  liste_email, 'formul') 

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)
        