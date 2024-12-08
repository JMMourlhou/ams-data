from ._anvil_designer import EvenementsTemplate
from anvil import *
import anvil.server

#import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import French_zone   #pour afficher la date du jour
from datetime import datetime
from datetime import timedelta

class Evenements(EvenementsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        
        # Init drop down event
        self.drop_down_event.selected_value = self.drop_down_event.items[0]  # "Réunion"
        self.note_for_meeting("meeting")
        
        # Init drop down date avec Date du jour et acquisition de l'heure
        now=French_zone.french_zone_time()   # now est le jour/h actuelle (datetime object)
        self.date_picker_1.placeholder = self.date_fr(now)
        
        # Drop down codes lieux
        self.drop_down_lieux.items = [(r['lieu'], r) for r in app_tables.lieux.search(tables.order_by("lieu", ascending=True))]
        for lieu in self.drop_down_lieux.items:
            print(lieu, lieu[0], lieu[1])
        liste=self.drop_down_lieux.items[0]
        self.drop_down_lieux.selected_value = liste[1]
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form("Main", 99)

    def date_picker_1_change(self, **event_args):
        """This method is called when an item is selected"""
        date = self.date_picker_1.date
        self.date_picker_1.placeholder = self.date_fr(date)

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
        if type == "meeting":
            self.text_area_notes.text = "Participants: A.C / A.JC / G.J / M.JM / L.C \nObjet: Réunion d'équipe \n\nNotes:\n "
        if type == "incident":
            self.text_area_notes.text = "Participants: A.C / A.JC / G.J / M.JM / L.C \nObjet: Incident \nPersonnes impliquées : \nNotes:\n "

    def text_area_commentaires_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.button_validation.visible = True

    def button_validation_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        thumb_pic = anvil.image.generate_thumbnail(file, 640)
        self.image_1.source = thumb_pic
        self.button_validation.visible = True

    def file_loader_2_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        thumb_pic = anvil.image.generate_thumbnail(file, 640)
        self.image_2.source = thumb_pic
        self.button_validation.visible = True

    def file_loader_3_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        thumb_pic = anvil.image.generate_thumbnail(file, 640)
        self.image_3.source = thumb_pic
        self.button_validation.visible = True

    def date_fr(self, date_en):
        jours_semaine = { "Mon": "Lun", "Tue": "Mar", "Wed": "Mer", "Thu": "Jeu", "Fri": "Ven", "Sat": "Sam", "Sun": "Dim" }
        date_format_en = date_en.strftime("%a, %d/%m/%Y, %H:%M")

        # Convertir les abréviations anglaises en françaises
        jour_en = date_en.strftime("%a")
        jour_fr = jours_semaine[jour_en]
        date_format_fr = date_format_en.replace(jour_en, jour_fr)
        #alert(date_format_fr)
        return date_format_fr

    
        
        

        