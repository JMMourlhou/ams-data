from ._anvil_designer import Recherche_stagiaireTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Recherche_stagiaire(Recherche_stagiaireTemplate):
    def __init__(self, inscript="recherche", **properties):       # inscript="inscription" si vient de visu_stages pour inscription d'1 stagiare
         
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        
        self.inscription = inscript
        if self.inscription != "recherche":   # inscription/num_stage
            self.drop_down_code_stage.visible = False
            self.drop_down_num_stages.visible = False
        
        # Drop down codes stages
        self.drop_down_code_stage.items = [(r['code'], r) for r in app_tables.codes_stages.search()]

    def filtre(self):
        # Récupération des critères
        c_role = self.text_box_role.text + "%"          # critère role
        c_nom = self.text_box_nom.text + "%"            #         nom
        c_prenom = self.text_box_prenom.text + "%"      #         prenom
        c_email = self.text_box_email.text + "%"        #         email
        c_tel = self.text_box_tel.text + "%"            #         tel
        
        # Nom    
        if self.text_box_nom.text != "" and self.text_box_email.text == "" and self.text_box_tel.text == "" and self.text_box_prenom.text == "" and self.text_box_role.text == "" :
            self.repeating_panel_1.items = anvil.server.call("search_on_name_only", c_nom)
        # Prénom
        if self.text_box_prenom.text != "" and self.text_box_email.text == "" and self.text_box_tel.text == "" and self.text_box_nom.text == "" and self.text_box_role.text == "":   
            self.repeating_panel_1.items = anvil.server.call("search_on_prenom_only", c_prenom)
        # Role
        if self.text_box_role.text != "" and self.text_box_nom.text == "" and self.text_box_prenom.text == "" :   
            self.repeating_panel_1.items = anvil.server.call("search_on_role_only", c_role)
        # Role & Nom
        if self.text_box_role.text != "" and self.text_box_nom.text != "" and self.text_box_prenom.text == "" :   
            self.repeating_panel_1.items = anvil.server.call("search_on_role_nom", c_role, c_nom)
        # Nom & Prénom
        if self.text_box_role.text == "" and self.text_box_nom.text != "" and self.text_box_prenom.text != "" :   
            self.repeating_panel_1.items = anvil.server.call("search_on_nom_prenom", c_nom, c_prenom)

        
        # Role & Nom & Prénom
        if self.text_box_role.text != "" and self.text_box_nom.text != "" and self.text_box_prenom.text != "" :   
            self.repeating_panel_1.items = anvil.server.call("search_on_role_nom_prenom", c_role, c_nom, c_prenom)

        
        # Tel
        if self.text_box_tel.text != "" and self.text_box_email.text == "" and self.text_box_nom.text == "" and self.text_box_prenom.text == "" and self.text_box_role.text == "" :  
            self.repeating_panel_1.items = anvil.server.call("search_on_tel_only", c_tel)
        # Mail
        if self.text_box_email.text != "" and self.text_box_tel.text == "" and self.text_box_nom.text == "" and self.text_box_prenom.text == "" and self.text_box_role.text == "" :  
            self.repeating_panel_1.items = anvil.server.call("search_on_email_only", c_email)
        
    def filtre_type_stage(self):
        # Récupération du critère stage
        row_type = self.drop_down_code_stage.selected_value

        #lecture du fichier stages et sélection des stages correspond au type de stage choisit
        list1 = app_tables.stages.search(q.fetch_only("date_debut", "numero"),       # recherche ds les stages
                                            code=row_type)                        
        if len(list1)==0:
            from anvil import open_form       # j'initialise la forme principale avec le choix du qcm ds la dropdown
            open_form("Recherche_stagiaire") 
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
            #date = st["date_debut"]    #DATE DU STAGE
            # lecture du fichier stagiaires_inscrits sur le stage et création d'1 liste par stage
            temp =  app_tables.stagiaires_inscrits.search(  q.fetch_only(),
                                                            tables.order_by("name", ascending=True),
                                                            stage=st
                                                         )
            liste_intermediaire1.append(temp)   # ajout de la liste (iterator object)du stage
            
        #print("nb de listes créées: ",len(liste_intermediaire1))
        
        # Je crée 1 liste à partir de ttes les listes créées:
        liste_finale = []
        for l in liste_intermediaire1:    #pour chaque liste iterator object
            for row in l:                      # pour chaque stagiaire du stage
                liste_finale.append(row)
        self.repeating_panel_1.items = liste_finale

    def drop_down_num_stages_change(self, **event_args):
        """This method is called when an item is selected"""
        selection=self.drop_down_num_stages.selected_value
        #print("selection: ",selection)
        #extraction du num stage
        self.repeating_panel_1.items = app_tables.stagiaires_inscrits.search(
                                        tables.order_by("name", ascending=True),
                                        stage=selection
                                      )

    def button_retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def button_recherche_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.drop_down_code_stage.selected_value = None
        self.drop_down_num_stages.visible = False
        self.filtre()

    def button_efface_click(self, **event_args):    # # j'efface les critères
        """This method is called when the button is clicked"""
        open_form('Recherche_stagiaire')
       





  









