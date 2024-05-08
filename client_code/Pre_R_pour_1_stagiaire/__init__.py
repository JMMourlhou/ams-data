from ._anvil_designer import Pre_R_pour_1_stagiaireTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global code_stage
code_stage = ""

global dico_pre_requis     # dico de tous les pr existants
dico_pre_requis = {}
global dico_pre_requis_stg  # dico des pr pour ce stgiaire
dico_pre_requis_stg = {}

class Pre_R_pour_1_stagiaire(Pre_R_pour_1_stagiaireTemplate):
    def __init__(self,stagiaire_inscrit_row, **properties):  # row stagiaire inscrit, vient de pré_requis_pour stagiaire admin
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        nom = stagiaire_inscrit_row['name'].capitalize()
        pr = stagiaire_inscrit_row['prenom'].capitalize()
        self.label_3.text = "Pré-R pour "+nom+" "+pr+"  / "+stagiaire_inscrit_row['stage_txt']

        # liste des pré-requis existants du stagiaire
        liste_pr_stagiaire = app_tables.pre_requis_stagiaire.search( q.fetch_only("requis_txt",
                                                                       stagiaire_email=q.fetch_only("email"),
                                                                       ),
                                                            numero=int(stagiaire_inscrit_row['numero']),
                                                            stagiaire_email=stagiaire_inscrit_row["user_email"]
                                                         )
        # Création du dict des pr du stagiaire
        global dico_pre_requis_stg  # dico des pr pour ce stgiaire
        dico_pre_requis_stg = {}
        for pr_st in liste_pr_stagiaire:
            clef = pr_st['requis_txt']
            valeur = ""
            dico_pre_requis_stg[clef] = valeur
            print(dico_pre_requis_stg.keys())
        
        # INITIALISATION Drop down pré-requis possible du stagiaire, je ne prends pas un pré requis déjà sélectionné pour ce stagiaire
        liste_drop_d = []
        global dico_pre_requis
        dico_pre_requis = {}
        
        # search de tous les pré-requis existants
        liste_tous_pr = app_tables.pre_requis.search()
        for pr in liste_tous_pr:
            clef_search = dico_pre_requis_stg.get(pr['requis'])
            if clef_search is None:
                liste_drop_d.append((pr['requis'], pr))
                dico_pre_requis[pr['code_pre_requis']] = pr['requis']
                print("non existant: ", pr['requis'])
            else:
                print("existant: ", pr['requis'])
                
        self.drop_down_pre_requis.items = liste_drop_d
       
        
        
        # affichage des pré-requis du stagiaire
        self.repeating_panel_1.items = liste_pr_stagiaire


    def drop_down_pre_requis_change(self, **event_args):
        """This method is called when an item is selected"""
        row = self.drop_down_pre_requis.selected_value  # row du pre_requis
        if row is None:
            alert("Vous devez sélectionner un pré-requis !")
            self.drop_down_code_stage.focus()
            return
        else:
            clef = row[
                "code_pre_requis"
            ]  # extraction de la clef à ajouter à partir de la row sélectionnée de la dropbox
        # rajout clef/valeur ds dico
        global dico_pre_requis
        dico_pre_requis[clef] = {  # AJOUT DE LA CLEF DS LE DICO
            "Doc": row["doc"],
            "Validé": False,
            "Commentaires": "",
            "Nom_document": "",
        }

        # réaffichage des pré requis
        list_keys = dico_pre_requis.keys()
        print(list_keys)
        self.repeating_panel_1.items = list(list_keys)  # liste des clefs (pré requis)
        # réinitialisation dropdown pré requis
        self.drop_down_pre_requis.items = [
            (r["requis"], r)
            for r in app_tables.pre_requis.search()
            if not dico_pre_requis.get(r["code_pre_requis"])
        ]

        global code_stage
        result = anvil.server.call(
            "modif_pre_requis_codes_stages", code_stage, dico_pre_requis
        )

        self.sov_dico_ds_temp()  # sauvegarde du dico ds TABLE TEMP
        # =================================================================================================
        r = alert(
            "Voulez-vous ajouter ce pré-requis pour tous les stagiaires de ce type de stage ?",
            buttons=[("oui", True), ("non", False)],
        )
        if r:  # Oui
            liste_stages = app_tables.stages.search(code_txt=code_stage)
            print("nb de stages: ", len(liste_stages))
            # acquisition des stagiaires inscrits à ces stages
            for stage in liste_stages:
                print(stage["numero"])
                liste_stagiaires = app_tables.stagiaires_inscrits.search(
                    numero=stage["numero"]
                )
                # Pour chq stagiaire, ajout du pré_requis
                for stagiaire in liste_stagiaires:
                    print(stagiaire["name"])
                    # ajout du pré_requis si pas existant
                    test = app_tables.pre_requis_stagiaire.search(
                        stage_num=stage,
                        item_requis=row,
                        stagiaire_email=stagiaire["user_email"],
                    )
                    print("lg: ", len(test))
                    if len(test) == 0:
                        print("non existant")
                        result = anvil.server.call(
                            "add_1_pre_requis",
                            stage,
                            stagiaire["user_email"]["email"],
                            row,
                        )
                        print("ajout: ", result)

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form("Visu_stages")

