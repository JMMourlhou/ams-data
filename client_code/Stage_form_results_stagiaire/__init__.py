from ._anvil_designer import Stage_form_results_stagiaireTemplate
from .. import French_zone  # POur acquisition de date et heure Francaise (Browser time)
from anvil import *

import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

global nb_questions_ferm  # nb questions fermées (check 0 à 5)
nb_questions_ferm = 0
global nb_questions_ouvertes  # nb questions ouvertes
nb_questions_ouvertes = 0


class Stage_form_results_stagiaire(Stage_form_results_stagiaireTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.column_panel_header.tag = "header"
        """
        self.column_panel_0.tag = 0
        self.column_panel_1.tag = 1
        self.column_panel_2.tag = 2
        self.column_panel_3.tag = 3
        self.column_panel_4.tag = 4
        self.column_panel_5.tag = 5
        self.column_panel_6.tag = 6
        self.column_panel_7.tag = 7
        self.column_panel_8.tag = 8
        self.column_panel_9.tag = 9
        self.column_panel_10.tag = 10

        self.column_panel_a1.tag = 0
        self.column_panel_a2.tag = 0
        self.column_panel_a3.tag = 0
        self.column_panel_a4.tag = 0
        self.column_panel_a5.tag = 0
        self.column_panel_a6.tag = 0
        self.column_panel_a7.tag = 0
        self.column_panel_a8.tag = 0
        self.column_panel_a9.tag = 0
        self.column_panel_a10.tag = 0
       
        self.label_1.tag = "label"
        self.label_2.tag = "label"
        self.label_3.tag = "label"
        self.label_4.tag = "label"
        self.label_5.tag = "label"
        self.label_6.tag = "label"
        self.label_7.tag = "label"
        self.label_8.tag = "label"
        self.label_9.tag = "label"
        self.label_10.tag = "label"
        """
        user = anvil.users.get_user()
        if user:
            # Initilistaion de la drop down dates 
            self.liste0 = app_tables.com.search(user=user)
            print("nb de dates où le stagiaire est intervenu ; ", len(self.liste0))
            if len(self.liste0) > 0: 
                liste_drop_d = []
                for row in self.liste0:
                    liste_drop_d.append((row["date"],row ))
                # print(liste_drop_d)
                self.drop_down_date.items = liste_drop_d

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form("Main", 99)

    def drop_down_date_change(self, **event_args):
        """This method is called when an item is selected"""
        self.date = self.drop_down_date.selected_value
        if self.date is None:
            alert("Vous devez sélectionner une date !")
            self.drop_down_date.focus()
            return
        # sélection des formulaires saisis à la date sélectionnée
        liste_formulaires = app_tables.com.search(date=self.date["date"])
        nb_formulaires = len(liste_formulaires)
        max_points_ferm = nb_formulaires * 6      # max de points possibles pour une question
        alert(f"max points fermés: {max_points_ferm}")
        #  ================================================================  Affichage résultats
        # extraction du stage par lecture du premier formulaire de la liste
        first_row = liste_formulaires[0]
        stage_row = first_row["stage_row"]
        # extraction des 2 dictionnaires du stage
        dico_q_ferm = stage_row["com_ferm"]
        dico_q_ouv = stage_row["com_ouv"]
        # nb_questions_ferm  
        nb_questions_ferm = int(dico_q_ferm["NBQ"])  # nb de questions fermées ds le dico
        #alert(f"nb de questions ferm : {nb_questions_ferm}")
        # nb_questions_ouv
        nb_questions_ouv = int(dico_q_ouv["NBQ"])  # nb de questions fermées ds le dico
        #alert(f"nb de question ouv: {nb_questions_ouv}")

        
        # =========================== Boucle sur tous les formulaires pour les questions fermées
        # initialisation des compteurs
        points_q1 = 0
        points_q2 = 0
        points_q3 = 0
        points_q4 = 0
        points_q5 = 0
        points_q6 = 0
        points_q7 = 0
        points_q8 = 0
        points_q9 = 0
        points_q10 = 0
        
        # boucle
        for formulaire in liste_formulaires:
            dico_ferm = formulaire["com_ferm"]   # dico fermé du formulaire
            
            points_q1 = points_q1 + dico_ferm["1"][1] + 1 # cumul 1ere question  + 1 car mini = 0, max = 5
            #alert(f"cumul q1: {points_q1}")
            points_q2 = points_q2 + dico_ferm["2"][1] + 1  # cumul 2eme question
            #alert(f"cumul q2: {points_q2}")
            points_q3 = points_q3 + dico_ferm["3"][1] + 1 # cumul 3eme question
            #alert(f"cumul q3: {points_q3}")
            points_q4 = points_q4 + dico_ferm["4"][1] + 1 # cumul 4eme question
            #alert(f"cumul q4: {points_q4}")
            points_q5 = points_q5 + dico_ferm["5"][1] + 1 # cumul 5eme question
            #alert(f"cumul q5: {points_q5}")
            points_q6 = points_q6 + dico_ferm["6"][1] + 1 # cumul 6eme question
            #alert(f"cumul q6: {points_q6}")
            points_q7 = points_q7 + dico_ferm["7"][1] + 1 # cumul 7eme question
            #alert(f"cumul q7: {points_q7}")
            points_q8 = points_q8 + dico_ferm["8"][1] + 1 # cumul 8eme question
            #alert(f"cumul q8: {points_q8}")
            points_q9 = points_q9 + dico_ferm["9"][1] + 1 # cumul 9eme question
            #alert(f"cumul q9: {points_q9}")
            points_q10 = points_q10 + dico_ferm["10"][1] + 1 # cumul 10eme question
            #alert(f"cumul q10: {points_q10}")
            
        # fin de boucle questions fermées, calcul des pourcentages
        pourcent_q1 = str(round((points_q1 / max_points_ferm) * 100,2))
        pourcent_q2 = str(round((points_q2 / max_points_ferm) * 100,2))
        pourcent_q3 = str(round((points_q3 / max_points_ferm) * 100,2))
        pourcent_q4 = str(round((points_q4 / max_points_ferm) * 100,2))
        pourcent_q5 = str(round((points_q5 / max_points_ferm) * 100,2))
        pourcent_q6 = str(round((points_q6 / max_points_ferm) * 100,2))
        pourcent_q7 = str(round((points_q7 / max_points_ferm) * 100,2))
        pourcent_q8 = str(round((points_q8 / max_points_ferm) * 100,2))
        pourcent_q9 = str(round((points_q9 / max_points_ferm) * 100,2))
        pourcent_q10 = str(round((points_q10 / max_points_ferm) * 100,2))
        # Détermination des couleurs d'affichage en fonction du pourcent
        self.couleurs(1,pourcent_q1)
        
        # affichage des formes fermées  en fonction de leur nb
        if nb_questions_ferm > 0:  # Check du nb de questions fermées à afficher et affectation des questions
            self.column_panel_1.visible = True
            self.label_1.text = dico_q_ferm["1"][0] + ": " + pourcent_q1 + " %"  # Je prends le 1er elmt de la liste (la question), le 2eme: si question 'obligatoire / facultative'
        if nb_questions_ferm > 1:
            self.column_panel_2.visible = True
            self.label_2.text = dico_q_ferm["2"][0] + ": " + pourcent_q2 + " %" 
        if nb_questions_ferm > 2:
            self.column_panel_3.visible = True
            self.label_3.text = dico_q_ferm["3"][0] + ": " + pourcent_q3 + " %" 
        if nb_questions_ferm > 3:
            self.column_panel_4.visible = True
            self.label_4.text = dico_q_ferm["4"][0] + ": " + pourcent_q4 + " %" 
        if nb_questions_ferm > 4:
            self.column_panel_5.visible = True
            self.label_5.text = dico_q_ferm["5"][0] + ": " + pourcent_q5 + " %" 
        if nb_questions_ferm > 5:
            self.column_panel_6.visible = True
            self.label_6.text = dico_q_ferm["6"][0] + ": " + pourcent_q6 + " %" 
        if nb_questions_ferm > 6:
            self.column_panel_7.visible = True
            self.label_7.text = dico_q_ferm["7"][0] + ": " + pourcent_q7 + " %" 
        if nb_questions_ferm > 7:
            self.column_panel_8.visible = True
            self.label_8.text = dico_q_ferm["8"][0] + ": " + pourcent_q8 + " %" 
        if nb_questions_ferm > 8:
            self.column_panel_9.visible = True
            self.label_9.text = dico_q_ferm["9"][0] + ": " + pourcent_q9 + " %" 
        if nb_questions_ferm > 9:
            self.column_panel_10.visible = True
            self.label_10.text = dico_q_ferm["10"][0] + ": " + pourcent_q10 + " %" 

        # affichage des formes ouvertes en fonction de leur nb
        dico_q_ouv = stage_row["com_ouv"]  # check du nb de questions ouvertes à afficher et affectation des questions
        global nb_questions_ouvertes  # nb questions ouvertes
        nb_questions_ouvertes = int(dico_q_ouv["NBQ"])
        if nb_questions_ouvertes > 0:
            self.column_panel_a1.visible = True
            self.label_a1.text = dico_q_ouv["1"][0]
            
        if nb_questions_ouvertes > 1:
            self.column_panel_a2.visible = True
            self.label_a2.text = dico_q_ouv["2"][0]
            
        if nb_questions_ouvertes > 2:
            self.column_panel_a3.visible = True
            self.label_a3.text = dico_q_ouv["3"][0]
            
        if nb_questions_ouvertes > 3:
            self.column_panel_a4.visible = True
            self.label_a4.text = dico_q_ouv["4"][0]
            
        if nb_questions_ouvertes > 4:
            self.column_panel_a5.visible = True
            self.label_a5.text = dico_q_ouv["5"][0]
            
        if nb_questions_ouvertes > 5:
            self.column_panel_a6.visible = True
            self.label_a6.text = dico_q_ouv["6"][0]
            
        if nb_questions_ouvertes > 6:
            self.column_panel_a7.visible = True
            self.label_a7.text = dico_q_ouv["7"][0]
            
        if nb_questions_ouvertes > 7:
            self.column_panel_a8.visible = True
            self.label_a8.text = dico_q_ouv["8"][0]
            
        if nb_questions_ouvertes > 8:
            self.column_panel_a9.visible = True
            self.label_a9.text = dico_q_ouv["9"][0]
            
        if nb_questions_ouvertes > 9:
            self.column_panel_a10.visible = True
            self.label_a10.text = dico_q_ouv["10"][0]
            
    def couleurs(self, num_question, pourcent,  **event_args):    
        if pourcent<=16: 
        nom_couleur = "theme:Error"
        if num_question == 1:
            self.label_1.background = nom_couleur
        if num_question == 2:
            self.label_2.background = nom_couleur
        if num_question == 3:
            self.label_3.background = nom_couleur
        if num_question == 4:
            self.label_4.background = nom_couleur
        if num_question == 5:
            self.label_5.background = nom_couleur
        if num_question == 6:
            self.label_6.background = nom_couleur
        if num_question == 7:
            self.label_7.background = nom_couleur
        if num_question == 8:
            self.label_8.background = nom_couleur
        if num_question == 9:
            self.label_9.background = nom_couleur
        if num_question == 10:
            self.label_10.background = nom_couleur
        return 
    