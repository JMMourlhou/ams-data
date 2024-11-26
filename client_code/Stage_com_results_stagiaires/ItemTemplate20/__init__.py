from ._anvil_designer import ItemTemplate20Template
from anvil import *
import anvil.server

import anvil.users
import anvil.tables as tables

from anvil.tables import app_tables


class ItemTemplate20(ItemTemplate20Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.label_nom.text = self.item['nom']
        longueur_voulue = 100
        
        self.label_1.text = self.display(self.item['pourcent_1'])   # fonction displaypour arrondir le % à l'entier
        self.label_1.background = self.bg_couleur(self.item['pourcent_1'])
        q1 = self.item['q1']
        q1 = q1.ljust(longueur_voulue)+"/"
        self.label_11.text = q1
        print("q1",len(q1))
        #self.spacer_1.height = self.space_height(q1)   # fonction space_height pour aligner l'outline card grace au spacer 
                
        
        self.label_2.text = self.display(self.item['pourcent_2'])
        self.label_2.background = self.bg_couleur(self.item['pourcent_2'])
        q2 = self.item['q2']
        q2 = q2.ljust(longueur_voulue)+"."
        self.label_12.text = q2
        print("q2",len(q2))
        
        #self.spacer_2.height = self.space_height(self.item['q2'])
        
        self.label_3.text = self.display(self.item['pourcent_3'])
        self.label_3.background = self.bg_couleur(self.item['pourcent_3'])
        q3 = self.item['q3']
        q3 = q3.ljust(longueur_voulue)+"."
        self.label_13.text = q3
        print("q3",len(q3))
        
        self.label_4.text = self.display(self.item['pourcent_4'])
        self.label_4.background = self.bg_couleur(self.item['pourcent_4'])
        q4 = self.item['q4']
        q4 = q4.ljust(longueur_voulue)+"."
        self.label_14.text = q4
        print("q4",len(q4))
        
        self.label_5.text = self.display(self.item['pourcent_5'])
        self.label_5.background = self.bg_couleur(self.item['pourcent_5'])
        q5 = self.item['q5']
        q5 = q5.ljust(longueur_voulue)+"."
        self.label_15.text = q5
        print("q5",len(q5))
        
        self.label_6.text = self.display(self.item['pourcent_6'])
        self.label_6.background = self.bg_couleur(self.item['pourcent_6'])
        q6 = self.item['q6']
        q6 = q6.ljust(longueur_voulue)+"."
        self.label_16.text = q6
        
        self.label_7.text = self.display(self.item['pourcent_7'])
        self.label_7.background = self.bg_couleur(self.item['pourcent_7'])
        q7 = self.item['q7']
        q7 = q7.ljust(longueur_voulue)+"."
        self.label_17.text = q7
        
        self.label_8.text = self.display(self.item['pourcent_8'])
        self.label_8.background = self.bg_couleur(self.item['pourcent_8'])
        q8 = self.item['q8']
        q8 = q8.ljust(longueur_voulue)+"."
        self.label_18.text = q8
        
        self.label_9.text = self.display(self.item['pourcent_9'])
        self.label_9.background = self.bg_couleur(self.item['pourcent_9'])
        q9 = self.item['q9']
        q9 = q9.ljust(longueur_voulue)+"."
        self.label_19.text = q9
        
        self.label_10.text = self.display(self.item['pourcent_10'])
        self.label_10.background = self.bg_couleur(self.item['pourcent_10'])
        q10 = self.item['q10']
        q10 = q10.ljust(longueur_voulue)+"."
        self.label_20.text = q10
        
    def display(self, nb, **properties):
        nb1=round(nb)
        print(nb1)
        text = str(nb1)+" %"
        print(text)
        return text
        
    def bg_couleur(self, nb):
        if nb < 10 == 0:
            bg_couleur = "theme:Error"
        elif nb < 30:
            bg_couleur = "theme:Orange"    
        elif nb < 60:
            bg_couleur = "theme:Jaune Orange"
        elif nb < 80:
            bg_couleur = "theme:Vert Tres Clair"
        elif nb < 90:
            bg_couleur = "theme:Vert Clair"    
        else:
            bg_couleur = "theme:Vert Foncé"
        return bg_couleur
        

    def space_height(self, question):
        # 1 ligne de texte = 14 caract ds l'outline card
        # 4 lignes = 4*16 = 64
        lg = len(question)
        nb_lignes = int(lg / 19)
        reste = lg % 19
        if reste > 0:
            nb_lignes += 1
        
        if nb_lignes == 1 or nb_lignes == 0:
            space = 32
            print(f"nb de lignes: {nb_lignes} / question: {question} ")
            print(f"space height: {space}")
        elif nb_lignes == 2:
            space = 10
            print(f"nb de lignes: {nb_lignes} / question: {question} ")
            print(f"space height: {space}")
        elif nb_lignes == 3:
            space = 8
            print(f"nb de lignes: {nb_lignes} / question: {question} ")
            print(f"space height: {space}")
        else :
            space = 0
            print(f"nb de lignes: {nb_lignes} / question: {question} ")
            print(f"space height: {space}")
        return space

        
