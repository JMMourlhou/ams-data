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
@anvil.server.callable           #modif d'un intitulé pr et répercution ds la table pr_stgiaires 
def modif_pr(pr_row, intitule):
    pr_row.update(requis = intitule)
    # modif des PR existants
    liste = app_tables.pre_requis_stagiaire.search(item_requis=pr_row)
    if len(liste)>0:
        for pr_r in liste:
            pr_r.update(requis_txt = intitule )
    valid=True
    return valid, len(liste)