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



#boucle sur la table qcm pour l'effacmt des lignes du qcm 4, 
def loop_qcm2():
    #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=7)
    if qcm_row:
    
        table = app_tables.qcm.search(qcm_nb=qcm_row)
        result="erreur"
        if table:
            for row in table:
                row.delete()
            result="loop ok"     

#boucle sur la table qcm pour modif rapide d'une colonne, ici sur la description
def loop_qcm3():
    #lecture fichier père qcm descro
    qcm_row = app_tables.qcm_description.get(qcm_nb=4)
    if qcm_row:
        table = app_tables.qcm.search(qcm_nb=qcm_row)
        result="erreur"
        txt="BNSSA 1 'Conn. du milieu'"
        if table:
            for row in table:
                row.update(param = txt)
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