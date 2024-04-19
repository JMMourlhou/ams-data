import anvil.server

import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import *

#boucle sur la table users pour modif rapide d'une colonne, ici sur le role (sauf l'administrateur)
def loop_users():
    table_users = app_tables.users.search()
    result="erreur"
    if table_users:
        for row in table_users:
            if row['email'] != "jmarc@jmm-formation-et-services.fr":
                row.update(role="S")
        result="loop ok"     
    return result

#boucle sur la table stagiaires inscrits pour maj des droits aux qcm par type de stage
def loop_stagiaire_inscrits():
    # 1 loop sur fichier stagiaires inscrits
    liste_st_inscrits = app_tables.stagiaires_inscrits.search()
    for row_stagiaire in liste_st_inscrits:
        # 2 lecture fichier père stage
        stage_row = app_tables.stages.get(numero = row_stagiaire['stage']['numero'])    # acquisition du num de stage
        print(stage_row['numero'])
        # 3 lecture fichier père type_stage
        type_stage_row = app_tables.codes_stages.get(code = stage_row['code']['code'])
        print(type_stage_row['droit_qcm'])
        #  *************************************************************************** MAJ des droits de ce stagiaire aux qcm (par type de stage) 
        row_stagiaire.update(droits_stagiaire_qcms=type_stage_row['droit_qcm'])


#boucle sur la table qcm_result pour l'effacmt de tous les résultats, 
def loop_del_result():
    table = app_tables.qcm_result.search()
    print(len(table))
    result="erreur"
    if table: 
        for row in table:
            row.delete()
        result="loop ok" 
    return result

#boucle sur la table qcm_result pour l'effacmt des lignes du qcm test (3), 
def loop_del_qcm3_result():
    #lecture user
    user_jm = app_tables.users.get(email="jmmourlhou@gmail.com")
    print(user_jm['prenom'])
    #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=3)
    print(qcm_row['destination'])
    if qcm_row:
        table = app_tables.qcm_result.search(qcm_number=qcm_row,
                                             user_qcm=user_jm
                                            )
        print(len(table))
        result="erreur"
        if table: 
            for row in table:
                row.delete()
            result="loop ok" 
    return result

#boucle sur la table qcm pour modif rapide d'une colonne, ici sur la description
def loop_qcm19():
    #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=19)
    if qcm_row:
        table = app_tables.qcm.search(qcm_nb=qcm_row)
        result="erreur"
        if table:
            for row in table:
                row.update(param = "Communication")
            result="loop ok"     

#boucle sur la table qcm pour modif rapide d'une colonne, ici sur le type des qcm BNSSA (4 à 9) 
def loop_qcm4():
    #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=4)
    if qcm_row:
        table = app_tables.qcm.search(qcm_nb=qcm_row )
        result="erreur"
        txt="PSE2"
        if table:
            for row in table:
                row.update(type= "Multi"
                          )
            result="loop ok"
        print(f"loop sur qcm4: {result}")
    
    #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=5)
    if qcm_row:
        table = app_tables.qcm.search(qcm_nb=qcm_row )
        result="erreur"
        txt="PSE2"
        if table:
            for row in table:
                row.update(type= "Multi"
                          )
            result="loop ok"
        print(f"loop sur qcm5: {result}")

    #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=6)
    if qcm_row:
        table = app_tables.qcm.search(qcm_nb=qcm_row )
        result="erreur"
        txt="PSE2"
        if table:
            for row in table:
                row.update(type= "Multi"
                          )
            result="loop ok"
        print(f"loop sur qcm6: {result}")

    #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=7)
    if qcm_row:
        table = app_tables.qcm.search(qcm_nb=qcm_row )
        result="erreur"
        txt="PSE2"
        if table:
            for row in table:
                row.update(type= "Multi"
                          )
            result="loop ok"
        print(f"loop sur qcm7: {result}")

    #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=8)
    if qcm_row:
        table = app_tables.qcm.search(qcm_nb=qcm_row )
        result="erreur"
        txt="PSE2"
        if table:
            for row in table:
                row.update(type= "Multi"
                          )
            result="loop ok"
        print(f"loop sur qcm8: {result}")

     #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=9)
    if qcm_row:
        table = app_tables.qcm.search(qcm_nb=qcm_row )
        result="erreur"
        txt="PSE2"
        if table:
            for row in table:
                row.update(type= "Multi"
                          )
            result="loop ok"
        print(f"loop sur qcm9: {result}")

