from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from InputBox.input_box import InputBox, alert2, input_box, multi_select_dropdown


class RowTemplate1(RowTemplate1Template):
    def __init__(self, **properties):
        
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.repeating_panel_1.visible = False  #qcm non visibles tant que pas de click sur bt Qcm
        try: # *********************************          Liste à partir table users
            if self.item['prenom'] != None:    # si prénom None, erreur
                self.button_1.text = self.item['nom']+" "+self.item['prenom']
                if self.item['role'] != "S":
                    self.button_1.foreground = "red"
            else:
                self.button_1.text = self.item['nom']
            self.button_3.text = self.item['tel']
            self.button_4.text = self.item['email']
            self.button_qcm.tag = self.item['email']
            self.button_histo.tag = self.item['email']
            self.drop_down_code_stage.tag = self.item['email']
            stagiaire_row = app_tables.users.get(email=self.item['email']) # pour pré-requis         
        except: # ***********************************  Liste à partir table Stagiaires inscrits
            mel = self.item['user_email']['email']
            user_row = app_tables.users.get(email=mel)
            stagiaire_row = user_row # pour les pré-requis
            self.button_1.text = user_row['nom']+" "+user_row['prenom']
            self.button_3.text = user_row['tel']
            self.button_4.text = user_row['email']
            self.button_histo.tag = user_row['email']
            self.drop_down_code_stage.tag = user_row['email']
            
        # Drop down stages inscrits du stagiaire pour les pré-requis du stage sélectionnés
        liste0 = app_tables.stagiaires_inscrits.search(user_email=stagiaire_row)
        #print("nb; ", len(liste0))
        liste_drop_d = []
        for row in liste0:
            #lecture fichier père stage
            stage=app_tables.stages.get(numero=row['stage']['numero'])
            #lecture fichier père type de stage
            type=app_tables.codes_stages.get(code=stage['code']['code'])
            liste_drop_d.append((type['code']+"  du "+str(stage['date_debut']), row))
        #print(liste_drop_d)
        self.drop_down_code_stage.items = liste_drop_d   
        
            
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        """
        Je ne peux pas remonter ds mes components pour savoir si je suis en mode "inscription",
            à partir de la forme Visu_stages
        Donc j'utilise la table Temp qui contient la raison d'entrée en recherche : recherche ou inscription
        """
        temp_row1 = app_tables.temp.search()[0]  # lecture de 1ere ligne fichier temp
        contenu = str(temp_row1['text'])

        if contenu[0:1] == "r":  # recherche
            try:
                mel = self.item['email']   
            except:
                mel = self.item['user_email']['email']

            from ...Saisie_info_apres_visu import Saisie_info_apres_visu
            open_form('Saisie_info_apres_visu', mel, num_stage=0, intitule="", provenance="recherche")
            
        if contenu[0:1] == "i":  # inscription du stagiaire au stage
            #alert(contenu)
            mel = self.item['email']
            stagiaire_row = app_tables.users.get(email=mel)
            #alert(stagiaire_row['email'])
            stage = contenu[12:15]

            # Choix du mode de financement / Création d'une box incluant le drop down mode de fi
            def show_results(self, result):
                #alert(result)
                pass
            
            #def input_box_show(rows, **event_args):
                #rows['counter'].label.content = 'Sélectionnez le mode de fi'
                
            def dropdown_change(results, rows, **event_args):
                pass                

            result={}
            nom_dropdown = 'mode_fi'  # sera également la clef du dictionnaire de sortie/résultat ib.results
            ib = InputBox('Choix du mode de financement', ['OK', 'Cancel'], default_button='OK',large=True)  # si touche return = OK
            #ib = InputBox('Choix du mode de financement', ['OK', 'Cancel'], default_button='OK', form_show=input_box_show)
            row = app_tables.mode_financement.get(code_fi="??")   #Pour sélectionner la row selected value de dropdown
            ib.add_dropdown(name=nom_dropdown, prompt="",items=[(r['intitule_fi'], r) for r in app_tables.mode_financement.search(tables.order_by("intitule_fi", ascending=True))], selected_value=row,events=[('change', dropdown_change)])
            # Je peux rajouter ds ma input box d'autres components:
            #ib.add_textbox(text=30, prompt='Width:', visible=True)  # visible True par défaut
            #ib.add_textbox(text=20, prompt='Height:', visible=True)
            #ib.add_richtext('Initial text', name='counter', visible = True)
            ib.show()
            #alert(ib.results)
            result=ib.results   #dictionaire  clef 'mode_fi' valeur=row table Mode_financement sélectionnée
            # ex de result:     {'mode_fi': <anvil.tables.Row: code_fi='ASS', intitule_fi='Association finance'>, 'clicked_button': 'OK'}
            valid = result.get('clicked_button')   # extraction de la valeur de la clef 'code_fi' ds dropdown 'mode_fi'
            if valid == 'OK':
                code_fi = result.get('mode_fi')['code_fi']   # ds dict 'result', extraction de la valeur de la clef 'mode_fi' (row, col 'code_fi')
                #alert(code_fi)
                if code_fi == "??":
                    alert("Sélectionner un mode de financement")
                    return
                txt_msg = anvil.server.call("add_stagiaire", stagiaire_row, stage, code_fi, type_add="bt_recherche")
                alert(txt_msg)
                open_form('Recherche_stagiaire', contenu)  # réouvre la forme mère pour mettre à jour l'affichage de l'histo
            
    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_1_click()

    def button_4_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_1_click()

    def button_qcm_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.repeating_panel_1.visible == False:
            self.repeating_panel_1.visible = True
            self.button_qcm.foreground = "red"
            self.button_1.foreground = "red"
            try:  # si recherche sur la table users
                stagiaire = app_tables.users.get(email=self.item['email'])
                qcm_results = app_tables.qcm_result.search(
                                                            tables.order_by("time", ascending=False),
                                                            user_qcm = stagiaire
                                                            )
            except: # si recherche sur la table
                stagiaire = app_tables.users.get(email=self.item['user_email']['email'])
                qcm_results = app_tables.qcm_result.search(
                                                            tables.order_by("time", ascending=False),
                                                            user_qcm = stagiaire
                                                            )
            if len(qcm_results)>0:      # qcm trouvés pour ce user
                    self.repeating_panel_1.items = qcm_results
        else:
            self.repeating_panel_1.visible = False
            self.button_1.foreground = "theme:Tertiary"               #yellow
            #self.button_1.background = "theme:On Primary Container"

    def button_histo_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.repeating_panel_2.visible == False:
            self.repeating_panel_2.visible = True
            self.button_histo.foreground = "red"
            self.button_1.foreground = "red"
            #self.button_1.background = "theme:On Primary Container"
            try:  # si recherche sur la table users
                stagiaire = app_tables.users.get(email=self.item['email'])
            except:
                stagiaire = app_tables.users.get(email=self.item['user_email']['email'])
            self.repeating_panel_2.items = app_tables.stagiaires_inscrits.search(user_email = stagiaire)
        else:
            self.repeating_panel_2.visible = False
            self.button_1.foreground = "theme:Tertiary"               #yellow
            #self.button_1.background = "theme:On Primary Container"

    def drop_down_code_stage_change(self, **event_args):
        """This method is called when an item is selected"""
        self.repeating_panel_3.visible = True
        row_stagiaire_inscrit = self.drop_down_code_stage.selected_value   # Stage sélectionné du user ds drop_down (row table stagiaire inscrit)
        if row_stagiaire_inscrit != None:
            # lecture fichier père stages
            row_stage = app_tables.stages.get(numero=row_stagiaire_inscrit['stage']['numero'])
            print(row_stage['numero'])
            # lecture des pré requis pour ce stage et pour ce stagiaire
            stagiaire_email = self.drop_down_code_stage.tag
            stagiaire_row = app_tables.users.get(email=stagiaire_email)
            liste_pr = app_tables.pre_requis_stagiaire.search(stagiaire_email=stagiaire_row,
                                                            stage_num=row_stage
                                                            )
            print(len(liste_pr))
            self.repeating_panel_3.items = liste_pr
        else:
            self.repeating_panel_3.visible = False
            








        
        
        