from ._anvil_designer import Stage_satisf_statisticsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Stage_satisf_statistics(Stage_satisf_statisticsTemplate):
    def __init__(
        self, **properties
    ):  
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.

        # import anvil.js    # pour screen size
        from anvil.js import window  # to gain access to the window object

        global screen_size
        screen_size = window.innerWidth

        
        # Drop down codes stages
        #création du dictionaire des stages ds tables formulaires de satisfaction
        liste_stage = [] # cette liste me permet de tester l'existence du num stage ds celle-ci
        
        liste_formulaires = app_tables.stage_satisf.search(q.fetch_only("stage_num_txt","stage_row"))                                                              
        print(len(liste_formulaires), 'formulaires lus')
        for formulaire in liste_formulaires:
            test_num_stage = formulaire['stage_num_txt']
            if test_num_stage not in liste_stage: #le stage n'existe pas encore ds la liste, le l'ajoute
                liste_stage.append(test_num_stage) 
        print(len(liste_stage), "stage(s)")
        
        # création de la drop down
        liste_stage_drop_down = []
        for stage in liste_stage:
            row_stage = app_tables.stages.get(numero=int(stage))
            if row_stage:
                liste_stage_drop_down.append((row_stage["code_txt"]+" du "+str(row_stage["date_debut"]),row_stage))
        self.drop_down_code_stages.items = liste_stage_drop_down
        

    def drop_down_code_stages_change(self, **event_args):
        """This method is called when an item is selected"""
        row = self.drop_down_code_stages.selected_value  # row du pre_requis
        if row is None:
            alert("Vous devez sélectionner un stage !")
            self.drop_down_code_stage.focus()
            return
        # lecture des formulaires du stage choisi
        liste_formulaires = app_tables.stage_satisf.search(stage_row=row)
        print(len(liste_formulaires), 'formulaires à traiter')
        #cumuls
        nb_rep_0 = 0
        nb_rep_1 = 0
        nb_rep_2 = 0
        nb_rep_3 = 0
        nb_rep_4 = 0
        nb_rep_5 = 0
        dico_rep_fermées = {}
        dico_rep_ouvertes = {}
        
        for formulaire in liste_formulaires:
            # dico questions fermées
            dico_rep_ferm = formulaire["rep_dico_rep_ferm"]
            # dico questions ouvertes
            dico_rep_ouv = formulaire["rep_dico_rep_ferm"]
            
            for cle in dico_rep_ferm.items():
                resultat = cle="1"
                if cle["1"] == "0": 
                    nb_rep_0 += 1
            print("nb de rep 0: ",  nb_rep_0)






    
            
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)