#boucle sur la table pré-requis par stagiaire pour ajouter un pré-requiq à tous les stgiaires d'un stage
def ajout_pre_requis():
    # lecture stage 
    stage_row=app_tables.stages.get(numero=116)
    # lecture pré-requis
    pre_requis_row=app_tables.pre_requis.get(code_pre_requis="PH-DI")
    # loop sur chaque stgiaire et ajout du pré-requis
    
    stagiaires = app_tables.stagiaires_inscrits.search(stage=stage_row)
    for stagiaire in stagiaires:
        
        app_tables.pre_requis_stagiaire.add_row(
                              stage_num = stage_row,  
                              stagiaire_email = stagiaire['user_email'],
                              item_requis = pre_requis_row,
                              check=False
                )    
        print(stagiaire['user_email'], " ", pre_requis_row['code_pre_requis'])

#boucle sur la table pré-requis par stagiaire pour enlever un pré-requiq à tous les stagiaires d'un stage
def del_pre_requis():
    # lecture stage 
    stage_row=app_tables.stages.get(numero=116)
    # lecture pré-requis
    pre_requis_row=app_tables.pre_requis.get(code_pre_requis="PH-CTF-P4")
    # loop sur table pre_requis_stagiaire et del du pré-requis
    liste_a_enlever = app_tables.pre_requis_stagiaire.search(item_requis=pre_requis_row,
                                                             stage_num=stage_row
                                                            )
    for pr in liste_a_enlever:
        print(pr['stagiaire_email']," ",pr['item_requis'])
        pr.delete()

#boucle sur la table stage pour mettre  en clair (txt) le type de stage (ex PSC1) 
def maj_stages_txt():
    liste = app_tables.stages.search()
    for stage in liste:
        #lecture fichier père type stage
        row_stage = app_tables.codes_stages.get(code=stage['code']['code'])
        stage.update(code_txt=row_stage['code'])
        print(stage['numero'], stage['code_txt'])

#boucle sur la table stagiaire inscrits pour  en clair txt 
def maj_stagiaires_inscrits_txt():
    # Drop down stages inscrits du user
    liste_stagiaires = app_tables.stagiaires_inscrits.search()
    
    for row in liste_stagiaires:
        #lecture fichier père stage
        stage=app_tables.stages.get(q.fetch_only("date_debut"),
                                                    numero=row['stage']['numero']
                                    )
        row.update(stage_txt=stage['code_txt'],
                  numero=stage['numero'])

#boucle sur la table pre_requis_stagiaire pour  en clair txt 
def maj_pr_stagiaires_txt():
    # Drop down stages inscrits du user
    liste_pr_stagiaires = app_tables.pre_requis_stagiaire.search()
    
    for row in liste_pr_stagiaires:
        #lecture fichier père stage
        stage = app_tables.stages.get(q.fetch_only("date_debut"),
                                                    numero=row['stage_num']['numero']
                                    )
        
        #lecture fichier père pré_requis
        pr = app_tables.pre_requis.get(code_pre_requis=row['item_requis']['code_pre_requis'])

        
        #lecture fichier père user
        try:
            usr = app_tables.users.get(email=row['stagiaire_email']['email'])
            
            row.update(code_txt=stage['code_txt'],
                  numero=stage['numero'],
                  nom=usr['nom'],
                  prenom=usr['prenom'],
                  requis_txt=pr['requis'])
            
        except:   # si user non trouvé, effact des pré requis
            print("row deleted for: ", row['stagiaire_email'])
            row.delete()

        
        
        