from ._anvil_designer import Pre_R_pour_type_stageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

global code_stage
code_stage = ""

global dico_pre_requis
dico_pre_requis = {}

class Pre_R_pour_type_stage(Pre_R_pour_type_stageTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        # Drop down codes stages
        self.drop_down_code_stage.items = [(r['code'], r) for r in app_tables.codes_stages.search()]
        self.drop_down_pre_requis.items = [(r["code_pre_requis"]+" "+r["requis"], r) for r in app_tables.pre_requis.search()]
        # affiches toutes les lignes de la table pré requis
        
    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        #lecture du dictionaire ds table codes_stages pour le stage sélectionné
        self.drop_down_pre_requis.visible = True
        row = self.drop_down_code_stage.selected_value
        if row == None :
            alert("Vous devez sélectionner un stage !")
            self.drop_down_code_stage.focus()
            return
     
        # initialisation du dictionaire des pré requis pour ce type de stage
        global code_stage
        code_stage = row["code"]
        
        if row['pre_requis'] == None:  # si le dictionaire n'existe pas encore (pas de pré requis encore introduit pour ce type de stage)
            dico_pre_requis = {}
        #print(type(row['pre_requis']))
        if isinstance(row['pre_requis'], dict):
            #dico_pre_requis ={}
            #global dico_pre_requis
            dico_pre_requis = row['pre_requis']
            # affichage des prérequis à partir du dico que je transforme  en liste
            list_keys = dico_pre_requis.keys()
            # j'affiche tous les pré requis
            print(len(list_keys))
            self.repeating_panel_1.items = list(list_keys)   # liste des clefs (pré requis)
        
    def drop_down_pre_requis_change(self, **event_args):
        """This method is called when an item is selected"""
        row = self.drop_down_pre_requis.selected_value
        if row == None :
            alert("Vous devez sélectionner un pré-requis !")
            self.drop_down_code_stage.focus()
            return
        #extraction de la clef à ajouter à partir de la row sélectionnée de la dropbox
        clef = row["code_pre_requis"]
        # rajout clef/valeur ds dico 
        global dico_pre_requis
        dico_pre_requis[clef]= {
                                "Doc": row["doc"],
                                "Validé": False,
                                "Commentaires": "",
                                "Nom_document": ""
                               }
        print(dico_pre_requis)

        global code_stage
        result = anvil.server.call("modif_pre_requis_codes_stages", code_stage, dico_pre_requis)
        alert(result)
        #réaffichage des pré requis
        self.drop_down_code_stage_change()
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)




    




