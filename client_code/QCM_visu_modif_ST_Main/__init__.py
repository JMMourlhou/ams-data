from ._anvil_designer import QCM_visu_modif_ST_MainTemplate
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..QCM_visu_modif import QCM_visu_modif
import random             # pour rechercher les qcm BNSSA randomly avec random.randrange(début, fin)
global liste
liste = []




class QCM_visu_modif_ST_Main(QCM_visu_modif_ST_MainTemplate):
    def __init__(self, qcm_descro_nb=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.qcm_row = None
        # acquisition du user
        user=anvil.users.get_user()        
        if user:
            self.admin = user['role']
            if self.admin[0:1]=="S":         # si pas stagiaire
               self.label_3.text = "Q.C.M"
        
        #initialisation du drop down des qcm créés et barêmes
        self.drop_down_qcm_row.items = [(r['destination'], r) for r in app_tables.qcm_description.search(
                                                                                                         visible=True
                                                                                                         )]
        
        if qcm_descro_nb != None:      #réinitialisation de la forme après une création ou modif
            self.qcm_nb = qcm_descro_nb # je sauve le row du qcm sur lesquel je suis en train de travailler
            # j'affiche le drop down du qcm
            self.drop_down_qcm_row.selected_value = qcm_descro_nb
            # j'envoie en drop_down_qcm_row_change
            self.drop_down_qcm_row_change()
    
    def drop_down_qcm_row_change(self, **event_args):
        """This method is called when an item is selected"""
        qcm_row = self.drop_down_qcm_row.selected_value
        self.qcm_row = qcm_row
        # Pour les lignes QCM déjà crée du qcm choisi
        global liste
        if qcm_row["qcm_nb"] != 10:
            liste = list(app_tables.qcm.search(qcm_nb=qcm_row))
        else:
            liste = list(self.liste_qcm_bnssa_blanc())
        nb_questions = len(liste)
        self.label_2.text = nb_questions + 1   # Num ligne à partir du nb lignes déjà créées

        # acquisition du user et modif de son temp (nb de questions de son qcm)
        user=anvil.users.get_user()
        r = anvil.server.call("temp_user_qcm", user, nb_questions)
        if r == False:
            alert("user non MAJ")
            return
        # affiche le titre
        if self.admin[0:1]=="S":         # si stagiaire
               self.label_3.text = "Q.C.M " + qcm_row["destination"]
        # affiches les lignes du qcm
        self.affiche_lignes_qcm(liste)
    
    def affiche_lignes_qcm(self, l=[]):
        global liste
        self.column_panel_content.clear()
        self.column_panel_content.add_component(QCM_visu_modif(liste), full_width_row=True)

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def button_annuler2_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)
 

    def liste_qcm_bnssa_blanc(self, **event_args):
        global liste
        liste=[]
        # 10 questions pour partie 1 qcm BNSSA (nb4)
        liste1 = self.liste_qcm_partie_x(4, 10)   # (num qcm, nb de questions à prendre randomly)
        for i in range(len(liste1)):
            liste.append(liste1[i])
        liste2 = self.liste_qcm_partie_x(5, 10)
        for i in range(len(liste2)):
            liste.append(liste2[i])
        liste3 = self.liste_qcm_partie_x(6, 10)
        for i in range(len(liste3)):
            liste.append(liste3[i])
        liste4 = self.liste_qcm_partie_x(7, 8)
        for i in range(len(liste4)):
            liste.append(liste4[i])
        liste5 = self.liste_qcm_partie_x(8, 8)
        for i in range(len(liste5)):
            liste.append(liste5[i])
        liste6 = self.liste_qcm_partie_x(9, 5)
        for i in range(len(liste6)):
            liste.append(liste6[i])
        #if user:
        #    result = anvil.server.call("qcm_blanc", liste)     # sauvegarde liste ds user
        return liste

    def liste_qcm_partie_x(self, qcm_nb, nb_max, **event_args):
        liste = []
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ qcm nb: ", qcm_nb)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ nb max: ", nb_max)
        # 10 questions à extraire randomly 
        #extraction du nb de questions du BNSSA partie 1
        qcm_row = app_tables.qcm_description.get(qcm_nb=qcm_nb)
        if qcm_row:
            liste_entierre = app_tables.qcm.search(qcm_nb=qcm_row )
            nb_total_questions = len(liste_entierre)
            print(f"nb question ds qcm_nb {qcm_nb}: {nb_total_questions}" )
        else:
            print("pb accès table qcm n° 4 (BNSSA partie 1)")
            return
        dict = {}
        while len(dict) < nb_max:
            num_question =   random.randrange(1, nb_total_questions+1)  
            question_row = app_tables.qcm.get(qcm_nb=qcm_row,
                                             num=num_question
                                             )
            clef = num_question           # clé du dict de questions     Comme il ne peut y avoir 2 même clé, si random prend 2 fois la même question, elle écrase l'autre
            valeur = question_row
            print("clef: ",clef)
            dict[clef] = valeur   # je mets à jour la liste dictionaire des questions
        
        for cle, valeur in dict.items():
            liste.append(valeur)
        
        return liste



            
        
        






