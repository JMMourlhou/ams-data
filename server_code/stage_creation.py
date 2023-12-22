import anvil.stripe
import anvil.files
from anvil.files import data_files
import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *  #pour les alertes

@anvil.server.callable           #Création d'un nouveau stage
def add_stage(code,
              numero,   # attention numero est txt
              lieu,
              date_debut,
              nb_stagiaires_deb,
              date_fin,
              nb_stagiaires_fin,
              nb_stagiaires_diplomes,
              commentaires
             ):
    print("lieu: ",lieu)         
    numero=int(numero)

    # lecture fichier père code stages
    code_stage = app_tables.codes_stages.get(code=code)
    if not code_stage :
        alert("Code stage non trouvé ds fichier param Code_stages")
        valid=False
        return valid
    # lecture fichier père lieux
    lieu_stage = app_tables.lieux.get(lieu=lieu)    
    if not lieu_stage :
        alert("Lieu stage non trouvé ds fichier param lieux")
        valid=False
        return valid   
        
    new_row=app_tables.stages.add_row(
                              code = code_stage,
                              numero = numero,
                              lieu = lieu_stage,
                              date_debut = date_debut,
                              nb_stagiaires_deb = 0,
                              date_fin = date_fin,
                              nb_stagiaires_fin = 0,
                              nb_stagiaires_diplomes = 0,
                              commentaires = commentaires,
                              allow_bgt_generation = True
                             )
        
                 
    stage = app_tables.stages.search(numero=new_row['numero'])
    if len(stage)>0:
        valid=True
        #incrément du compteur de stages
        num = app_tables.cpt_stages.search()[0]
        cpt=int(num['compteur'])+1 
        num.update(compteur=cpt)
    else:
        valid=False
    return valid