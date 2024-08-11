import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *  #pour les alertes

#Création d'un nouveau Pré-Requis
@anvil.server.callable 
def add_pr(code_stage,     # row codes_pr concernée
              
             ):
    
    new_row=app_tables.stages.add_row(
                              
                             )
        
                 
    stage = app_tables.stages.search(numero=new_row['numero'])
    if len(stage)>0:
        valid=True
    else:
        valid=False
    return valid


# ==========================================================================================
@anvil.server.callable           #modif d'un pr
def modif_pr(pr_row, intitule):
    pr_row.update(requis = intitule)
    valid=True
    return valid