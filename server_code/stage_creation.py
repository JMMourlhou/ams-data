import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from anvil import *  #pour les alertes

#Création d'un nouveau stage
@anvil.server.callable 
def add_stage(code_stage,     # row codes_stage concernée
              code_txt,
              numero,         # numéro de stage en clair: txt
              lieu_stage,     # row lieux concerné
              date_debut,
              nb_stagiaires_deb,
              date_fin,
              nb_stagiaires_fin,
              nb_stagiaires_diplomes,
              commentaires
             ):
    #print("lieu: ",lieu)         
    numero=int(numero)   
    new_row=app_tables.stages.add_row(
                              code = code_stage,
                              code_txt = code_stage['code'],
                              numero = numero,
                              lieu = lieu_stage,
                              date_debut = date_debut,
                              nb_stagiaires_deb = 0,
                              date_fin = date_fin,
                              nb_stagiaires_fin = 0,
                              nb_stagiaires_diplomes = 0,
                              commentaires = commentaires,
                              allow_bgt_generation = False
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