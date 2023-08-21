from ._anvil_designer import QrCode_displayTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import French_zone

class QrCode_display(QrCode_displayTemplate):
    def __init__(self, num_stage=0, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens
        if num_stage==0 :
            alert("Numéro de stage non valide")
            return
        else:
            time = self.recup_time()
            param="/#?stage=" + str(num_stage) + "&t=" + time
            code_app1 = "https://sxgqveyu3c2nj5kr.anvil.app/BBDLB54NWHHYKEE3YYGJGU4G" + param  # App "AMS Data"  + code stage
            media=anvil.server.call('mk_qr_code',code_app1)
            self.image_1.source=media

        def recup_time(): 
            time=french_zone.time_french_zone()
            time_str=""
            time_str=str(time)
            time_str=time_str.replace(" ","_")
            return(time_str)

