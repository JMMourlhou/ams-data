from ._anvil_designer import ItemTemplate4Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

global question  # sauvegarde de la question
question = ""
global bareme 
bareme = 1      # bareme est numeric
global reponse
reponse = True   # reponse est booléen

class ItemTemplate4(ItemTemplate4Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        
        self.text_box_num.text = self.item['num']
        self.text_box_num.tag.numero = self.item['num']
        self.text_box_num.tag.nom = "num"
        
        self.text_box_question.text = self.item['question']
        self.text_box_question.tag.nom = "question"
        self.text_box_question.tag.numero = self.item['num']
        
        self.check_box_reponse.checked = self.item['reponse']
        self.check_box_reponse.tag.nom = "reponse"
        self.check_box_reponse.tag.numero = self.item['num']

        self.drop_down_bareme.items=["1","2","3","4","5"]
        self.drop_down_bareme.selected_value = self.item['bareme']                 
        self.drop_down_bareme.tag.nom = "bareme"
        self.drop_down_bareme.tag.numero = self.item['num']
        
        self.button_modif.tag.numero = self.item['num']          #Je sauve le NUMERO de question ds le tag      
        self.button_modif.tag.nom = "button"
        
    def text_box_question_change(self, **event_args):   # Question a changé
        """This method is called when the text in this text box is edited"""
        # je récupère le contenu du cpnt
        global question
        question = self.lecture_cpnt(event_args).capitalize()
    
    def drop_down_bareme_change(self, **event_args):     # Bareme a changé
        """This method is called when this checkbox is checked or unchecked"""
        global bareme
        bareme = self.lecture_cpnt(event_args)
        
    
    def check_box_reponse_change(self, **event_args):   # Reponse a changé: 
        """This method is called when this checkbox is checked or unchecked"""
        global reponse
        reponse = self.lecture_cpnt(event_args)


    def lecture_cpnt(self, event_args):
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
        
        cpnt=event_args['sender'] #quel component a été changé
        # je récupère le contenu du cpnt en fonction du tag.nom et type du component
        if  type(cpnt) is TextBox or type(cpnt) is TextArea:
            return cpnt.text
        if type(cpnt) is CheckBox:
            return cpnt.checked
        if type(cpnt) is DropDown:
            return cpnt.selected_value

    
    def button_modif_click(self, **event_args):   #ce n'est que l'orsque le user a clicker sur modif que je prend le contenu
        """This method is called when the button is clicked"""
        
        #je connais le num de question à changer
        num = int(self.button_modif.tag.numero)
        #from ... import test_qcm_modif
        #result=test_qcm_modif.test_deux_lignes_qcm()
        #alert(result)            

        # je récupère mes variables globales  question, reponse, bareme
        global question
        global reponse
        global bareme
        result = anvil.server.call('modif_qcm', num, question, reponse, bareme)
        if not result:
            alert("erreur de création d'une question QCM")
            return
        
        from anvil import open_form       # j'initialise la forme principale
        open_form("QCM_visu_modif_Main") 

   
        


    

        

    

        




 


        
        