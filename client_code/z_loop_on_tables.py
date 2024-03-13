import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
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

    