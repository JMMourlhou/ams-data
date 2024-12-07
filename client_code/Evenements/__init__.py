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
from anvil.js.window import moment

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
        self.date_picker_1.pick_time = True
        date_format_fr = now.strftime("%d/%m/%Y, %H:%M")
        self.date_picker_1.placeholder = date_format_fr
        
        
        # Drop down codes lieux
        self.drop_down_lieux.items = [(r['lieu'], r) for r in app_tables.lieux.search()]
        for lieu in self.drop_down_lieux.items:
            print(lieu, lieu[0], lieu[1])
        liste=self.drop_down_lieux.items[0]
        self.drop_down_lieux.selected_value = liste[1]
        
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form("Main", 99)

    def drop_down_date_change(self, **event_args):
        """This method is called when an item is selected"""
        
        date = self.date_picker_1.date
        #date_format_fr = moment(date).locale('fr').strftime("%d/%m/%Y, %H:%M")
        #date_format_fr = moment(date).locale('fr').format('ddd, D MMM YYYY, HH:mm')
        self.date_picker_1.placeholder = date.strftime("%d/%m/%Y, %H:%M")

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
        
        

        