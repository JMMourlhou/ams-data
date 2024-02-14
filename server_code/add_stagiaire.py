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

"""
ADD & EFFACEMENT d'1 stagiaire du stage
"""


@anvil.server.callable           # ADD d'un nouveau stagiaire ds le stage
@anvil.tables.in_transaction
def add_stagiaire(stagiaire_row, stage, mode_fi, type_add=""):
    valid=""
    # lecture fichier père stages
    code_stage = app_tables.stages.get(numero=int(stage))
    if not code_stage :
        valid="Stage non trouvé ds fichier stages !"
        return valid
  
    # lecture fichier père user (lecture différente si vient de création 1ere entrée ou bt_modif en recherche)
    if type_add == "":               # 1ere entrée par flash Qr_code: le user est le stagiaire
        user = anvil.users.get_user()
    if type_add == "bt_recherche":   # le stagiaire a été choisit ds recherche (Recherche_stagiaire / RowTemplate1)
        user = app_tables.users.get(email=stagiaire_row['email'])
    if user:
        if user != stagiaire_row :
            valid="Stagiaire non trouvé ds fichier users !"
            return valid
    else:
        valid="User non trouvé ds fichier users !"
        return valid

    # lecture fichier père mode financemnt
    mode_fin = app_tables.mode_financement.get(code_fi=mode_fi)    
    if not mode_fin :
        valid="Mode de financemnt non trouvé ds fichier param mode financemnt !"
        return valid

    #vérification si user pas déjà inscrit ds fichier stagiaire inscrit, POUR CE STAGE:
    
    test = app_tables.stagiaires_inscrits.search(user_email=user,                 # ce user
                                                 stage=code_stage)                # ET pour ce stage
    if len(test)>0:
        valid="Stagiaire déjà inscrit à ce stage !"
        # ******************************************************************* EFFACT code stage ds user avant retour
        user.update(temp = 0)
        return valid 

    """ Ajout des droits QCM pour ce stagiaire """
    if code_stage:
        type_stage = code_stage['code']
        type_stage_row = app_tables.codes_stages.get(code=type_stage['code'])
        if type_stage_row:
            if type_stage_row['droit_qcm'] != None:
                dico_droits_qcm = type_stage_row['droit_qcm']
            else:
                dico_droits_qcm = {}
    
    new_row=app_tables.stagiaires_inscrits.add_row(
                              stage = code_stage,  
                              user_email = user,
                              name = user['nom'].lower(),    # nom pour permettre le tri sur le nom
                              financement = mode_fin,
                              droits_stagiaire_qcms = dico_droits_qcm
                              )
             
    stagiaire_row = app_tables.stagiaires_inscrits.search(stage=new_row['stage'])
    if stagiaire_row:
        # ******************************************************************* EFFACT code stage ds user et INCREMENT du nb de stgiaires ds le stage:
        # ajouter le dico de l'historique du stagiare (ex; {"PSC1 du 28/08/202":(101,True)} )
        historique = {}
        valeur = []     
        #print(type(user['histo']))
        historique = user["histo"]
        st = code_stage["code"]["code"]
        st=st.strip()
        #print(st)
        clef = st + " du "+str(code_stage["date_debut"])
        valeur = [code_stage["numero"],None]  # None sera remplacé par True si diplomé
        historique[clef] = valeur              # ajout de la nouvelle clef ds l'historique
        user.update(temp = 0,
                   histo=historique
                   )
        
        # INCREMENT nb de stagiaires début stage ds fichier père stage
        try:  # si nb à None il y aurait une erreur
            if code_stage:
                nb = int(code_stage['nb_stagiaires_deb'])+1
                code_stage.update(nb_stagiaires_deb=nb)
                #print("passage ds try ok")
            else:
                valid="erreur: code_stage vide"
        except:        # nb à None,  
            nb=1
            code_stage.update(nb_stagiaires_deb=nb)
            #print("passage ds except ok")
            
        valid="Stagiaire inscrit ! (" + str(nb) + ")"
    else:
        valid="Stagiaire non retrouvé dans fichier stagiaires inscrits"

    """  +++++++++++++++++++++++++   Création des pré requis pour ce stagiaire """
    # lecture du fichier stages pour lecture du dictionnaire de ses pré-requis
    if code_stage:
        type_stage = code_stage['code']
        type_stage_row = app_tables.codes_stages.get(code=type_stage['code'])
    if type_stage_row:
        dico_pre_requis = type_stage_row['pre_requis']
        if dico_pre_requis != None:   # il y a des clefs pre-requis
            
            #tri du dictionaire pre requis sur les clefs 
            liste_des_clefs = dico_pre_requis.keys()   #création de la liste des clefs du dictionaires prérequis
            liste_triée_des_clefs = sorted(liste_des_clefs)  # création de la liste triée des clefs du dictionaires prérequis
            dico_pre_requis_trié = {}
            for key in liste_triée_des_clefs:
                 dico_pre_requis_trié[key] = dico_pre_requis[key]
            
            for clef,value in dico_pre_requis_trié.items():
                print("clef: ",clef)
                pr_row = app_tables.pre_requis.get(code_pre_requis=clef)
                new_row_pr = app_tables.pre_requis_stagiaire.add_row(
                              stage_num = code_stage,  
                              stagiaire_email = user,
                              item_requis = pr_row,
                              check=False
                )    
    return valid


# =========================================================================================================================================
@anvil.server.callable           #DEL d'1 stagiaire du stage
@anvil.tables.in_transaction
def del_stagiaire(stagiaire_row, stage_row):     # stagiaire_row = table users row      stage_row = table stages row
    valid=""
    # DECREMENTATION nb de stagiaires ds ce stage
    # lecture fichier père stages
    stage_r = app_tables.stages.get(numero=int(stage_row['numero']))
    if not stage_r :
        valid="Stage non trouvé ds table stages !"
        return valid
    else:
        nb = int(stage_r['nb_stagiaires_deb'])-1
        stage_r.update(nb_stagiaires_deb=nb)

    #effacement des pré-requis du stagiaire
    #lecture des rows à effacer ds pre requis
    liste_pr = app_tables.pre_requis_stagiaire.search(stagiaire_email=stagiaire_row,
                                                   stage_num=stage_row
                                                  )
    if len(liste_pr) > 0:
        for pr in liste_pr:
            pr.delete()
            
    
    # Lecture table stagiaires inscrits à ce stage pour lecture et MAJ clef histo et effacement du stagiaire
    row = app_tables.stagiaires_inscrits.get(user_email=stagiaire_row,       # ce user
                                                 stage=stage_row)            # ET pour ce stage
    if not row :
        valid="Stagiaire à enlever du stage non trouvé ds table stagiaires inscrits !"
        return valid
        
    # Pour MAJ HISTO, table users
    user = app_tables.users.get(email=stagiaire_row['email'])    
    if not user :
        valid="MAJ histo: user à mettre à jour non trouvé ds table users !"
        return valid
    else:
        historique = {}
        valeur = []     
        historique = user["histo"]   
        st = stage_r["code"]["code"]
        st=st.strip()
        clef = st + " du "+str(stage_r["date_debut"])
        print("clef",clef)
        try:                          # erreur si histo vide
            del historique[clef]
            user.update(histo=historique)
        except:
            print("clé historique non trouvée")
        
   
    # Del of stagiaire in the stage
    row.delete()
    valid="Stagiaire effacé de ce stage !"
   
    return valid