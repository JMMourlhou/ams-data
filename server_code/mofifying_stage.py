import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *  #pour les alertes

@anvil.server.callable           #modif d'un stage
@anvil.tables.in_transaction
def modif_stage(type,
              numero,   # attention numero est txt
              lieu,
              date_debut,
              nb_stagiaires_deb,
              date_fin,
              nb_stagiaires_fin,
              nb_stagiaires_diplomes,
              commentaires
             ):
    numero=int(numero)

    # lecture fichier père code stages
    code_stage = app_tables.codes_stages.get(code=type)
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
                    commentaires = commentaires
                    )
        valid=True
    return valid