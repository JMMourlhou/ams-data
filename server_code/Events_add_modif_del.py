import anvil.email
import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *  #pour les alertes


# =========================================================================================
# appelé par form Evenements 
# Création d'un nouvel Evenement (Réunion ou Incident), sauvegarde auto tt les 30 secondes...
#   ... pour éviter de perdre les données en cas de session expired (sur tel possible)

@anvil.server.callable 
# Auto_sov = True: sauvegarde auto, doit modifier le row, si un id existe déjà
# id du row = not None si sauvegarde auto, contient le id_row à modifier (sauf si c'est la 1ere sauvegarde)
def add_event(id, type_event, date_time, lieu_row, lieu_txt, note, img_1, img_2, img_3, writing_date_time, mot_clef):
    #    si id = None, indique que c'est une premiere sauvegarde, j'utilise .add_row
    if id is None:
        new_row=app_tables.events.add_row(  
                                            type_event=type_event,
                                            date=date_time,
                                            lieu=lieu_row,
                                            lieu_text=lieu_txt,
                                            note=note,
                                            img1=img_1,
                                            img2=img_2,
                                            img3=img_3,
                                            writing_date_time=writing_date_time,
                                            mot_clef=mot_clef
                                        )
        id = new_row.get_id()  # en création de l'évènement, je sauve l'id pour pouvoir le modifier en sauvegrde auto ou sauvegarde finale (bt Validation)
        re_read_row = app_tables.events.get_by_id(id)
        if re_read_row:
            valid=True
        else:
            valid=False
        
    # si id = not None, indique qu'il y a déjà eu une sauvegarde: j'utilise update
    if id is not None:
        re_read_row = app_tables.events.get_by_id(id)
        if re_read_row:
            valid=True
            re_read_row.update(
                                type_event=type_event,
                                date=date_time,
                                lieu=lieu_row,
                                lieu_text=lieu_txt,
                                note=note,
                                img1=img_1,
                                img2=img_2,
                                img3=img_3,
                                writing_date_time=writing_date_time,
                                mot_clef=mot_clef
                                )
        else:
            valid=False
    return valid, id


# =========================================================================================
# appelé par form Evenements_vissu_modif_del / ItemTemplate21
# Effacement d'un Evenement (Réunion ou Incident)
# row contient le self.item à effacer, (click sur bt del)
@anvil.server.callable 
def del_event(to_be_deleted_event_row):
    result=False
    id=to_be_deleted_event_row.get_id()
    to_be_deleted_event_row.delete()

    #relecture
    test = app_tables.events.get_by_id(id)
    if not test:
        result=True
    return result
    