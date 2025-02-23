from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *  #pour les alertes


# ==========================================================================================
#Création d'un nouveau code
@anvil.server.callable 
def add_text_formulaire(code, text, obligation):
    new_row=app_tables.texte_formulaires.add_row(
                              code=code,
                              text=text,
                              obligation=obligation
                             )
                 
    row = app_tables.texte_formulaires.search(code=new_row['code'])
    if len(row)>0:
        valid=True
    else:
        valid=False
    return valid

# ==========================================================================================
@anvil.server.callable           #Del d'un code texte
def del_text_formulaire(code_row):
    valid = False
    code_row.delete()
    valid = True
    
    return valid

# ==========================================================================================
@anvil.server.callable           #modif d'un lieu et adresse 
def modif_text_formulaire(code_row, code, text, obligation):
    valid = False
    code_row.update(
                    code=code,
                    text=text,
                    obligation=obligation
                    )
    valid = True
    return valid
