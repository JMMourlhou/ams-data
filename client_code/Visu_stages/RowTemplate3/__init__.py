from ._anvil_designer import RowTemplate3Template
from anvil import *

import anvil.server


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
        
        self.button_qcm.tag.stage = self.item['numero']  #numero de stage en tag du bouton self.button_qcm
        if screen_size < 800:
            self.text_box_1.visible = False
            if self.item['date_debut'] != None:
                self.text_box_3.text = self.item['date_debut'].strftime("%m/%Y")   # format date française avec fonction Python strftime
        else:
            self.text_box_1.visible = True
            self.button_inscription.text = "Inscription"
            self.button_pre_requis.text = "Pré-requis"
            if self.item['date_debut'] != None:
                self.text_box_3.text = self.item['date_debut'].strftime("%d/%m/%Y")   # format date française avec fonction Python strftime
            self.button_qcm.text = "Résultats des QCM"
            
        self.text_box_1.text = self.item['numero']
        stage = self.item['code']['code']
        stage = stage.strip()
        if len(self.item['commentaires'])>2:
            self.text_box_2.text = self.item['code']['code']+" "+self.item['commentaires'][0:3]                  # ajout des 3 1eres lettres du commentaire (pour quel stage)
        else:
            self.text_box_2.text = self.item['code']['code']

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
            #print("test inscription;",num_stage)
            inscription = "inscription/"+str(num_stage)
            
            table_temp = app_tables.temp.search()[0]
            table_temp.update(text=inscription)
        
            open_form('Recherche_stagiaire',inscription)

    def button_pr_requis_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ...Pre_R_pour_stagiaire_admin import Pre_R_pour_stagiaire_admin
        num_stage = int(self.text_box_1.text)
        open_form('Pre_R_pour_stagiaire_admin',num_stage)

    def button_qcm_click(self, **event_args):
        """This method is called when the button is clicked"""
        #lecture du stage du stage à partir du tag du bt self.button_qcm
        num_stage_int = self.button_qcm.tag.stage
        # lecture du stage
        stage_row = app_tables.stages.get(numero=num_stage_int)
        if stage_row:
            #print("stage: ", stage_row['numero'])
            from ...QCM_Results import QCM_Results
            open_form('QCM_Results', stage_row)

  


