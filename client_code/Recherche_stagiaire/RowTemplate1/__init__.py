from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from InputBox.input_box import InputBox, alert2, input_box, multi_select_dropdown

global num_stage  # pour le click sur button_5 et envoie ds le stage
num_stage = 0

global cpt   # pour afficher le dernier stage assisté ds bt 5
cpt = 0

class RowTemplate1(RowTemplate1Template):
    def __init__(self, **properties):
        
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        
        try:          # Liste à partir table users
            cumul_clefs_histo = ""
            if self.item['histo'] == None:
                msg = self.item['nom']+" "+self.item['prenom'] + " avec histo sans {} (table 'users')"
                alert(msg)
                return
                
            if self.item['histo'] != {} or self.item['histo'] != None:   #lecture du dictionnaire historique des stages du stagiaire
                historique = self.item['histo']
                cpt = 1
                for clef,valeur in historique.items():   #Boucle sur le dictionnaire histo ds Users
                    print(clef)
                    global num_stage
                    num_stage = valeur[0]   # le num stage est le premier élément de valeur (clef:valeur) 
                    test_tag_vide = self.button_5.tag
                    if cpt == 1:   # si c'est le stage le plus récent, je le retient pour l'afficher si bt 5 clické
                        self.button_5.tag = num_stage
                    cpt += 1
                    cumul_clefs_histo = cumul_clefs_histo + " " + clef

            self.button_1.text = self.item['nom']+" "+self.item['prenom']
            self.button_3.text = self.item['tel']
            self.button_4.text = self.item['email']
            if len(historique)>1:
                self.button_5.height = 36 * len(historique)
            self.button_5.text = cumul_clefs_histo.lstrip()
        except: # ***********************************  Liste à partir table Stagiaires inscrits
            # lecture table users à partir du mail du stagiaire
            mel = self.item['user_email']['email']
            user = app_tables.users.get(email=mel)
            self.button_1.text = user['nom']+" "+user['prenom']
            self.button_3.text = user['tel']
            self.button_4.text = user['email']
            # lecture fichier père stage pour obtenir le num et date du stage
            st = self.item['stage']['numero']
            stg = app_tables.stages.get(numero=st)
            self.button_5.text = str(stg['date_debut'])+" / "+str(stg['numero'])
            self.button_5.tag = st
            
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
                txt_msg = anvil.server.call("add_stagiaire", stagiaire_row, stage, code_fi, type_add="bt_recherche")
                alert(txt_msg)
                open_form('Recherche_stagiaire', contenu)  # réouvre la forme mère pour mettre à jour l'affichage de l'histo
            
    def button_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_1_click()

    def button_4_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_1_click()

        

    def column_panel_1_show(self, **event_args):
        """This method is called when the column panel is shown on the screen"""
        global cpt
        cpt += 1

    def button_5_focus(self, **event_args):
        """This method is called when the text area gets focus"""
        if self.button_5.text != "":
            num_stage = self.button_5.tag
            
            if num_stage != 0:
                open_form('Stage_visu_modif',"recherche",num_stage) 





        
        
        