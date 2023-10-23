from ._anvil_designer import RowTemplate3Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Visu_stages
from anvil import open_form

from alert2.alert2 import alert2

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
            
        self.text_box_1.text = self.item['numero']
        stage = self.item['code']['code']
        stage = stage.strip()
        self.text_box_2.text = self.item['code']['code']                     # link key
        if self.item['date_debut'] != None:
            self.text_box_3.text = self.item['date_debut'].strftime("%d/%m/%Y")   # format date française avec fonction Python strftime
        

    # récupération par l'event:
    def text_box_1_focus(self, **event_args):
        """This method is called when the button is clicked"""
        num_stage = int(self.text_box_1.text)
        open_form('Stage_visu_modif',"visu_stages", num_stage)   
    
    def text_box_2_focus(self, **event_args):
        """This method is called when the button is clicked"""
        self.text_box_1_focus()

    def text_box_3_focus(self, **event_args):
        """This method is called when the link is clicked"""
        self.text_box_1_focus()

    def button_inscription_click(self, **event_args):
        """This method is called when the button is clicked"""
   
        r=alert("Inscription de ce stagiaire ?",buttons=[("Non",False),("Oui",True)])
        if r :   #oui  
            a=alert2(role='outlined',
                  background='black',   
                  content='This is the body of my alert',
                  #content=   
                  header='This is the Title of my alert',    # header=False Will disable Header
                  footer_buttons=["No","Yes"],
                  close_button_color='red',
                  footer_buttons_align='center',footer_buttons_spacing='medium',
                  footer_color='green',
                  header_color='red', 
                  foreground='white',   
                  font_size=18,   
                  width=80  #amount of screen to be covered by the alert
                  )
         


            a.close()
            
            from ...Recherche_stagiaire import Recherche_stagiaire
            num_stage = self.text_box_1.text
            inscription = "inscription/"+num_stage
            
            table_temp = app_tables.temp.search()[0]
            table_temp.update(text=inscription)
        
            open_form('Recherche_stagiaire',inscription)


