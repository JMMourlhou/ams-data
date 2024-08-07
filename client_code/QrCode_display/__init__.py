from ._anvil_designer import QrCode_displayTemplate
from anvil import *

import anvil.server

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import French_zone
from anvil import open_form 

class QrCode_display(QrCode_displayTemplate):
    def __init__(self, log_in=False, num_stage=0, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens
        # si log_in = False, appel du qr_code pour que les stagiaires s'inscrivent au stage
        if log_in is False:
            # lecture du stage par son numéro si pas de log_in normal
            stage = app_tables.stages.get(numero=int(num_stage)) 
            if not stage:
                alert("Code du stage non trouvé")
                return
            txt_stage=stage['code']['code']
            txt_stage=txt_stage.replace("_","")
            self.label_titre.text = "Flachez pour s'inscrire au "+ txt_stage + " du " + str(stage['date_debut'].strftime("%d/%m/%Y"))
            if num_stage==0 :
                alert("Numéro de stage non valide")
                return
            else:
                time = self.recup_time()
                param="/#?a=qrcode" + "&stage=" + str(num_stage) + "&t=" + time
        else:
            # si log_in =True, appel du qr_code pour que les stagiaires log in ds l'appli, donc pas de num stage
            param = ""
            self.label_titre.text = "Flachez pour vous connecter à l'appli AMSdata "

        # Lecture de la variable globale "code_app1" ds table variables_globales
        app = anvil.server.call('get_variable_value', "code_app1")
        stage_link = app + param  # App "AMS Data"  + code stage
        self.text_area_lien.text = stage_link
        print(stage_link)
        self.text_area_lien.display = True
        media=anvil.server.call('mk_qr_code',stage_link)
        self.image_1.source=media

    def recup_time(self, **event_args): 
        time=French_zone.french_zone_time()
        time_str=""
        time_str=str(time)
        time_str=time_str.replace(" ","_")
        return(time_str)

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

        


