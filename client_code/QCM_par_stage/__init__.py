from ._anvil_designer import QCM_par_stageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class QCM_par_stage(QCM_par_stageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.f = get_open_form()
        # Drop down codes types de stages
        liste = [(r['code'], r) for r in app_tables.codes_stages.search(tables.order_by("code", ascending=True))]   
        self.drop_down_types_stages.items = liste
    
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        open_form(self.f)

    def drop_down_types_stages_change(self, **event_args):
        """This method is called when an item is selected"""
        self.stage_row = self.drop_down_types_stages.selected_value
        
        # Tous les qcm
        self.liste_qcm_descro = app_tables.qcm_description.search(tables.order_by("destination", ascending=True))  
        print(f"nb de qcm: {len(self.liste_qcm_descro)}")  
        
        # lecture du dictionaire du stage
        self.dict = self.stage_row["droit_qcm"] 
        
        # panel des qcms (MOINS LES QCM DEJA SELECTIONNE POUR CE STAGE)
        if self.dict is not None and self.dict != {}:     # ni None, ni {}
            # Enlever les qcm déjà sélectionnés
            liste_qcm_dispos = []
            liste_qcm_selectionnes = []
            for qcm in self.liste_qcm_descro:
                clef_search = self.dict.get(str(qcm['qcm_nb']))   # recherche sur le num du qcm (doit être str)
                if clef_search is None:  
                    # ce qcm n'est pas ds le dict du stage, je l'affiche ds panel 1, qcm dispos
                    print(qcm['destination'])
                    liste_qcm_dispos.append((qcm['qcm_nb'], qcm['destination'], qcm['visu_qcm_par_stage']))
                else: # ce qcm est ds le dict du stage, je l'affiche ds panel 2, qcm selectionnés
                    liste_qcm_selectionnes.append((qcm['qcm_nb'], qcm['destination'], qcm['visu_qcm_par_stage']))
                    
        else: # si pas de dict, j'affiche ts les qcm
            liste_qcm_dispos = self.liste_qcm_descro
            liste_qcm_selectionnes = []
            
        print(f"Nb de qcm dipos: {len(liste_qcm_dispos)}")
        self.repeating_panel_1.visible = True
        self.repeating_panel_1.items = liste_qcm_dispos

        print(f"Nb de qcm sélectionnés: {len(liste_qcm_selectionnes)}") 
        self.repeating_panel_2.visible = True
        self.repeating_panel_2.items = liste_qcm_selectionnes
        
        