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
global liste
liste = []

class QCM_visu_modif_ST_Main(QCM_visu_modif_ST_MainTemplate):
    def __init__(self, qcm_descro_nb=None, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        # acquisition du user
        user=anvil.users.get_user()        
        if user:
            self.admin = user['role']
            if self.admin[0:1]=="S":         # si pas stagiaire
               self.label_3.text = "Q.C.M"
        
        #initialisation du drop down des qcm créés et barêmes
        self.drop_down_qcm_row.items = [(r['destination'], r) for r in app_tables.qcm_description.search()]
        
        if qcm_descro_nb != None:      #réinitialisation de la forme après une création ou modif
            self.qcm_nb = qcm_descro_nb # je sauve le row du qcm sur lesquel je suis en train de travailler
            # j'affiche le drop down du qcm
            self.drop_down_qcm_row.selected_value = qcm_descro_nb
            # j'envoie en drop_down_qcm_row_change
            self.drop_down_qcm_row_change()
    
    def drop_down_qcm_row_change(self, **event_args):
        """This method is called when an item is selected"""
        qcm_row = self.drop_down_qcm_row.selected_value

        # Pour les lignes QCM déjà crée du qcm choisi
        global liste
        liste = list(app_tables.qcm.search(qcm_nb=qcm_row))
        nb_questions = len(liste)
        self.label_2.text = nb_questions + 1   # Num ligne à partir du nb lignes déjà créées

        # acquisition du user et modif de son temp (nb de questions de son qcm)
        user=anvil.users.get_user()
        r = anvil.server.call("temp_user_qcm", user, nb_questions)
        if r == False:
            alert("user non MAJ")
            return
        # affiche le titre
        if self.admin[0:1]=="S":         # si pas stagiaire
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

    def button_aff_result1_click(self, **event_args):
        """This method is called when the button is clicked"""
        # affichage des résultats
        #nb_bonnes_rep = 0   
        self.column_panel_2.visible = True

    def button_aff_result2_click(self, **event_args):
        """This method is called when the button is clicked"""
        # affichage des résultats
        self.button_aff_result1_click()    






