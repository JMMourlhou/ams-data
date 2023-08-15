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
def add_stage(type,
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
    # lecture fichier père lieux
    lieu_stage = app_tables.lieux.get(lieu=lieu)    
                 
    new_row=app_tables.stages.add_row(
                              type = code_stage,
                              numero = numero,
                              lieu = lieu_stage,
                              date_debut = date_debut,
                              nb_stagiaires_deb = nb_stagiaires_deb,
                              date_fin = date_fin,
                              nb_stagiaires_fin = nb_stagiaires_fin,
                              nb_stagiaires_diplomes = nb_stagiaires_diplomes,
                              commentaires = commentaires
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