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
        self.drop_down_code_stage.tag.etat=False
        # Drop down codes stages
        self.drop_down_code_stage.items = [(r['code'], r) for r in app_tables.codes_stages.search()]
        
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
    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        self.drop_down_code_stage.tag.etat=True
        self.filtre_type_stage()   
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
    def filtre_type_stage(self):
        # Récupération du critère stage
        row_type = self.drop_down_code_stage.selected_value
        if row_type == None :
            alert("Sélectionnez le type de stage !")
            return
        #lecture du fichier stages et sélection des stages correspond au type choisit
        list1 = app_tables.stages.search(type=row_type)
        if len(list1)==0:
            alert("pas de stage de ce type")

        # Initialisation du Drop down num_stages
        self.drop_down_num_stages.items = [(str(r['date_debut']), r) for r in list1]
        self.drop_down_num_stages.visible = True
        """
        #affichage de tous les stagiaires de ces stages du type choisit
        list = []
        for stage in liste1:
            # lecture du contenu de chaque stage de ce type et sauvegarde de la liste
            temp=app_tables.stagiaires_inscrits.search(
                tables.order_by("nom", ascending=True),
                stage=liste1
            )
            list.extend(temp)   #pour chaque stage sélectionné, rajoute les stagiaires inscrits à la fin de list, 
           
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
        """

    def drop_down_num_stages_change(self, **event_args):
        """This method is called when an item is selected"""
        pass

    def button_retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)





