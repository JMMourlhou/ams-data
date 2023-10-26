from ._anvil_designer import Pre_R_pour_type_stageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Pre_R_pour_type_stage(Pre_R_pour_type_stageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # Drop down codes stages
        self.drop_down_code_stage.items = [(r['code'], r) for r in app_tables.codes_stages.search()]
        self.drop_down_pre_requis.items = [(r["requis"], r) for r in app_tables.pre_requis.search()]
        # affiches toutes les lignes de la table pré requis
        
    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        self.column_panel_content.clear()
        #  lecture du dictionaire ds table codes_stages pour le stage sélectionné
        row = self.drop_down_code_stage.selected_value
        if row == None :
            alert("Vous devez sélectionner un stage !")
            self.drop_down_code_stage.focus()
            return
        
     
        # initialisation du dictionaire des pré requis pour ce type de stage
        if row['pre_requis'] == None:
            dico_pre_requis = {}
        #print(type(row['pre_requis']))
        if isinstance(row['pre_requis'], dict):
            dico_pre_requis ={}
            dico_pre_requis = row['pre_requis']
            # affichage des prérequis à partir du dico que je transforme  en liste
            liste = dico_pre_requis.keys()
            # j'affiche tous les pré requis
            print(liste)

            self.repeating_panel_1.items = list(liste)   # liste des clefs (pré requis)
        
                
                
                
        
        
            
      
        
        
    def drop_down_pre_requis_change(self, **event_args):
        """This method is called when an item is selected"""
        pass
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def button_creer_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass


    




