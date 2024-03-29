
import anvil.files
from anvil.files import data_files
import anvil.email

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *  #pour les alertes

@anvil.server.callable           #modif d'un stage
@anvil.tables.in_transaction
def modif_stage(code,
              numero,   # attention numero est txt
              lieu,
              date_debut,
              nb_stagiaires_deb,
              date_fin,
              nb_stagiaires_fin,
              nb_stagiaires_diplomes,
              commentaires,
              allow_bgt_generation
             ):
    numero=int(numero)

    # lecture fichier père code stages
    code_stage = app_tables.codes_stages.get(code=code)
    if not code_stage:   
        alert("Code stage non trouvé ds fichier param Code_stages")
        valid=False
        return valid             
    # lecture fichier père lieux
    lieu_stage = app_tables.lieux.get(lieu=lieu)    
    if not lieu_stage :
        alert("Lieu stage non trouvé ds fichier param lieux")
        valid=False
        return valid    

    # lecture du stage à modifier par son numéro             
    stage = app_tables.stages.get(numero=numero) 
    if not stage:
        alert("Lieu stage non trouvé ds fichier param lieux")
        valid=False
    else:   
        stage.update(lieu = lieu_stage,
                    date_debut = date_debut,
                    nb_stagiaires_deb = nb_stagiaires_deb,
                    date_fin = date_fin,
                    nb_stagiaires_fin = nb_stagiaires_fin,
                    nb_stagiaires_diplomes = nb_stagiaires_diplomes,
                    commentaires = commentaires,
                    allow_bgt_generation = allow_bgt_generation
                    )
        valid=True
    return valid