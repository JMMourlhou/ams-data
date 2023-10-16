from ._anvil_designer import Recherche_stagiaireTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from itertools import chain


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
                tables.order_by("nom", ascending=True),
                admin =q.not_(True)    # on n'affiche pas l'admin !
                )
    def text_box_nom_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.drop_down_code_stage.selected_value = None
        self.drop_down_num_stages.visible = False
        self.filtre()
    def text_box_prenom_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.drop_down_code_stage.selected_value = None
        self.drop_down_num_stages.visible = False
        self.filtre()
    def text_box_tel_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.drop_down_code_stage.selected_value = None
        self.drop_down_num_stages.visible = False
        self.filtre()
    def text_box_email_change(self, **event_args):
        """This method is called when the text in this text box is edited"""
        self.drop_down_code_stage.selected_value = None
        self.drop_down_num_stages.visible = False
        self.filtre()
    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        
        self.text_box_nom.text=""       # critere nom
        self.text_box_prenom.text=""  # critere prenom
        self.text_box_email.text=""  # critere email
        self.text_box_tel.text=""  # critere tel
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
                    admin =q.not_(True)    # on n'affiche pas l'admin !
                )
            )
    def filtre_type_stage(self):
        # Récupération du critère stage
        row_type = self.drop_down_code_stage.selected_value
        #if row_type == None :
        #    alert("Sélectionnez le type de stage !")
        #    return
        #lecture du fichier stages et sélection des stages correspond au type de stage choisit
        
        list1 = app_tables.stages.search(code=row_type)     # recherche ds les stages
        if len(list1)==0:
            alert("Pas de stage de ce type enregistré")
        print("nb de stage de ce type: ",len(list1))
        
        # Initialisation du Drop down num_stages et dates
        self.drop_down_num_stages.items = [(str(r['date_debut'])+" / "+str(r['numero']), r) for r in list1]
        self.drop_down_num_stages.visible = True
        """
        for r in self.drop_down_num_stages.items:           # Je peux boucler ds ma dropdown
            print(r, r[0], r[1])                            # je peux extraire 0 ce qui est affiché, 1 row stage
        """    
        #affichage de tous les stagiaires de ces stages du type choisit
        liste_intermediaire1=[]
        for st in list1:               # boucle sur les stages de même type (ex psc1)                
            date = st["date_debut"]    #DATE DU STAGE
            # lecture du fichier stagiaires_inscrits sur le stage et création d'1 liste par stage
            temp =  app_tables.stagiaires_inscrits.search(
                        tables.order_by("name", ascending=True),
                        stage=st
                    )
            liste_intermediaire1.append(temp)   # ajout de la liste (iterator object)du stage
            
        print("nb de listes créées: ",len(liste_intermediaire1))
        
        # Je crée 1 liste à partir de ttes les listes créées:
        liste_finale = []
        for l in liste_intermediaire1:    #pour chaque liste iterator object
            for row in l:                      # pour chaque stagiaire du stage
                liste_finale.append(row)
        self.repeating_panel_1.items = liste_finale

    def drop_down_num_stages_change(self, **event_args):
        """This method is called when an item is selected"""
        selection=self.drop_down_num_stages.selected_value
        print("selection: ",selection)
        #extraction du num stage
        self.repeating_panel_1.items = app_tables.stagiaires_inscrits.search(
                                        tables.order_by("name", ascending=True),
                                        stage=selection
                                      )


    def button_retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def text_box_nom_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        pass






