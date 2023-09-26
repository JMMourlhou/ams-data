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
global dernier_num
dernier_num = 0

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
        global dernier_num
        global question
        question, dernier_num = self.lecture_cpnt(event_args)
        question = question.capitalize()
        
    def drop_down_bareme_change(self, **event_args):     # Bareme a changé
        """This method is called when this checkbox is checked or unchecked"""
        global dernier_num
        global bareme
        bareme, dernier_num = self.lecture_cpnt(event_args)
        
    
    def check_box_reponse_change(self, **event_args):   # Reponse a changé: 
        """This method is called when this checkbox is checked or unchecked"""
        global dernier_num
        global reponse
        reponse, dernier_num = self.lecture_cpnt(event_args)


    def lecture_cpnt(self, event_args):
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
        
        cpnt=event_args['sender'] #quel component a été changé
        # je récupère le contenu du cpnt en fonction du tag.nom et type du component ET le num de question correspondant
        if  type(cpnt) is TextBox or type(cpnt) is TextArea:
            return cpnt.text, cpnt.tag.numero 
        if type(cpnt) is CheckBox:
            return cpnt.checked, cpnt.tag.numero
        if type(cpnt) is DropDown:
            return cpnt.selected_value, cpnt.tag.numero

    
    def button_modif_click(self, **event_args):   #ce n'est que l'orsque le user a clicker sur modif que je prend le contenu
        """This method is called when the button is clicked"""
        
        #num de question du bouton 
        num = int(self.button_modif.tag.numero)
        print("Ligne question du bouton: ", num)
        global dernier_num
        if num == dernier_num :
            # je récupère mes variables globales  question, reponse, bareme
            global question
            global reponse
            global bareme
            result = anvil.server.call('modif_qcm', num, question, reponse, bareme)
            if not result:
                alert("erreur de création d'une question QCM")
                return
        else:
            alert("Ne modifier qu'1 ligne à la fois")
            
        # j'initialise la forme principale
        dernier_num = 0
        from anvil import open_form       
        open_form("QCM_visu_modif_Main")
        

   
        


    

        

    

        




 


        
        