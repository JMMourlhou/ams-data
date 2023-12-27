from ._anvil_designer import RowTemplate3Template
from anvil import *
import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Visu_stages
from anvil import open_form

from InputBox.input_box import InputBox, alert2, input_box, multi_select_dropdown

#import anvil.js    # pour screen size
from anvil.js import window # to gain access to the window object
global screen_size
screen_size = window.innerWidth

class RowTemplate3(RowTemplate3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        if screen_size < 800:
            self.text_box_1.visible = False
        else:
            self.text_box_1.visible = True
            self.button_inscription.text = "Inscription"
            self.button_pre_requis.text = "Pré-requis"
            
        self.text_box_1.text = self.item['numero']
        stage = self.item['code']['code']
        stage = stage.strip()
        self.text_box_2.text = self.item['code']['code']                     # link key
        if self.item['date_debut'] != None:
            self.text_box_3.text = self.item['date_debut'].strftime("%d/%m/%Y")   # format date française avec fonction Python strftime
        

    # récupération par l'event:
    def text_box_3_click(self, **event_args):   # Click sur date
        """This method is called when the button is clicked"""
        self.text_box_1_click()
        
    def text_box_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        num_stage = int(self.text_box_1.text)
        open_form('Stage_visu_modif',"visu_stages", num_stage)   
        
    def text_box_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.text_box_1_click()

    def button_inscription_click(self, **event_args):
        """This method is called when the button is clicked"""
        r=alert2('Si vous voulez effectuer une **inscription**:\n\n'
               '```\n'
               '1- Cliquez sur "Oui"\n'
               '2- Recherchez le stagiaire\n'
               '   à inscrire\n'
               '3- Cliquez sur son nom\n'
                '```\n' 
                ,
                buttons=['Oui', 'Non'],
                default_button='Oui',     # si press return=Oui
                large=True
                )
        if r== "Oui" :   
            from ...Recherche_stagiaire import Recherche_stagiaire
            num_stage = self.text_box_1.text
            inscription = "inscription/"+str(num_stage)
            
            table_temp = app_tables.temp.search()[0]
            table_temp.update(text=inscription)
        
            open_form('Recherche_stagiaire',inscription)

    def button_pr_requis_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ...Pre_R_pour_stagiaire_admin import Pre_R_pour_stagiaire_admin
        num_stage = int(self.text_box_1.text)
        open_form('Pre_R_pour_stagiaire_admin',num_stage)



  


