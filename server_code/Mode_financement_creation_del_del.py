from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *  #pour les alertes


# ==========================================================================================
#Création d'un nouveau lieu
@anvil.server.callable 
def add_mode_fi(code_mode_fi, intitule):
    new_row=app_tables.mode_financement.add_row(
                              mode_fi=code_mode_fi,
                              intitule_fi=intitule
                             )
                 
    row = app_tables.lieux.search(mode_fi=new_row['mode_fi'])
    if len(row)>0:
        valid=True
    else:
        valid=False
    return valid

# ==========================================================================================
@anvil.server.callable           #Del d'un lieu (si pas utilisé en table stagiaire inscrits)
def del_mode_fi(mode_fi_row, code_mode_fi, intitule):
    valid = False
    # del des PR stagiaires existants
    liste = app_tables.stages.search(mode_fi=code_mode_fi)
    if len(liste)==0:
        mode_fi_row.delete()
        valid = True
    
    return valid, len(liste), liste

# ==========================================================================================
@anvil.server.callable           #modif d'un lieu et adresse 
def modif_mode_fi(lieu_row, adresse, lieu, old_lieu):
    valid = False
    lieu_row.update(adresse = adresse,
                   lieu=lieu)
    valid = True
            
    return valid
