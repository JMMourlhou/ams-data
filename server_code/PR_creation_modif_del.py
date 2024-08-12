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
def add_pr(code, intitule, commentaires):
    
    new_row=app_tables.pre_requis.add_row(
                              code_pre_requis=code,
                              requis=intitule,
                              commentaires=commentaires,
                              doc=False
                             )
        
                 
    pr = app_tables.pre_requis.search(code_pre_requis=new_row['code_pre_requis'])
    if len(pr)>0:
        valid=True
    else:
        valid=False
    return valid


# ==========================================================================================
@anvil.server.callable           #modif d'un intitulé pr et répercution ds la table pr_stgiaires 
def modif_pr(pr_row, intitule, code):
    pr_row.update(requis = intitule,
                 code_pre_requis=code)
    # modif des PR existants
    liste = app_tables.pre_requis_stagiaire.search(item_requis=pr_row)
    if len(liste)>0:
        for pr_r in liste:
            pr_r.update(requis_txt = intitule)
    valid=True
    return valid, len(liste)

# ==========================================================================================
@anvil.server.callable           #Del d'un pr et répercution ds la table pr_stgiaires 
def del_pr(pr_row):
    valid = False
    pr_row.delete()
    valid = True
    
    # del des PR stagiaires existants
    liste = app_tables.pre_requis_stagiaire.search(item_requis=pr_row)
    if len(liste)>0:
        valid = False
        for pr_r in liste:
            pr_r.delete()
        # Vérification
        liste = app_tables.pre_requis_stagiaire.search(item_requis=pr_row)
        if len(liste)==0:
            valid = True
    return valid, len(liste)
