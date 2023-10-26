from ._anvil_designer import ItemTemplate5Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
global ancien_num_ligne    # pour pouvoir rendre un bt inactif si perte de focus
ancien_num_ligne = 0

class ItemTemplate5(ItemTemplate5Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.


        self.text_box_pre_requis.text = self.item['requis']
        self.text_box_pre_requis.tag.nom = "requis"
        self.text_box_pre_requis.tag.numero = self.item['num']

        """
        self.check_box_pre_requis.checked = False
        self.check_box_pre_requis.tag.nom = "reponse"
        self.check_box_pre_requis.tag.numero = self.item['num']
        """
        
        self.button_modif.tag.numero = self.item['num']          #Je sauve le NUMERO du pre requis ds le tag
        self.button_modif.tag.nom = "button"


    """
    def text_box_question_change(self, **event_args):   # Question a changé
        """This method is called when the text in this text box is edited"""
        # je récupère le contenu du cpnt
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"

 
    def check_box_reponse_change(self, **event_args):   # ckeck box a changé:
        """This method is called when this checkbox is checked or unchecked"""
        self.button_modif.enabled = True
        self.button_modif.background = "red"
        self.button_modif.foregroundground = "yellow"
        global ancien_num_ligne
        ancien_num_ligne = self.check_box_reponse.tag.numero

    def button_modif_click(self, **event_args):   #ce n'est que l'orsque le user a clicker sur modif que je prend le contenu
        """This method is called when the button is clicked"""

        # je récupère mes question, reponse, bareme de la ligne du bouton pressé
        # Je remonte au conteneur parent du bouton (le flow panel)
        flowpanel = self.button_modif.parent    # conteneur d'1 ligne
        for cpnt in flowpanel.get_components():
            print(cpnt, cpnt.tag)
            if cpnt.tag.nom == "num":
                num = int(cpnt.text)
            if cpnt.tag.nom =="question":
                question = cpnt.text
                # mettre la 1ere lettre en maj mais laisser le reste comme tappé
                #je boucle à partir de la deuxieme lettre et cumul le text


                txt = question[0].capitalize()    # txt commence par la position 1 de la question, mise en majuscule
                txt2 = question[1:len(question)]   #Slice je prends toute la question à partir de la position 2
                #print(txt+txt2)
                """
                for x in range(1,len(question)):  # je pars de la position2 et boucle j'usquà la fin de la question
                    txt = txt + question[x]
                """
                question = txt + txt2
            if cpnt.tag.nom =="reponse":
                reponse = cpnt.checked
            if cpnt.tag.nom =="bareme":
                bareme = cpnt.selected_value

        result = anvil.server.call('modif_qcm', num, question, reponse, bareme)
        if not result:
            alert("erreur de création d'une question QCM")
            return

        # j'initialise la forme principale
        from anvil import open_form
        open_form("QCM_visu_modif_Main")

    def text_box_question_lost_focus(self, **event_args):
        """This method is called when the TextBox loses focus"""
        global ancien_num_ligne
        ancien_num_ligne = self.text_box_question.tag.numero

    def text_box_question_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        num = self.text_box_question.tag.numero
        # Je recherche le bouton de l'ancienne ligne pour le désactiver
        #Je remonte du component sur 3 niveaux (jusqu'au repeat panel de la form 'QCM_visu_modif')
        global ancien_num_ligne
        if ancien_num_ligne != 0 and num != ancien_num_ligne:
            flowpanel = self.button_modif.parent    # conteneur d'1 ligne
            repeat_item_panel = flowpanel.parent    # conteneur objet ligne (item)
            repeat_panel = repeat_item_panel.parent  # conteneur des lignes (repeat panel) ds QCM_visu_modi
            #print("**** repeating panel *****", type(repeat_panel))

            for item_lignes in repeat_panel.get_components():
                for ligne in item_lignes.get_components():
                    for cpnt in ligne.get_components():
                        if cpnt.tag.nom == "button" and cpnt.tag.numero == ancien_num_ligne:
                            #c'est le bt de l'ancienne ligne
                            self.button_modif.enabled = False
                            self.button_modif.background = "theme:Tertiary"
                            self.button_modif.foregroundground = "theme:Error"
                            ancien_num_ligne = 0
    """