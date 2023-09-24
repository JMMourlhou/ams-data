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
        
        self.text_box_3.text = self.item['num']
        self.text_box_2.text = self.item['question']
        self.text_box_2.tag = self.item['num']          #Je sauve le num de question ds le tag
        self.check_box_1.checked = self.item['reponse']
        self.check_box_1.tag = self.item['num']  
        self.text_box_1.text = self.item['bareme']                 
        self.text_box_1.tag = self.item['num']
        self.button_modif.tag = self.item['num']
        
    
    def text_box_2_change(self, **event_args):   # Question a changé
        """This method is called when the text in this text box is edited"""
        self.button_modif.enabled = True
        t_box2_changed = event_args['sender']
        # je récupère le contenu de la question
        global question
        question = t_box2_changed.text
        print(question)

    def text_box_1_change(self, **event_args):     # Bareme a changé
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.enabled = True
        t_box1_changed = event_args['sender']
        # je récupère le contenu de la question
        global bareme
        bareme = t_box1_changed.text
        print(bareme)

    
    def check_box_1_change(self, **event_args):   # Reponse a changé: 
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.enabled = True
        c_box_changed = event_args['sender']
        global reponse
        reponse = c_box_changed.checked
        print(reponse)
    
    def button_modif_click(self, **event_args):
        """This method is called when the button is clicked"""
        print(self.button_modif.tag)
        
        #je connais le num de question à changer
        num = int(self.button_modif.tag)

        # je récupère mes variables globales  question, reponse, bareme
        global question
        global reponse
        global bareme
        result = anvil.server.call('modif_qcm', num, question, reponse, bareme)
        if result:
            alert("ok")

   
        


    

        

    

        




 


        
        