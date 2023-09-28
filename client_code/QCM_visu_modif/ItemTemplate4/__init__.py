from ._anvil_designer import ItemTemplate4Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global ancien_num_ligne    # pour pouvoir rendre un bt inactif si perte de focus  
ancien_num_ligne = 0

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
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
       
    def drop_down_bareme_change(self, **event_args):     # Bareme a changé
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
    
    def check_box_reponse_change(self, **event_args):   # Reponse a changé: 
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
  
    def button_modif_click(self, **event_args):   #ce n'est que l'orsque le user a clicker sur modif que je prend le contenu
        """This method is called when the button is clicked"""
  
        # je récupère mes question, reponse, bareme de la ligne du bouton pressé
        # Je remonte au parent (le flow panel)
        flowpanel = self.button_modif.parent    # conteneur d'1 ligne 
        
        repeat_item_panel = flowpanel.parent
        print("**** repeat panel4 *****", type(repeat_item_panel))   # conteneur objet ligne (item)
        
        repeat_panel = repeat_item_panel.parent
        print("**** repeating panel *****", type(repeat_panel))   # conteneur des lignes

        col_panel = repeat_panel.parent
        print("**** col panel *****", type(col_panel)) 
        
        
        
        for cpnt in flowpanel.get_components():
            print(cpnt, cpnt.tag)
            if cpnt.tag.nom == "num":
                num = int(cpnt.text)
            if cpnt.tag.nom =="question":
                question = cpnt.text
                prem_lettre = question[0].capitalize
                # A FAIRE; mettre la 1ere lettre en maj mais laisser le reste comme tappé
            if cpnt.tag.nom =="reponse":
                reponse = cpnt.checked
            if cpnt.tag.nom =="bareme":
                bareme = cpnt.selected_value
        
        result = anvil.server.call('modif_qcm', num, question, reponse, bareme)
        if not result:
            alert("erreur de création d'une question QCM")
            return
            
        # j'initialise la forme principale
        from anvil import open_form       
        open_form("QCM_visu_modif_Main")
        

   
        


    

        

    

        




 


        
        