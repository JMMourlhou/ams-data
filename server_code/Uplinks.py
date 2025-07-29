import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.server
import base64

@anvil.server.callable
def get_media_data_from_table_users(user_email):
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

@anvil.server.callable
def get_media_data_from_table_qcm(qcm_link, num):
    print("Module dans AMSDATA IDE : Lecture row ok")
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
