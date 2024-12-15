from ._anvil_designer import EvenementsTemplate
from anvil import *
import anvil.server

import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import French_zone   #pour afficher la date du jour
from datetime import datetime

# Change les bt 'apply' en 'Valider' si je veux saisir l'heure en même tps que la date (picktime set à True)
# VOIR DATE PICKER, SHOW EVENT

# Saisie d'un évenement ou d'un incident 
#   Pb rencontré: session expired si la saisie est intérrompue 
    # 2 Solutions implémentées:  - Un 'ping' sur le serveur toutes les 5 minutes (300" timer 1) empêche la session d'expirée (sur un ordinateur) 
    #                                mais pas sur un tel qd l'écran s'étteint.  
    #                            - Une sauvegarde auto toutes les 30 secondes (timer 2), ce qui permet de ne pas perdre bp de données si expired. 

class Evenements(EvenementsTemplate):
    def __init__(self, to_be_modified_row=None, origine="", **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.f = get_open_form()
        # origine n'est pas vide si cette forme a été appelée en modification (click sur une row en Evenements_visu_modif_del)
        #    permet de tester l'origine si BT annuler est cliqué
        self.origine = origine  
        
        # Drop down codes lieux
        self.drop_down_lieux.items = [(r['lieu'], r) for r in app_tables.lieux.search(tables.order_by("lieu", ascending=True))]
        for lieu in self.drop_down_lieux.items:
            print(lieu, lieu[0], lieu[1])
        liste=self.drop_down_lieux.items[0]
        self.drop_down_lieux.selected_value = liste[1]

        self.now = French_zone.french_zone_time()   # now est le jour/h actuelle (datetime object)
        date0 = self.now.date()                     # exraction de la date uniqt 
        self.date_sov = date0.strftime("%Y/%m/%d")

        # Test si ouverture en mode Création ou modif (self.to_be_modified_row = None si création)
        self.to_be_modified_row = to_be_modified_row
        if self.to_be_modified_row is None:
            # Creation
            self.id = None
            self.outlined_card_main.visible = False
            
            self.image_1.source = None
            self.outlined_card_1.visible = False
            
            self.image_2.source = None
            self.outlined_card_2.visible = False
            
            self.image_3.source = None
            self.outlined_card_3.visible = False
        else:
            # Modif à partir du row passé en init par la form Evenements_visu_modif_del
            self.id=self.to_be_modified_row.get_id()
            # initilisation des composants de cette forme par le row passé en init par la form Evenements_visu_modif_del

            #   0123456789
            # t=2023/01/17
            t = self.to_be_modified_row["date"]
            # Extraire l'année, le mois et le jour à partir de la chaîne
            yy=t[0:4]  # 0 à 4, 4 non inclus
            mm=t[5:7]
            dd=t[8:10]
            # Création de la variable de type date 
            date1 = datetime(int(yy), int(mm), int(dd))
            self.date_picker_1.pick_time = True
            self.date_picker_1.date = date1
            self.drop_down_event.selected_value = self.to_be_modified_row["type_event"]
            self.drop_down_lieux.selected_value = self.to_be_modified_row["lieu"]
            self.text_area_mot_clef.text = self.to_be_modified_row["mot_clef"]
            self.text_area_notes.text = self.to_be_modified_row["note"]
            
            if self.to_be_modified_row["img1"] is not None:
                self.image_1.source = self.to_be_modified_row["img1"]
                self.column_panel_trav_sur_img_1.visible = True
                self.flow_panel_loader_1.visible = False
            else:
                self.image_1.source = None
                self.outlined_card_1.visible = False
                self.flow_panel_loader_1.visible = True

            if self.to_be_modified_row["img2"] is not None:
                self.image_2.source = self.to_be_modified_row["img2"]
                self.column_panel_trav_sur_img_2.visible = True
                self.flow_panel_loader_2.visible = False
            else:
                self.image_2.source = None
                self.outlined_card_2.visible = False
                self.flow_panel_loader_2.visible = True
                
            if self.to_be_modified_row["img3"] is not None:
                self.image_3.source = self.to_be_modified_row["img3"]
                self.column_panel_trav_sur_img_3.visible = True
                self.flow_panel_loader_3.visible = False
            else:
                self.image_3.source = None
                self.outlined_card_3.visible = False
                self.flow_panel_loader_3.visible = True
                
            self.flow_panel_lieu_date.visible = True
            self.outlined_card_main.visible = True
            
        # Init drop down event (Pour l'instant choix à rentrer pour ne pas perdre les notes si je change le type d'evenmt)
        """
        self.drop_down_event.selected_value = self.drop_down_event.items[0]  # "Réunion"
        self.note_for_meeting("meeting")
        """
        
        # Init drop down date avec Date du jour et acquisition de l'heure
        t = str(self.now)
        # Extraire l'année, le mois et le jour à partir de la chaîne
        yy=t[0:4]  # 0 à 4, 4 non inclus
        mm=t[5:7]
        dd=t[8:10]
        hh=t[11:13]
        mi=t[14:16]
        # Création de la variable de type date 
        date1 = datetime(int(yy), int(mm), int(dd), int(hh), int(mi))
        self.date_picker_1.pick_time = True
        self.date_picker_1.date = date1


    def drop_down_event_change(self, **event_args):
        """This method is called when an item is selected"""
        #self.drop_down_event.selected_value = self.drop_down_event.items[0]  # "Réunion"
        self.type = self.drop_down_event.selected_value
        if self.type == "Réunion" or self.type == "Incident":
            self.flow_panel_lieu_date.visible = True
            self.outlined_card_main.visible = True
            if self.type == "Réunion":
                self.note_for_meeting("meeting")
            if self.type == "Incident":
                self.note_for_meeting("incident")


    def note_for_meeting(self, type):
        #now = French_zone.french_zone_time()   # now est le jour/h actuelle (datetime object)
        heure = self.now.time()
        heure = heure.strftime("%H:%M")
        date0 = self.now.date()
        date = date0.strftime("%d/%m/%Y")
        if type == "meeting":
            self.text_area_notes.text = (f"Participants : A.C / A.JC / G.J / M.JM / L.C \nObjet : Réunion d'équipe du {date} à {heure}\n\nNotes :\n ")
        if type == "incident":
            self.text_area_notes.text = ("Incident,    notes prises par : \nDate de l'incident : \nHeure de l'incident : \nPersonne(s) impliquée(s) : \nTémoins : \nNotes : ")

    def text_area_commentaires_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.button_validation.visible = True
        #self.button_validation_1.visible = True
        self.button_validation_2.visible = True

    # validation:   auto_sov True si sauvegarde auto tte les 30", appelé par timer_2_tick
    def button_validation_click(self, auto_sov=False, id=None, **event_args):
        """This method is called when the button is clicked"""
        writing_date_time = French_zone.french_zone_time()   # now est le jour/h actuelle (datetime object)
        row_lieu = self.drop_down_lieux.selected_value
        lieu_txt = row_lieu['lieu']
        result, self.id = anvil.server.call("add_event", 
                                                    self.id,                                  # row id   pour réécrire le row en auto sov tt les 30"
                                                    auto_sov,                                 # False si bt validation utilisé   /   True si sauvegarde auto lancée par timer2, ts les 30 secondes
                                                    self.drop_down_event.selected_value,      # Type event
                                                    self.date_sov,                            # date
                                                    row_lieu,                                 # lieu row
                                                    lieu_txt,                                 # lieu en clair
                                                    self.text_area_notes.text,                # notes    
                                                    self.image_1.source,                      # image 1
                                                    self.image_2.source,
                                                    self.image_3.source,
                                                    writing_date_time,                        # Date et heure de l'enregistrement
                                                    self.text_area_mot_clef.text              # Mot clef pour accès rapide en recherche
                                     )       
        if not result :
            alert("Evenement non sauvegardé !")
        # si la sauvegarde a été effectué en fin de saisie de l'évenemnt (clique sur Bt 'Valider'), on sort en modifiant le tag sov_incorrecte False ds le row de l'event
        if auto_sov is False: 
            # sortie normale
            open_form(self.f)
            
    # Une sauvegarde a déjà été effectuée, j'efface cette sauvegarde temporaire SI JE VIENS DE CREER CET EVNT (origine="")
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        if self.id is not None and self.origine=="":  
            result = anvil.server.call("del_event_bt_retour", self.id)
            if not result :
                alert("Sauvegarde temporaire non effacée !")    
        open_form(self.f)

    # Image1 en chargement
    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
            nom=self.nom_img("1")  # envoi en fonction d'initialisation du nom de l'image 1
            file_rezized = anvil.server.call('resize_img', file, nom)   # 800x600 ou 600x800
            self.image_1.source = file_rezized
            self.file_loader_1.text = "1 img chargée"
            self.button_validation.visible = True
            
            self.flow_panel_loader_1.visible = False
            self.outlined_card_1.visible = True
            self.button_rotation_1.visible = True
            self.button_del_1.visible = True
            self.button_visu_1.visible = True
            
    def file_loader_2_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
            nom=self.nom_img("2")  # envoi en fonction d'initialisation du nom de l'image 2
            file_rezized = anvil.server.call('resize_img', file, nom)   # 800x600 ou 600x800
            self.image_2.source = file_rezized
            self.file_loader_2.text = "1 img chargée"
            self.button_validation.visible = True

            self.flow_panel_loader_2.visible = False
            self.outlined_card_2.visible = True
            self.button_rotation_2.visible = True
            self.button_del_2.visible = True
            self.button_visu_2.visible = True

    def file_loader_3_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
            nom=self.nom_img("3")   # envoi en fonction d'initialisation du nom de l'image 3
            file_rezized = anvil.server.call('resize_img', file, nom)   # 800x600 ou 600x800
            self.image_3.source = file_rezized
            self.file_loader_3.text = "1 img chargée"
            self.button_validation.visible = True

            self.flow_panel_loader_3.visible = False
            self.outlined_card_3.visible = True
            self.button_rotation_3.visible = True
            self.button_del_3.visible = True
            self.button_visu_3.visible = True

    # POur afficher OK et Retour en FRancais (calendrier) 
    # Cette méthode se lance qd le date_picker component s'affiche 
    def date_picker_1_show(self, **event_args):
        # Change les bt 'apply' en 'Valider'
        from anvil.js.window import document
        for btn in document.querySelectorAll('.daterangepicker .applyBtn'):
            btn.textContent = 'Ok'
        for btn in document.querySelectorAll('.daterangepicker .cancelBtn'):
            btn.textContent = 'Retour' 

    # Pour empêcher le msg session expired (suffit pour ordinateur, pas pour tel) 
    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        with anvil.server.no_loading_indicator:
            result = anvil.server.call("ping")
        print(f"ping on server to prevent 'session expired' every 5 min, server answer:{result}")

    # Pour lancer une sauvegarde automatique toutes les 30 secondes
    def timer_2_tick(self, **event_args):
        """This method is called Every 30 seconds. Does not trigger if [interval] is 0."""
        # Toutes les 30 secondes, sauvegarde auto, self.id contient l'id du row qui est en cours de saisie
        with anvil.server.no_loading_indicator:
            self.button_validation_click(True,self.id)  # auto sov: TRUE
        
    # Initialisation du préfixe du nom du fichier img 
    def nom_img(self,num_img_txt):
        nom_img = self.date_sov+"_"+self.drop_down_event.selected_value+"_"+num_img_txt
        return nom_img

    def button_visu_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Pre_Visu_img import Pre_Visu_img
        open_form("Pre_Visu_img", self.image_1.source)

    def button_rotation_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        file=self.image_1.source
        self.image_1.source = anvil.image.rotate(file,90)
        self.button_validation.visible = True

    def button_del_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.image_1.source = None
        self.button_validation.visible = True
        self.outlined_card_1.visible = False
        self.flow_panel_loader_1.visible = True
        self.file_loader_1.text = "Photo1"

    def button_visu_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Pre_Visu_img import Pre_Visu_img
        open_form("Pre_Visu_img", self.image_2.source)

    def button_rotation_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        file=self.image_2.source
        self.image_2.source = anvil.image.rotate(file,90)
        self.button_validation.visible = True

    def button_del_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.image_2.source = None
        self.button_validation.visible = True
        self.outlined_card_2.visible = False
        self.flow_panel_loader_2.visible = True
        self.file_loader_2.text = "Photo2"

    def button_visu_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Pre_Visu_img import Pre_Visu_img
        open_form("Pre_Visu_img", self.image_3.source)

    def button_rotation_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        file=self.image_3.source
        self.image_3.source = anvil.image.rotate(file,90)
        self.button_validation.visible = True

    def button_del_3_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.image_3.source = None
        self.button_validation.visible = True
        self.outlined_card_3.visible = False
        self.flow_panel_loader_3.visible = True
        self.file_loader_3.text = "Photo3"


        

    
        
        

        
