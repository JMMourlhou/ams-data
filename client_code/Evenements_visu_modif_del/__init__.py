from ._anvil_designer import Evenements_visu_modif_delTemplate
from anvil import *

import anvil.users
import anvil.server

import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from .. import French_zone  # pour afficher la date du jour
from datetime import datetime

# Visu, Modif, Del d'un évenement ou d'un incident
# type_evnt permet de réafficher les évenemnts après un effact d'un evnt (type_evnt != None)
class Evenements_visu_modif_del(Evenements_visu_modif_delTemplate):
    def __init__(self, type_evnt=None ,**properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.id = None
        self.data_grid_1.visible = False
        self.check_box_visu_erreurs.visible = False
        # envoi direct en traitement du drop down evenement si vient d'un effacement d'évenement
        self.type_event = type_evnt
        if self.type_event is not None:
            self.drop_down_event.selected_value = self.type_event
            self.drop_down_event_change()
            

        # Init drop down event (Pour l'instant choix à rentrer pour ne pas perdre les notes si je change le type d'evenmt)
        """
        self.drop_down_event.selected_value = self.drop_down_event.items[0]  # "Réunion"
        self.note_for_meeting("meeting")
        """

        # acquisition de l'heure
        self.now = (French_zone.french_zone_time())  # now est le jour/h actuelle (datetime object)
    

    def date_picker_1_change(self, **event_args):
        """This method is called when an item is selected"""
        now = self.date_picker_1.date
        self.date_picker_1.date = None
        # self.date_picker_1.visible=False  # Efface le component date pour pouvoir afficher le place holder
        self.date_picker_1.placeholder = self.date_fr(now)
        self.date_picker_1.visible = True
        self.text_area_notes.scroll_into_view()

    def date_fr(self, date_en):
        jours_semaine = {
            "Mon": "Lun",
            "Tue": "Mar",
            "Wed": "Mer",
            "Thu": "Jeu",
            "Fri": "Ven",
            "Sat": "Sam",
            "Sun": "Dim",
        }
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
        # Acquisition du choix d'évenements à afficher
        self.type = self.drop_down_event.selected_value
        if self.type == "Nouvel évenement":
            from ..Evenements import Evenements
            open_form("Evenements")
        # Acquisition du check box: Affiche les erreurs de sauvegardes
        visu_des_erreurs = self.check_box_visu_erreurs.checked
        
        # Création de la liste des évenemnts: NE PRENDRE QUE LES EVENEMNTS SAUVES PAR VALIDATION (sauf si chechk box visu erreurs Checked )
        #   certaines raws viennent de sauvegardes temporaires ttes les 30 sec par forme 'Evenements'
        #      ( venant de sorties incontrolées par fermetures defen^tres ou appuis sur la touche gauche du tel)
            
        if self.type == "Voir une réunion":
            type_evenement = "réunion"
        elif self.type == "Voir un incident":
            type_evenement = "incident"
        else:
            type_evenement = "autre"
            
        liste = app_tables.events.search(tables.order_by("writing_date_time", ascending=False),
                                        auto_sov=visu_des_erreurs, 
                                        type_event=type_evenement
                                        )
        self.repeating_panel_1.items=liste
        self.check_box_visu_erreurs.visible = True
        self.data_grid_1.visible = True
            
    def check_box_visu_erreurs_change(self, **event_args):
        """This method is called when this checkbox is checked or unchecked"""
        self.drop_down_event_change()     


    def note_for_meeting(self, type):
        now = (
            French_zone.french_zone_time()
        )  # now est le jour/h actuelle (datetime object)
        heure = now.time()
        heure = heure.strftime("%H:%M")
        date0 = now.date()
        date = date0.strftime("%d/%m/%Y")
        self.date_sov = date0.strftime("%Y/%m/%d")
        if type == "meeting":
            self.text_area_notes.text = f"Participants: A.C / A.JC / G.J / M.JM / L.C \nObjet: Réunion d'équipe du {date} à {heure}\n\nNotes:\n "
        if type == "incident":
            self.text_area_notes.text = f"Participants: A.C / A.JC / G.J / M.JM / L.C \nObjet: Incident, date/heure: .........\nPersonnes impliquées : \nNotes:\n "

    def text_area_commentaires_change(self, **event_args):
        """This method is called when the text in this text area is edited"""
        self.button_validation.visible = True
        # self.button_validation_1.visible = True
        self.button_validation_2.visible = True

    # validation:   auto_sov True si sovegarde auto tte les 30"   id est l'id
    def button_validation_click(self, auto_sov=False, id=None, **event_args):
        """This method is called when the button is clicked"""
        writing_date_time = (
            French_zone.french_zone_time()
        )  # now est le jour/h actuelle (datetime object)
        row_lieu = self.drop_down_lieux.selected_value
        lieu_txt = row_lieu["lieu"]
        result, self.id = anvil.server.call(
            "add_event",
            self.id,  # row id   pour réécrire le row en auto sov tt les 30"
            self.drop_down_event.selected_value,  # Type event
            self.date_sov,  # date
            row_lieu,  # lieu row
            lieu_txt,  # lieu en clair
            self.text_area_notes.text,  # notes
            self.image_1.source,  # image 1
            self.image_2.source,
            self.image_3.source,
            writing_date_time,  # Date et heure de l'enregistrement
        )
        if not result:
            alert("Evenement non sauvegardé !")
        # si la sauvegarde a été effectué en fin de saisie de l'évenemnt (clique sur Bt 'Valider')
        if auto_sov is False:
            self.button_annuler_click()

    def file_loader_1_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  # pas d'annulation en ouvrant choix de fichier
            nom = self.nom_img(
                "1"
            )  # envoi en fonction d'initialisation du nom de l'image 1
            file_rezized = anvil.server.call(
                "resize_img", file, nom
            )  # 800x600 ou 600x800
            self.image_1.source = file_rezized
            self.button_validation.visible = True

    def file_loader_2_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  # pas d'annulation en ouvrant choix de fichier
            nom = self.nom_img(
                "2"
            )  # envoi en fonction d'initialisation du nom de l'image 2
            file_rezized = anvil.server.call(
                "resize_img", file, nom
            )  # 800x600 ou 600x800
            self.image_2.source = file_rezized
            self.button_validation.visible = True

    def file_loader_3_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        if file is not None:  # pas d'annulation en ouvrant choix de fichier
            nom = self.nom_img(
                "3"
            )  # envoi en fonction d'initialisation du nom de l'image 3
            file_rezized = anvil.server.call(
                "resize_img", file, nom
            )  # 800x600 ou 600x800
            self.image_3.source = file_rezized
            self.button_validation.visible = True

    def date_picker_1_hide(self, **event_args):
        """This method is called when the DatePicker is removed from the screen"""
        # Change les bt 'apply' en 'Valider'
        from anvil.js.window import document

        for btn in document.querySelectorAll(".daterangepicker .applyBtn"):
            btn.textContent = "Ok"
        for btn in document.querySelectorAll(".daterangepicker .cancelBtn"):
            btn.textContent = "Retour"

    # Pour empêcher le msg session expired (suffit pour ordinateur, pas pour tel)
    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        with anvil.server.no_loading_indicator:
            result = anvil.server.call("ping")
        print(
            f"ping on server to prevent 'session expired' every 5 min, server answer:{result}"
        )


    # Initialisation du préfixe du nom du fichier img
    def nom_img(self, num_img_txt):
        nom_img = (
            self.date_sov
            + "_"
            + self.drop_down_event.selected_value
            + "_"
            + num_img_txt
        )
        return nom_img

    def text_box_date_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        liste = app_tables.events.search(tables.order_by("writing_date_time", ascending=False),
                                        auto_sov=visu_des_erreurs, 
                                        type_event=type_evenement
                                        )
        self.repeating_panel_1.items=liste

    def text_box_mot_clef_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        pass

    def text_box_lieu_focus(self, **event_args):
        """This method is called when the TextBox gets focus"""
        pass


