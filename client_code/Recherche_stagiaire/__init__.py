from ._anvil_designer import Recherche_stagiaireTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Recherche_stagiaire(Recherche_stagiaireTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        # j'affiche tous les stagiaires
        self.repeating_panel_1.items = app_tables.users.search(
                tables.order_by("nom", ascending=True)
                )
    def text_box_nom_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.filtre()
    def text_box_prenom_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.filtre()
    def text_box_tel_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.filtre()
    def text_box_email_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.filtre()
    
    def filtre(self):
        # Récupération des critères
        c_nom = self.text_box_nom.text + "%"       # critere nom
        c_prenom = self.text_box_prenom.text + "%"  # critere prenom
        c_email = self.text_box_email.text + "%"  # critere email
        c_tel = self.text_box_tel.text + "%"  # critere tel
        
        # création de la liste triée par nom qui répond aux critères
        self.repeating_panel_1.items = app_tables.users.search(
                tables.order_by("nom", ascending=True),
                q.all_of                  # all of queries must match
                (
                    nom=q.ilike(c_nom),       # ET
                    prenom=q.ilike(c_prenom),  # ET
                    email=q.ilike(c_email),    # ET
                    tel=q.ilike(c_tel),    # ET
                )
            )


