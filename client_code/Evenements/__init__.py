from ._anvil_designer import EvenementsTemplate
from anvil import *
import anvil.server

import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import French_zone   #pour afficher la date du jour
from datetime import datetime

# Saisie d'un évenement ou d'un incident 
#   Pb rencontré: session expired si la saisie est intérrompue 
    # 2 Solutions implémentées:  - Un 'ping' sur le serveur toutes les 5 minutes (300" timer 1) empêche la session d'expirée (sur un ordinateur) 
    #                                mais pas sur un tel qd l'écran s'étteint.  
    #                            - Une sauvegarde auto toutes les 30 secondes (timer 2), ce qui permet de ne pas perdre bp de données si expired. 

class Evenements(EvenementsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.id = None

        # Change les bt 'apply' en 'Valider' si je veux saisir l'heure en même tps que la date (picktime set à True)
        from anvil.js.window import document
        for btn in document.querySelectorAll('.daterangepicker .applyBtn'):
            btn.textContent = 'Ok'
        for btn in document.querySelectorAll('.daterangepicker .cancelBtn'):
            btn.textContent = 'Retour' 
        
        # Init drop down event
        self.drop_down_event.selected_value = self.drop_down_event.items[0]  # "Réunion"
        self.note_for_meeting("meeting")
        
        # Init drop down date avec Date du jour et acquisition de l'heure
        self.now = French_zone.french_zone_time()   # now est le jour/h actuelle (datetime object)
        self.date_picker_1.placeholder = self.date_fr(self.now) # fonction date_fr change Sun en Dim ds le place holder
     
        
        # Drop down codes lieux
        self.drop_down_lieux.items = [(r['lieu'], r) for r in app_tables.lieux.search(tables.order_by("lieu", ascending=True))]
        for lieu in self.drop_down_lieux.items:
            print(lieu, lieu[0], lieu[1])
        liste=self.drop_down_lieux.items[0]
        self.drop_down_lieux.selected_value = liste[1]

    def date_picker_1_change(self, **event_args):
        """This method is called when an item is selected"""  
        now = self.date_picker_1.date
        self.date_picker_1.date = None
        #self.date_picker_1.visible=False  # Efface le component date pour pouvoir afficher le place holder
        self.date_picker_1.placeholder = self.date_fr(now)
        self.date_picker_1.visible=True
        self.text_area_notes.scroll_into_view()

    def date_fr(self, date_en):
        jours_semaine = { "Mon": "Lun", "Tue": "Mar", "Wed": "Mer", "Thu": "Jeu", "Fri": "Ven", "Sat": "Sam", "Sun": "Dim" }
        date_format_en = date_en.strftime("%a, %d/%m/%Y")

        # Convertir les abréviations du jour anglaises en françaises
        jour_en = date_en.strftime("%a")
        jour_fr = jours_semaine[jour_en]
        date_format_fr = date_format_en.replace(jour_en, jour_fr)
        return date_format_fr    
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form("Main", 99)

    def drop_down_event_change(self, **event_args):
        """This method is called when an item is selected"""
        self.type = self.drop_down_event.selected_value
        if self.type == "Réunion":
            self.note_for_meeting("meeting")
        if self.type == "Incident":
            self.note_for_meeting("incident")

    def drop_down_lieux_change(self, **event_args):
        """This method is called when an item is selected"""
        pass

    def note_for_meeting(self, type):
        now = French_zone.french_zone_time()   # now est le jour/h actuelle (datetime object)
        heure = now.time()
        heure = heure.strftime("%H:%M")
        date0 = now.date()
        date = date0.strftime("%d/%m/%Y")
        self.date_sov = date0.strftime("%Y/%m/%d")
        if type == "meeting":
            self.text_area_notes.text = (f"Participants: A.C / A.JC / G.J / M.JM / L.C \nObjet: Réunion d'équipe du {date} à {heure}\n\nNotes:\n ")
        if type == "incident":
            self.text_area_notes.text = (f"Participants: A.C / A.JC / G.J / M.JM / L.C \nObjet: Incident, date/heure: .........\nPersonnes impliquées : \nNotes:\n ")

    def text_area_commentaires_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.button_validation.visible = True
        self.button_validation_1.visible = True
        self.button_validation_2.visible = True

    # validation:   auto_sov True si sovegarde auto tte les 30"   id est l'id 
    def button_validation_click(self, auto_sov=False, id=None, **event_args):
        """This method is called when the button is clicked"""
        writing_date_time = French_zone.french_zone_time()   # now est le jour/h actuelle (datetime object)
        row_lieu = self.drop_down_lieux.selected_value
        lieu_txt = row_lieu['lieu']
        result, self.id = anvil.server.call("add_event", 
                                                    self.id,                                  # row id   pour réécrire le row en auto sov tt les 30"
                                                    self.drop_down_event.selected_value,      # Type event
                                                    self.date_sov,                            # date
                                                    row_lieu,                                 # lieu row
                                                    lieu_txt,                                 # lieu en clair
                                                    self.text_area_notes.text,                # notes    
                                                    self.image_1.source,                      # image 1
                                                    self.image_2.source,
                                                    self.image_3.source,
                                                    writing_date_time,                        # Date et heure de l'enregistrement
                                     )       
        if not result :
            alert("Evenement non sauvegardé !")
        # si la sauvegarde a été effectué en fin de saisie de l'évenemnt (clique sur Bt 'Valider')
        if auto_sov is False: 
            self.button_annuler_click()

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
            file_rezized = anvil.server.call('resize_img', file, "img1")   # 800x600 ou 600x800
            self.image_1.source = file_rezized
            self.button_validation.visible = True

    def file_loader_2_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
            file_rezized = anvil.server.call('resize_img', file, "img2")   # 800x600 ou 600x800
            self.image_2.source = file_rezized
            self.button_validation.visible = True

    def file_loader_3_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
            file_rezized = anvil.server.call('resize_img', file, "img3")   # 800x600 ou 600x800
            self.image_3.source = file_rezized
            self.button_validation.visible = True

    def date_picker_1_hide(self, **event_args):
        """This method is called when the DatePicker is removed from the screen"""
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
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        # Toutes les 30 secondes, sauvegarde auto
        with anvil.server.no_loading_indicator:
            self.button_validation_click("True",self.id)
        

  

    
        
        

        