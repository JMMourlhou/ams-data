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


class QCM_visu_modif_Main(QCM_visu_modif_MainTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

        # Pour les lignes QCM déjà crée du repeating panel
        liste = list(app_tables.qcm.search())
        nb_questions = len(liste)
        self.text_box_num.text = nb_questions + 1   # Num ligne à partir du nb lignes déjà créées 
        
        self.drop_down_bareme.items=["1","2","3","4","5"]
        #self.drop_down_bareme.selected_value = 0              # Barême = 1 par défaut 
        
        # Drop down codes stages
        self.drop_down_code_stage.items = [(r['code'], r) for r in app_tables.codes_stages.search()]
      
        # affiches les lignes du qcm
        self.affiche_lignes_qcm()

    def affiche_lignes_qcm(self):
        self.column_panel_content.clear()
        self.column_panel_content.add_component(QCM_visu_modif(), full_width_row=True)

    def file_loader_photo_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        #self.image_photo.source = file
        thumb_pic = anvil.image.generate_thumbnail(file, 320)
        self.image_photo.source = thumb_pic
        self.button_creer.visible = True

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def text_box_question_change(self, **event_args):   # Question a changé
        """This method is called when the text in this text box is edited"""
        self.button_creer_couleurs()
    
    def text_box_bareme_change(self, **event_args):     # Bareme a changé
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
        question = self.text_box_question.text
        bareme = int(self.drop_down_bareme.selected_value)
        reponse = self.check_box_reponse.checked
        

        #je connais le num de question à changer
        num = int(self.text_box_num.text)
        if self.image_photo.source == None:
            image = None
        else:
            image = self.image_photo.source
        
        # je récupère mes variables globales  question, reponse, bareme
        result = anvil.server.call("add_ligne_qcm", num, question, reponse, bareme, image, code_stage="PSE1")         #num du stage  de la ligne
        if result:
            alert("ok")
            # raffraichit les lignes qcm
            self.affiche_lignes_qcm()
            from anvil import open_form       # j'initialise la forme principale
            open_form("QCM_visu_modif_Main") 
            
        else:
            alert("erreur de création d'une question QCM")
            
        
        

