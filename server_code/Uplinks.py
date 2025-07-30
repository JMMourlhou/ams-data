import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import base64

"""
UPLINKS pour mise à jour des FICHIERS MEDIA ds tables du Pi5 distant
        à partir de la base AMSDATA sur platforme Anvil
Ces modules sont appelés par un script Python 'run_uplink_media' ds le ct Docker, voir:  
        /mnt/ssd-prog/home/jmm/AMS_data/cmd-2-service-ct-uplink-amsdata.sh
"""

@anvil.server.callable
def get_media_data_from_table_users(user_email):      # email doit être une donnée taxte ou num, pas de row en uplink
    row = app_tables.users.get(email=user_email)
    if row and row['photo']:
        media = row['photo']
        return {
            "id": row.get_id(),
            "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
            "name": media.name,
            "content_type": media.content_type
        }
    return None
    
# 1 image à extraire / Table qcm
@anvil.server.callable
def get_media_data_from_table_qcm(qcm_nb, num):            #qcm_nb, num doivent être texte
    print("Module dans AMSDATA IDE : Lecture row ok")
    qcm_link = app_tables.qcm_description.get(qcm_nb=qcm_nb)
    row = app_tables.qcm.get(qcm_nb=qcm_link,num=num)
    if row and row['photo']:
        print("Module dans AMSDATA IDE : Lecture row ok")
        media = row['photo']
        return {
            "id": row.get_id(),
            "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
            "name": media.name,
            "content_type": media.content_type
        }
    print("retour à None")    
    return None
    
# 2 images à extraire / Table pre_requis_stagiaire
@anvil.server.callable
def get_media_data_from_table_pre_requis(stage_num, email, requis):     # stage_num, email, requis num doivent être des données taxte ou num, pas de row en uplink
    stage_link = app_tables.stages.get(numero=stage_num)
    stagiaire_link = app_tables.users.get(email=email)
    requis_link = app_tables.pre_requis.get(code_pre_requis=requis)
    
    # Initialisations par défaut
    media_doc1 = media_thumb = None
    
    row = app_tables.pre_requis_stagiaire.get(stage_num=stage_link, stagiaire_email=stagiaire_link, item_requis=requis_link)
    if row and row['doc1'] is not None:
        media = row['doc1']
        media_doc1 = {
            "id": row.get_id(),
            "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
            "name": media.name,
            "content_type": media.content_type
        }

        media = row['thumb']
        media_thumb = {
            "id": row.get_id(),
            "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
            "name": media.name,
            "content_type": media.content_type
        }
        return media_doc1, media_thumb 
    return None, None

# 3 images à extraire / Table events
@anvil.server.callable
def get_media_data_from_table_events(date, name):     # date doit être une donnée taxte ou num, pas de row en uplink
    row = app_tables.events.get(date=date, mot_clef=name)
    
    # Initialisations par défaut
    media_img1 = media_img2 = media_img3 = None
    
    if row and row['img1'] is not None:
        media = row['img1']
        media_img1 = {
            "id": row.get_id(),
            "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
            "name": media.name,
            "content_type": media.content_type
        }
        
        if row['img2'] is not None:
            media = row['img2']
            media_img2 = {
                "id": row.get_id(),
                "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
                "name": media.name,
                "content_type": media.content_type
            }
            
        if row['img3'] is not None:
            media = row['img3']
            media_img3 = {
                "id": row.get_id(),
                "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
                "name": media.name,
                "content_type": media.content_type
            }
        return media_img1, media_img2, media_img3 
    return None, None, None


# var 'position' permet une lecture séqentielle du début à la fin de la table files
# et de relire le bon row ici, sur base distante amsdata sur l'IDE Anvil
@anvil.server.callable
def get_media_data_from_table_files(position):      # position est une donnée num, pas de row en uplink
    row = app_tables.files.search()[position]   # 0 = 1ere position, position du row dans la table, 
    if row and row['file']:
        media = row['file']
        return {
            "id": row.get_id(),
            "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
            "name": media.name,
            "content_type": media.content_type
        }
    return None

    # 5 medias pdf à extraire / Table stages
@anvil.server.callable
def get_media_data_from_table_stages(numero:int) -> tuple:     # numero doit être une donnée taxte ou num, pas de row en uplink
    # tuple renvoyé par la fonction: list_media, trombi_media, diplomes, satis_pdf, suivi_pdf
    row = app_tables.stages.get(numero=numero)

    # Initialisations par défaut
    list_media = trombi_media = diplomes = satis_pdf = suivi_pdf =None

    if row:
        if row['list_media'] is not None:
            media = row['list_media']
            list_media = {
                "id": row.get_id(),
                "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
                "name": media.name,
                "content_type": media.content_type
            }
        else:
            list_media = None
            
        if row['trombi_media'] is not None:
            media = row['trombi_media']
            trombi_media = {
                "id": row.get_id(),
                "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
                "name": media.name,
                "content_type": media.content_type
            }
        else:
            trombi_media = None

        if row['diplomes'] is not None:
            media = row['diplomes']
            diplomes = {
                "id": row.get_id(),
                "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
                "name": media.name,
                "content_type": media.content_type
            }
        else:
            diplomes = None

        if row['satis_pdf'] is not None:
            media = row['satis_pdf']
            satis_pdf = {
                "id": row.get_id(),
                "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
                "name": media.name,
                "content_type": media.content_type
            }
        else:
            satis_pdf = None

        if row['suivi_pdf'] is not None:
            media = row['suivi_pdf']
            suivi_pdf = {
                "id": row.get_id(),
                "bytes": base64.b64encode(media.get_bytes()).decode('utf-8'),  # ✅ encodé en texte
                "name": media.name,
                "content_type": media.content_type
            }
        else:
            suivi_pdf = None
        
    return list_media, trombi_media, diplomes, satis_pdf, suivi_pdf 
        
    