from ._anvil_designer import Formulaire_par_type_stageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

global dico_formulaire
dico_formulaire = {}

global dico_test
dico_test = {}

class Formulaire_par_type_stage(Formulaire_par_type_stageTemplate):
    def __init__(self, code_stage="", **properties):  # code stage si vient d'annulation d'un pré_requis ds R.RowTemplate1
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.text_area_sov_dico.text = {}
        # Initialisation drop down codes stages
        liste = [(r["code"], r)for r in app_tables.codes_stages.search(tables.order_by("code", ascending=True))]
        self.drop_down_code_stage.items = liste
        if (code_stage != ""):  # si vient d'annulation d'un pré_requis ds R.RowTemplate1, je pre selectionne la dropdown stage
            row = app_tables.codes_stages.get(code=code_stage)
            self.drop_down_code_stage.selected_value = row
            self.drop_down_code_stage_change()

    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        # lecture du dictionaire ds table codes_stages pour le stage sélectionné
        self.row_stage = self.drop_down_code_stage.selected_value
        if self.row_stage is None:
            alert("Vous devez sélectionner un stage !")
            self.drop_down_code_stage.focus()
            return
        self.drop_down_type_formulaire.visible = True
         
    
    def drop_down_type_formulaire_change(self, **event_args):
        """This method is called when an item is selected"""
        global dico_test
        global dico_formulaire
        self.repeating_panel_2.visible = False
        type_formulaire = self.drop_down_type_formulaire.selected_value
        type_formulaire = str(type_formulaire[0:5])
        
        # initialisation de la liste des textes formulaires de la table texte_formulaires
        # lecture du dictionaire pour ce type de stage et type de formulaire
    
        if type_formulaire == "SAT_F":
            dico_formulaire = self.row_stage["satisf_q_ferm_template"]
            dico_test = self.row_stage["satisf_q_ferm_template"]
        if type_formulaire == "SAT_O":
            dico_formulaire = self.row_stage["satisf_q_ouv_template"]
            dico_test = self.row_stage["satisf_q_ouv_template"]
        if type_formulaire == "SUI_F":
            dico_formulaire = self.row_stage["suivi_stage_q_ferm_template"]
            dico_test = self.row_stage["suivi_stage_q_ferm_template"]
        if type_formulaire == "SUI_O":
            dico_formulaire = self.row_stage["suivi_stage_q_ouv_template"]
            dico_test = self.row_stage["suivi_stage_q_ouv_template"]
        if type_formulaire == "com_F":
            dico_formulaire = self.row_stage["com_ferm"]
            dico_test = self.row_stage["com_ferm"]
        if type_formulaire == "com_O":
            dico_formulaire = self.row_stage["com_ouv"]
            dico_test = self.row_stage["com_ouv"]
        # affichage repeating panel et maj drop down des textes dispos    
        self.maj_display()
        # Sauvegarde du dico_formulaire ds la variable text-area _sov_dico
       
        self.text_area_sov_dico.text = dico_test
        
    def drop_down_textes_formulaire_change(self, **event_args):
        """This method is called when an item is selected"""
        global dico_formulaire
        global dico_test
        row = self.drop_down_textes_formulaire.selected_value  # row du texte
        if row is None:
            alert("Vous devez sélectionner un pré-requis !")
            self.drop_down_code_stage.focus()
            return
        else:
            clef = row["code"]  # extraction de la clef à ajouter à partir de la row sélectionnée de la dropbox
            
        # rajout clef/valeur ds dico dico_test
        
        obl = ""
        if row["obligation"] is True:
            obl = "obligatoire"
        else:
            obl = "facultative"
        dico_formulaire[clef] = [                          # AJOUT DE LA CLEF DS LE DICO
                                row["text"],
                                obl    
                                ]
        
        # rajout clef/valeur ds dico dico_formulaire
        clef = len(dico_test)
        
        obl = ""
        if row["obligation"] is True:
            obl = "obligatoire"
        else:
            obl = "facultative"
        dico_formulaire[clef] = [                          # AJOUT DE LA CLEF DS LE DICO
                                row["text"],
                                obl    
                                ]
        # Sauvegarde du dico_formulaire ds la variable text-area _sov_dico
        self.text_area_sov_dico.text = dico_test
        # affichage repeating panel et maj drop down des textes dispos    
        self.maj_display() 
        self.sov_dico()
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Parametres import Parametres
        open_form("Parametres")

    def maj_display(self):   
        global dico_formulaire
        list_textes = app_tables.texte_formulaires.search(tables.order_by("code", ascending=True))
        # affichage du repeating panel des textes dèjà dans le dictionaire lu 
        if dico_formulaire != {}:   
            # dico doit être transformé en liste
            list_keys = dico_formulaire.keys()
            list_keys = sorted(list_keys)  # création de la liste triée des clefs du dictionaire formulaire
            # j'affiche tous les pré requis
            print('nb de clés: ',len(list_keys))
            self.repeating_panel_2.visible = True
            self.repeating_panel_2.items = list(list_keys)  # liste des clefs (code des formulaires)
            """
            self.sov_dico_ds_temp()  # sauvegarde du dico ds TABLE TEMP
            """
        # Initialisation drop down textes_formulaire 
        type_formulaire = self.drop_down_type_formulaire.selected_value
        list_drop_down = []
        for row in list_textes:
            cod=row["code"][0:5]
            if cod == type_formulaire:
                # si ce texte n'est pas déjà dans les clés du dico_formulaire,je l'affiche
                if not dico_formulaire.get(row["code"]):
                    list_drop_down.append((row["text"],row))
        self.drop_down_textes_formulaire.items=list_drop_down       
        self.drop_down_textes_formulaire.visible = True

    def sov_dico(self):
        # modif du dico test en table codes_stages
        code_stage_row = self.drop_down_code_stage.selected_value
        global dico_test
        type_formulaire = self.drop_down_type_formulaire.selected_value
        result = anvil.server.call("modif_dico_formulaire_codes_stages", code_stage_row, dico_test, type_formulaire )
        if not result:
            alert("Erreur: l'écriture du dictionnaire non effectuée !")
        
    def sov_dico_ds_temp(self, **event_args):
        table_temp = app_tables.temp.search()[0]  # sauvegarde du dico ds TABLE TEMP
        global code_stage
        global dico_pre_requis
        table_temp.update(pre_r_pour_stage=dico_pre_requis, code_stage=code_stage)