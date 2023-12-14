import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *  #pour les alertes

def doc_name_creation(stage_num, item_requis, row_user):
    
    # lecture du stagiaire
    row=app_tables.users.get(email=row_user['email'])
    if not row:
        print("Pre_R_doc_name : user non trouvé à partir de son mail") 
    len_name = len(row['nom'])       #  premiers caractères du Nom  ???
    name = row['nom'][0:len_name]        # pour l'instant tous les caractères du Nom    
    name = name.replace(" ","-")        #!!! si espaces ds nom 
    prenom = row['prenom'][0:1]   # 1 caract prénom
    
    # Acquisition du num de stage
    stg = str(stage_num['numero'])     # Num de stge

    # Acquisition de l'item requis
    item = item_requis['code_pre_requis']
    
    file_name= stg + "_"+ item +"_"+ name.capitalize() + "-"+ prenom.capitalize()    # l'extension sera ajoutée ds les autres modules

    return file_name
