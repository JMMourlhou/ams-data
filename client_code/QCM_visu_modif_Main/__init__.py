from ._anvil_designer import QCM_visu_modif_MainTemplate
from anvil import *
import anvil.server
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
        self.column_panel_question.visible = False
        #initialisation des drop down des qcm créés et barêmes
        self.image_1.source = None
        self.drop_down_qcm_row.items = [(r['destination'], r) for r in app_tables.qcm_description.search(tables.order_by("destination", ascending=True))]
        self.drop_down_bareme.items=["1","2","3","4","5","10"]
        self.drop_down_bareme.selected_value = "1"
        self.drop_down_nb_options.items=([("Vrai/Faux", 1), ("2 options", 2), ("3 options", 3), ("4 options", 4), ("5 options", 5)])
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  Ré-affichage ?   +++++++++++++++++++++++++++++
        if qcm_descro_nb is not None:      #réinitialisation de la forme après une création ou modif
            self.qcm_nb = qcm_descro_nb # je sauve le row du qcm sur lesquel je suis en train de travailler
            # j'affiche le drop down du qcm
            self.drop_down_qcm_row.selected_value = qcm_descro_nb
            # j'envoie en drop_down_qcm_row_change
            self.drop_down_qcm_row_change()

    def drop_down_qcm_row_change(self, **event_args):
        """This method is called when an item is selected"""
        qcm_row = self.drop_down_qcm_row.selected_value
        user=anvil.users.get_user()

        # test si il est le propriétaire
        if qcm_row["qcm_owner"]["email"] != user["email"]:
            alert("Vous n'êtes pas le propriétaire de ce QCM, \nVous ne pouvez pas le modifier !")
            return
        
        # Pour les lignes QCM déjà crée du qcm choisi
        global liste
        liste = list(app_tables.qcm.search(qcm_nb=qcm_row))
        nb_questions = len(liste)
        print("nb questions: ", nb_questions)
        #num_question = str(nb_questions + 1)
        self.label_2.text = nb_questions + 1  # Num ligne à partir du nb lignes déjà créées

        # modif du user's temp (nb de questions de son qcm)
        
        r = anvil.server.call("temp_user_qcm", user, nb_questions,qcm_row["qcm_nb"])
        if r is False:
            alert("user non MAJ")
            return
            
        # Affiche button Test si au moins 1 question existe déjà
        if nb_questions > 1:
            self.button_test.visible = True
            
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
        self.column_panel_img.visible = True
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

        self.column_panel_img.visible = True
        self.text_box_correction.visible = True    
        self.text_box_question.visible = True    
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
        if self.drop_down_bareme.selected_value == None:
            alert("Choisissez un barême !")
            return
        qst = self.text_box_question.text
        qst = qst.strip()
        question = qst

        cor = self.text_box_correction.text
        cor = cor.strip()
        correction = cor
        bareme = int(self.drop_down_bareme.selected_value)
        qcm_nb = self.drop_down_qcm_row.selected_value

        if self.image_1.source != "":
            image = self.image_1.source
        else:
            image = None
        # creation de la réponse multi en fonction du nb d'options choisies +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        reponse = ""
        if self.rep1.checked is True:
            r1 = "1"
        else: 
            r1 = "0"
        if self.rep2.checked is True:
            r2 = "1"
        else: 
            r2 = "0"
        if self.rep3.checked is True:
            r3 = "1"
        else: 
            r3 = "0"
        if self.rep4.checked is True:
            r4 = "1"
        else: 
            r4 = "0"
        if self.rep5.checked is True:
            r5 = "1"
        else: 
            r5 = "0"
        if self.drop_down_nb_options.selected_value == 1 or self.drop_down_nb_options.selected_value == 2:    
            reponse = r1 + r2
        if self.drop_down_nb_options.selected_value == 3:
            reponse = r1 + r2 + r3
        if self.drop_down_nb_options.selected_value == 4:
            reponse = r1 + r2 + r3 + r4
        if self.drop_down_nb_options.selected_value == 5:
            reponse = r1 + r2 + r3 + r4 + r5
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  NUM question   +++++++++++++++++++++++++++++
        num = int(self.label_2.text) #je connais le num de question à changer
        # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++  type de question   +++++++++++++++++++++++++++++
        if self.drop_down_nb_options.selected_value == 1:    # type V/F
            type = "V/F"       # rep1 ou rep2 peuvent être vrai
        else:
            type = "Multi"     # rep1 et rep2 peuvent être vrai 
        # param
        param = self.drop_down_qcm_row.selected_value["destination"]
        # je récupère mes variables globales  question, reponse, bareme
        result = anvil.server.call("add_ligne_qcm", num, question, correction, reponse, bareme, image, qcm_nb, type, param)         #num du stage  de la ligne
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
            if self.rep1.checked is True:   
                self.rep2.checked = False
            else:
                self.rep2.checked = True

    def rep2_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        if self.drop_down_nb_options.selected_value == 1:    # option vrai/faux
            if self.rep2.checked is True:   
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

    def button_test_click(self, **event_args):
        """This method is called when the button is clicked"""

        # Concepteur du qcm demande un test du qcm qu'il met à jour
        # écriture ds table user, colonne 'temp2' : "test" 
        user=anvil.users.get_user()
        if user:
            result = anvil.server.call("modify_users_temp2", user, "test")
            self.affiche_lignes_qcm()
            result = anvil.server.call("modify_users_temp2", user, None)   # je remets temp2 à vide

    def button_creation_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.column_panel_question.visible = False
        self.column_panel_content.visible = False
        # initialisation du num en lisant tous les QCM dispo et en ajoutant 1
        nb_qcm = app_tables.qcm_description.search()
        self.text_box_num_qcm.text=len(nb_qcm)+1
        #initialisation des propriétaires potentiels, bureaux/formateurs
        liste = app_tables.users.search(
                                            q.fetch_only("nom","prenom","email","role"),
                                            tables.order_by("prenom", ascending=True),
                                            q.not_ (role = "S") or (role = "T")
                                                     
                                        )
            
        liste2 = []
        for qcm_owner in liste:
            liste2.append((qcm_owner["prenom"]+" "+qcm_owner["nom"],qcm_owner["email"]))
        self.drop_down_owner.items=liste2
    
