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
@anvil.server.callable           #modif d'un intitulé pr et répercution ds la table pr_stgiaires ET Table Codes_stages, si le dictionnaire des pr pour un stage contient ce code
def modif_pr(pr_row, intitule, code, old_code):
    pr_row.update(requis = intitule,
                 code_pre_requis=code)
    
    # modif du PR existant en table "pre_requis_stagiaire"
    liste = app_tables.pre_requis_stagiaire.search(item_requis=pr_row)
    if len(liste)>0:
        for pr_r in liste:
            pr_r.update(requis_txt = intitule)
            
    # modif des PR existants en table Codes_stages
    liste = app_tables.codes_stages.search()   # lecture de chaque stage
    for stage in liste:
        # lecture du dico
        dico = {}
        dico = stage['pre_requis']
        # recherche si clef (old_code) existante, si oui effact ancienne clef puis recréation avec la nouvelle
        test = dico.get(old_code)
        print("test: ", test)
        if test is not None: # Clé existante 1 on l'efface, 2 on recrée 
            del dico[old_code]
            # création du nx pr ds dico pr pour ce stage
            clef = code
            print("new key: ", clef)
            dico[clef]= {                        # AJOUT DE LA nouvelle CLEF DS LE DICO PR table codes stages
                            "Doc": intitule,
                            "Validé": False,
                            "Commentaires": "",
                            "Nom_document": ""
                        }
    valid=True
    return valid, len(liste)

# ==========================================================================================
@anvil.server.callable           #Del d'un pr et répercution ds la table pr_stgiaires ET table code_stages
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
        liste1 = app_tables.pre_requis_stagiaire.search(item_requis=pr_row)
        if len(liste1)==0:
            valid = True
    return valid, len(liste)
