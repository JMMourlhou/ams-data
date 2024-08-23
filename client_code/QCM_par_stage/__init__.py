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
        # lecture du dictionaire du stage
        self.dict = self.stage_row["droit_qcm"]
        self.column_panel_1.visible = True
        
        # panel panel des qcms (MOINS LES QCM DEJA SELECTIONNE POUR CE STAGE)
        # Tous les qcm
        self.liste_qcm_descro = app_tables.qcm_description.search(tables.order_by("destination", ascending=True))  
        # Enlever les qcm déjà sélectionnés
        liste = []
        for qcm in self.liste_qcm_descro:
            clef_search = self.dict.get(str(qcm['qcm_nb']))   # recherche sur le num du qcm (doit être str)
            if clef_search is None:                           # si ce qcm n'est pas sélectionné, je l'afficherai
                liste.append(qcm['destination'])
                                                  
        self.repeating_panel_1.items = list(liste)
                                                                
        
        