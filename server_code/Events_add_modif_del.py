import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *  #pour les alertes


# =========================================================================
#Création d'un nouveau Evenement (Réunion ou Incident)
@anvil.server.callable 
def add_event(type_event, date_time, lieu_row, lieu_txt, note, img_1, img_2, img_3):
    
    new_row=app_tables.events.add_row(  type_event=type_event,
                                        date_time=date_time,
                                        lieu=lieu_row,
                                        lieu_text=lieu_txt,
                                        note=note,
                                        img1=img_1,
                                        img2=img_2,
                                        img3=img_3
                                    )
                 
    id = new_row.get_id()
    re_read_row = app_tables.events.get_by_id(id)
    if re_read_row:
        valid=True
    else:
        valid=False
    return valid
