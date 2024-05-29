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
                              allow_bgt_generation = False,
                              saisie_satisf_ok = False,                                 # Ne pas saisir le form de stisfaction            
                              satis_dico1_q_ferm=code_stage["satisf_q_ferm_template"],  # copie du template de la table "code_stages", questions fermées
                              satis_dico2_q_ouv=code_stage["satisf_q_ouv_template"]     # copie du template de la table "code_stages", questions ouvertes
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


# ==========================================================================================
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
              allow_bgt_generation,    # True/False
              allow_form_satisf        # True/False   
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
                    allow_bgt_generation = allow_bgt_generation,
                    saisie_satisf_ok=allow_form_satisf
                    )
        valid=True
    return valid


# ==========================================================================================
#Effact d'un stage existant (si pas de stagiaires), le test a été effectué en client side
@anvil.server.callable 
def del_stage(stage_num):   # stage_num: num de stage en txt
    result = False
    #lecture du row du stage:
    stage_row = app_tables.stages.get(numero=stage_num)
    if stage_row:
        stage_row.delete()
        result = True
       
        #décrément du compteur de stages si c'est le dernier stage créé
        cpt_num_stage_row = app_tables.cpt_stages.search()[0]
        if stage_num ==  cpt_num_stage_row['compteur']:
            cpt=int(cpt_num_stage_row['compteur'])-1 
            cpt_num_stage_row.update(compteur=cpt)
    return result