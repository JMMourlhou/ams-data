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
                
    new_row=app_tables.people.add_row(type = type,
                              numero = numero,
                              date_debut = date_debut,
                              nb_stagiaires_deb = nb_stagiaires_deb,
                              date_fin = date_fin,
                              nb_stagiaires_fin = nb_stagiaires_fin,
                              nb_stagiaires_diplomes = nb_stagiaires_diplomes,
                              commentaires = commentaires
                             )
    print("Création du stage", new_row['type'])
    
    stage = app_tables.stages.get(numero=new_row[numero])
    if stage:
        valid=True
    else:
        valid=False
    return