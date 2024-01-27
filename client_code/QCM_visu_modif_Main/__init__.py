from ._anvil_designer import QCM_visu_modif_MainTemplate
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
# ==========================================================================   Ellaboration d'un QCM par un formateur ou admin
class QCM_visu_modif_Main(QCM_visu_modif_MainTemplate):
    def __init__(self, qcm_descro_nb=None, **properties):      #qcm_descro_nb n'est pas None si je suis en réaffichage après création ou maj d'1 question du qcm 
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.column_panel_1.visible = False
        #initialisation du drop down des qcm créés et barêmes
        self.drop_down_qcm_row.items = [(r['destination'], r) for r in app_tables.qcm_description.search()]
        self.drop_down_bareme.items=["1","2","3","4","5","10"]
        self.drop_down_nb_options.items=([("Vrai/Faux", 1), ("2 options", 2), ("3 options", 3), ("4 options", 4), ("5 options", 5)])
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
        print("nb questions: ", nb_questions)
        #num_question = str(nb_questions + 1)
        self.label_2.text = nb_questions + 1  # Num ligne à partir du nb lignes déjà créées

        # acquisition du user et modif de son temp (nb de questions de son qcm)
        user=anvil.users.get_user()
        r = anvil.server.call("temp_user_qcm", user, nb_questions)
        if r == False:
            alert("user non MAJ")
            return

         # affiches les lignes du qcm
        self.label_3.text = "Mise à jour du Q.C.M " + qcm_row["destination"]
        self.column_panel_1.visible = True
        self.affiche_lignes_qcm(liste)


    def affiche_lignes_qcm(self, l=[]):
        global liste
        self.column_panel_content.clear()
        self.column_panel_content.add_component(QCM_visu_modif(liste), full_width_row=True)

    def file_loader_photo_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        thumb_pic = anvil.image.generate_thumbnail(file, 640)
        self.image_1.source = thumb_pic
        self.button_creer.visible = True

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def drop_down_nb_options_change(self, **event_args):
        """This method is called when an item is selected"""
        self.rep1.checked = False
        self.rep2.checked = False
        self.rep3.checked = False
        self.rep4.checked = False
        self.rep5.checked = False
        choix = self.drop_down_nb_options.selected_value
        print(choix, type(choix))
        if choix == 1:   # Vrai/ Faux    l'1 ou l'autre, rep1 et rep2 ne peuvent pas  être identiques
            self.rep3.visible = False
            self.rep4.visible = False
            self.rep5.visible = False
            self.rep1.text = "Vrai"
            self.rep2.text = "Faux"
        if choix > 1:     # 2 options possibles, rep1 et rep2 peuvent être identiques  ex 11 
            self.rep1.text = "A"
            self.rep2.text = "B"
            self.rep3.visible = False
            self.rep4.visible = False
            self.rep5.visible = False
            self.text_box_question.text = "titre\n\nA  .\n\nB  ."
        if choix > 2:     # au moins 3 options possibles, rep1 à rep3 peuvent être identiques  ex 111
            self.rep3.visible = True
            self.rep4.visible = False
            self.rep5.visible = False
            self.text_box_question.text = "titre\n\nA  .\nB  .\nC  ."
        if choix > 3:     # au moins 4 options possibles, rep1 et rep4 peuvent être identiques  ex  1111
            self.rep4.visible = True
            self.rep5.visible = False
            self.text_box_question.text = "titre\n\nA  .\nB  .\nC  .\nD  ."
        if choix > 4:     # 5 options possibles, rep1 à rep2 peuvent être identiques
            self.rep5.visible = True
            self.text_box_question.text = "titre\n\nA  .\nB  .\nC  .\nD  .\nE  ."
            
        self.column_panel_options.visible = True
        self.button_creer_couleurs()

    def text_box_question_change(self, **event_args):   # Question a changé
        """This method is called when the text in this text box is edited"""
        self.button_creer_couleurs()

    def text_box_correction_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.button_creer_couleurs()

    def drop_down_bareme_change(self, **event_args):     # Bareme a changé
        """This method is called when this checkbox is checked or unchecked"""
        self.button_creer_couleurs()

    def check_box_reponse_change(self, **event_args):   # Reponse a changé:
        """This method is called when this checkbox is checked or unchecked"""
        self.button_creer_couleurs()

    def button_creer_couleurs(self): # qd changement
        self.button_creer.enabled = True
        self.button_creer.background = "red"
        self.button_creer.foregroundground = "yellow"

    def button_creer_click(self, **event_args):   #ce n'est que l'orsque le user a clicker sur modif que je prend le contenu
        """This method is called when the button is clicked"""
        if self.text_box_question.text == "":
            alert("La question est vide !")
            return
        qst = self.text_box_question.text
        qst = qst.strip()
        question = qst

        cor = self.text_box_correction.text
        cor = cor.strip()
        correction = cor
        bareme = int(self.drop_down_bareme.selected_value)
        qcm_nb = self.drop_down_qcm_row.selected_value
        image = self.image_1.source
        # creation de la réponse multi en fonction du nb d'options choisies +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        reponse = ""
        if self.rep1.checked == True:
            r1 = 1
        else: 
            r1 = 0
        if self.rep2.checked == True:
            r2 = 1
        else: 
            r2 = 0
        if self.rep3.checked == True:
            r3 = 1
        else: 
            r3 = 0
        if self.rep4.checked == True:
            r4 = 1
        else: 
            r4 = 0
        if self.rep5.checked == True:
            r5 = 1
        else: 
            r5 = 0
        if self.drop_down_nb_options.selected_value == 1 or self.drop_down_nb_options.selected_value == 2:    
            reponse = r1 + r2
        if self.drop_down_nb_options.selected_value == 3:
            reponse = r1 + r2 + r3
        if self.drop_down_nb_options.selected_value == 4:
            reponse = r1 + r2 + r3 + r4
        if self.drop_down_nb_options.selected_value == 5:
            reponse = r1 + r2 + r3 + r4 + r5
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        num = int(self.label_2.text) #je connais le num de question à changer

        # je récupère mes variables globales  question, reponse, bareme
        result = anvil.server.call("add_ligne_qcm", num, question, correction, reponse, bareme, image, qcm_nb)         #num du stage  de la ligne
        if result:
            n = Notification("Création de la question !",
                 timeout=1)   # par défaut 2 secondes
            n.show()
            # raffraichit les lignes qcm en récupérant le choix du qcm ds la dropdown
            from anvil import open_form       # j'initialise la forme principale avec le choix du qcm ds la dropdown
            open_form("QCM_visu_modif_Main", qcm_nb)

        else:
            alert("erreur de création d'une question QCM")

    def rep1_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.drop_down_nb_options.selected_value == 1:    # option vrai/faux
            if self.rep1.checked == True:   
                self.rep2.checked = False
            else:
                self.rep2.checked = True

    def rep2_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.drop_down_nb_options.selected_value == 1:    # option vrai/faux
            if self.rep2.checked == True:   
                self.rep1.checked = False
            else:
                self.rep1.checked = True

    def rep3_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.button_creer_couleurs()

    def rep4_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.button_creer_couleurs()

    def rep5_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.button_creer_couleurs()