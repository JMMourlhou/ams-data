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
        row = self.drop_down_code_stages.selected_value  # row du stage
        if row is None:
            alert("Vous devez sélectionner un stage !")
            self.drop_down_code_stage.focus()
            return
        #self.label_titre.text = row["code_txt"]+" du "+str(row["date_debut"]
        self.label_titre.text = row
        dico_rep_ferm = {}
        dico_rep_ouv = {}

        # Création des dico des réponses cumulées
        rep0_cumul = {}                                                 
        rep0_cumul["1"] =  0        # Cumul des réponses 0, question 1   # Cumil Réponses 0 pour question 1
        rep0_cumul["2"] =  0        # Cumul des réponses 0, question 2  
        rep0_cumul["3"] =  0        # Cumul des réponses 0, question 3   
        rep0_cumul["4"] =  0        # Cumul des réponses 0, question 4   
        rep0_cumul["5"] =  0        # Cumul des réponses 0, question 5   
        rep0_cumul["6"] =  0        # Cumul des réponses 0, question 6   
        rep0_cumul["7"] =  0        # Cumul des réponses 0, question 7   
        rep0_cumul["8"] =  0        # Cumul des réponses 0, question 8   
        rep0_cumul["9"] =  0        # Cumul des réponses 0, question 9   
        rep0_cumul["10"] =  0        # Cumul des réponses 0, question 10   

        # Création des dico des réponses cumulées
        rep1_cumul = {}                                                 # Cumul Réponses 1 pour question 2
        rep1_cumul["1"] =  0        # Cumul des réponses 0, question 1   
        rep1_cumul["2"] =  0        # Cumul des réponses 0, question 2  
        rep1_cumul["3"] =  0        # Cumul des réponses 0, question 3   
        rep1_cumul["4"] =  0        # Cumul des réponses 0, question 4   
        rep1_cumul["5"] =  0        # Cumul des réponses 0, question 5   
        rep1_cumul["6"] =  0        # Cumul des réponses 0, question 6   
        rep1_cumul["7"] =  0        # Cumul des réponses 0, question 7   
        rep1_cumul["8"] =  0        # Cumul des réponses 0, question 8   
        rep1_cumul["9"] =  0        # Cumul des réponses 0, question 9   
        rep1_cumul["10"] =  0        # Cumul des réponses 0, question 10   

        # Création des dico des réponses cumulées
        rep2_cumul = {}                                                 # Cumul Réponses 2
        rep2_cumul["1"] =  0        # Cumul des réponses 0, question 1   
        rep2_cumul["2"] =  0        # Cumul des réponses 0, question 2  
        rep2_cumul["3"] =  0        # Cumul des réponses 0, question 3   
        rep2_cumul["4"] =  0        # Cumul des réponses 0, question 4   
        rep2_cumul["5"] =  0        # Cumul des réponses 0, question 5   
        rep2_cumul["6"] =  0        # Cumul des réponses 0, question 6   
        rep2_cumul["7"] =  0        # Cumul des réponses 0, question 7   
        rep2_cumul["8"] =  0        # Cumul des réponses 0, question 8   
        rep2_cumul["9"] =  0        # Cumul des réponses 0, question 9   
        rep2_cumul["10"] =  0        # Cumul des réponses 0, question 10   
        
         # Création des dico des réponses cumulées
        rep3_cumul = {}                                                 # Cumil Réponses 3
        rep3_cumul["1"] =  0        # Cumul des réponses 0, question 1   
        rep3_cumul["2"] =  0        # Cumul des réponses 0, question 2  
        rep3_cumul["3"] =  0        # Cumul des réponses 0, question 3   
        rep3_cumul["4"] =  0        # Cumul des réponses 0, question 4   
        rep3_cumul["5"] =  0        # Cumul des réponses 0, question 5   
        rep3_cumul["6"] =  0        # Cumul des réponses 0, question 6   
        rep3_cumul["7"] =  0        # Cumul des réponses 0, question 7   
        rep3_cumul["8"] =  0        # Cumul des réponses 0, question 8   
        rep3_cumul["9"] =  0        # Cumul des réponses 0, question 9   
        rep3_cumul["10"] =  0        # Cumul des réponses 0, question 10   

        # Création des dico des réponses cumulées
        rep4_cumul = {}                                                 # Cumul Réponses 4
        rep4_cumul["1"] =  0        # Cumul des réponses 0, question 1   
        rep4_cumul["2"] =  0        # Cumul des réponses 0, question 2  
        rep4_cumul["3"] =  0        # Cumul des réponses 0, question 3   
        rep4_cumul["4"] =  0        # Cumul des réponses 0, question 4   
        rep4_cumul["5"] =  0        # Cumul des réponses 0, question 5   
        rep4_cumul["6"] =  0        # Cumul des réponses 0, question 6   
        rep4_cumul["7"] =  0        # Cumul des réponses 0, question 7   
        rep4_cumul["8"] =  0        # Cumul des réponses 0, question 8   
        rep4_cumul["9"] =  0        # Cumul des réponses 0, question 9   
        rep4_cumul["10"] =  0        # Cumul des réponses 0, question 10   

        # Création des dico des réponses cumulées
        rep5_cumul = {}                                                 # Cumul Réponses 5
        rep5_cumul["1"] =  0        # Cumul des réponses 0, question 1   
        rep5_cumul["2"] =  0        # Cumul des réponses 0, question 2  
        rep5_cumul["3"] =  0        # Cumul des réponses 0, question 3   
        rep5_cumul["4"] =  0        # Cumul des réponses 0, question 4   
        rep5_cumul["5"] =  0        # Cumul des réponses 0, question 5   
        rep5_cumul["6"] =  0        # Cumul des réponses 0, question 6   
        rep5_cumul["7"] =  0        # Cumul des réponses 0, question 7   
        rep5_cumul["8"] =  0        # Cumul des réponses 0, question 8   
        rep5_cumul["9"] =  0        # Cumul des réponses 0, question 9   
        rep5_cumul["10"] =  0        # Cumul des réponses 0, question 10

        # lecture des formulaires du stage choisi
        cpt_formulaire = 0
        liste_formulaires = app_tables.stage_satisf.search(stage_row=row)
        print(len(liste_formulaires), 'formulaires à traiter')
        
        for formulaire in liste_formulaires:
            cpt_formulaire += 1
            print("==========================FORMULAIRE", cpt_formulaire)
            # dico questions fermées
            dico_rep_ferm = formulaire["rep_dico_rep_ferm"]  # dico questions fermées du formulaire
            nb_questions_ferm = len(dico_rep_ferm) #nb questions ds formulaire questions fermées 
            print("nb_q_fermées: ", nb_questions_ferm)
            
            # dico questions ouvertes
            dico_rep_ouv = formulaire["rep_dico_rep_ouv"]   # dico questions ouvertes du formulaire
            nb_questions_ouv = len(dico_rep_ouv)
            print("nb_q_ouvertes: ", nb_questions_ouv)
            
            # Boucle sur le dictionaire fermé du formulaire
            # ex du contenu du dico en table qd lu:   ('1', ["Conditions d'accueil sur les lieux de formation:", 0])
            #                                          cle   valeur
            #                             indices valeur;    0                                                    1
            #                                                tuple [question, reponse]    
            for cle, val in dico_rep_ferm.items():     
                reponse = val[1]  # indice 1: donc reponse (int)
                
                for q in range(1,nb_questions_ferm+1): # boucle sur nb questionsfermées de 1 à nb_questions_fermées (exclusif)
                    question = str(q) # transorme q (int) en question str
                    #print("======= QUESTION N° ", question)
                    if cle == question:  # ex si question 1        
                        print("cle/question: ",cle)
                        print("valeur/reponse: ",reponse)
                        if reponse == 0:                                  # le stagiaire a répondu 0 à la question 
                            # lecture dico des cumuls pour la question, réponse 0
                            temp = int(rep0_cumul[str(question)])
                            temp += 1    # cumul de la reponse 0    à la question 
                            rep0_cumul[str(question)]=temp
                            print(rep0_cumul[str(question)])
                        if reponse == 1:                                  # le stagiaire a répondu 1 à la question 
                            # lecture dico des cumuls pour la question, réponse 0
                            temp = int(rep1_cumul[str(question)])
                            temp += 1    # cumul de la reponse 1    à la question 
                            rep1_cumul[str(question)]=temp
                            print(rep1_cumul[str(question)])     
                        if reponse == 2:                                  # le stagiaire a répondu 2 à la question 
                            # lecture dico des cumuls pour la question, réponse 0
                            temp = int(rep2_cumul[str(question)])
                            temp += 1    # cumul de la reponse 2    à la question 
                            rep2_cumul[str(question)]=temp
                            print(rep2_cumul[str(question)]) 
                        if reponse == 3:                                  # le stagiaire a répondu 3 à la question 
                            # lecture dico des cumuls pour la question, réponse 0
                            temp = int(rep3_cumul[str(question)])
                            temp += 1    # cumul de la reponse 3    à la question 
                            rep3_cumul[str(question)]=temp
                            print(rep3_cumul[str(question)]) 
                        if reponse == 4:                                  # le stagiaire a répondu 4 à la question 
                            # lecture dico des cumuls pour la question, réponse 0
                            temp = int(rep4_cumul[str(question)])
                            temp += 1    # cumul de la reponse 3    à la question 
                            rep4_cumul[str(question)]=temp
                            print(rep4_cumul[str(question)]) 
                        if reponse == 5:                     # le stagiaire a répondu 5 à la question 
                            # lecture dico des cumuls pour la question, réponse 0
                            temp = int(rep5_cumul[str(question)])
                            temp += 1    # cumul de la reponse 3    à la question 
                            rep5_cumul[str(question)]=temp
                            print("cumul5 ", rep5_cumul[str(question)]) 
                    
        print(f"Résultat pour les {len(liste_formulaires)} formulaires:")  
        print("nb de rep 0/1: ", rep0_cumul["1"])
        print("nb de rep 1/1: ", rep1_cumul["1"])
        print("nb de rep 2/1: ", rep2_cumul["1"])
        print("nb de rep 3/1: ", rep3_cumul["1"])
        print("nb de rep 4/1: ", rep4_cumul["1"])
        print("nb de rep 5/1: ", rep5_cumul["1"])
        print()
        print("nb de rep 0/2: ", rep0_cumul["2"])
        print("nb de rep 1/2: ", rep1_cumul["2"])
        print("nb de rep 2/2: ", rep2_cumul["2"])
        print("nb de rep 3/2: ", rep3_cumul["2"])
        print("nb de rep 4/2: ", rep4_cumul["2"])
        print("nb de rep 5/2: ", rep5_cumul["2"])
        print()
        print("nb de rep 0/3: ", rep0_cumul["3"])
        print("nb de rep 1/3: ", rep1_cumul["3"])
        print("nb de rep 2/3: ", rep2_cumul["3"])
        print("nb de rep 3/3: ", rep3_cumul["3"])
        print("nb de rep 4/3: ", rep4_cumul["3"])
        print("nb de rep 5/3: ", rep5_cumul["3"])
        print()
        print("nb de rep 0/4: ", rep0_cumul["4"])
        print("nb de rep 1/4: ", rep1_cumul["4"])
        print("nb de rep 2/4: ", rep2_cumul["4"])
        print("nb de rep 3/4: ", rep3_cumul["4"])
        print("nb de rep 4/4: ", rep4_cumul["4"])
        print("nb de rep 5/4: ", rep5_cumul["4"])
        print()
        print("nb de rep 0/5: ", rep0_cumul["5"])
        print("nb de rep 1/5: ", rep1_cumul["5"])
        print("nb de rep 2/5: ", rep2_cumul["5"])
        print("nb de rep 3/5: ", rep3_cumul["5"])
        print("nb de rep 4/5: ", rep4_cumul["5"])
        print("nb de rep 5/5: ", rep5_cumul["5"])
        print()
        print("nb de rep 0/6: ", rep0_cumul["6"])
        print("nb de rep 1/6: ", rep1_cumul["6"])
        print("nb de rep 2/6: ", rep2_cumul["6"])
        print("nb de rep 3/6: ", rep3_cumul["6"])
        print("nb de rep 4/6: ", rep4_cumul["6"])
        print("nb de rep 5/6: ", rep5_cumul["6"])







    
            
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)
