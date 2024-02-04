import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def add_ligne_qcm(num_question, question, correction, rep, bareme, image, qcm_nb, type, param):
    
    # qcm_nb est la row venant du dropdown choix du qcm
   
    new_row=app_tables.qcm.add_row(num= int(num_question),
                                   question = question,
                                   correction = correction,
                                   rep_multi = rep,
                                   bareme = str(bareme),
                                   photo = image,
                                   qcm_nb = qcm_nb,
                                   type = type,
                                   param = param)

            
    qcm_row = app_tables.qcm.search(qcm_nb = qcm_nb,
                                    num=num_question
                                    )
    if qcm_row:
        valid=True
    else:
        valid=False
    return valid

# =================================================================================================================
# MODIF du QCM (en maj d'un qcm)
@anvil.server.callable           #modif d'une ligne de Qcm
def modif_qcm(qcm_descro_row, num_question, question, rep, bareme, photo, correction):

    # lecture de la ligne à modifier par son numéro             
    qcm_row = app_tables.qcm.get(num=num_question,
                                qcm_nb=qcm_descro_row)
    if not qcm_row:
        print("Ligne qcm non trouvée ds fichier qcm")
        return False
    else:   
        rep_multi = rep
        qcm_row.update(question = question,
                     rep_multi = rep,
                     bareme = str(bareme),
                     photo = photo,
                     correction= correction
                    )
        return True

# =================================================================================================================
# Delete d'1 ligne du QCM (en mode maj d'un qcm)
@anvil.server.callable           #modif d'une ligne de Qcm
def delete_qcm(qcm_descro_row, num_question):

    # lecture de la ligne à modifier par son numéro             
    qcm_row = app_tables.qcm.get(num=num_question,
                                qcm_nb=qcm_descro_row)
    if not qcm_row:
        print("Ligne qcm non trouvée ds fichier qcm")
        return False
    else:   
        qcm_row.delete()        
        return True

# ==================================================================================================
# modify the question number of the qcm questions after a deletion of a question
# ==================================================================================================
@anvil.server.callable
def renumber_qcm(qcm_descro_row):
#lecture fichier père qcm descro
        table = app_tables.qcm.search(qcm_nb=qcm_descro_row)
        result=False
        cpt = 0
        if table:
            for row in table:
                cpt += 1
                row.update(num = cpt
                          )
            result=True
        param_table_qcm = qcm_descro_row["destination"]
        print(f"loop Re-numération après delete ds table {param_table_qcm}: {result}")
        return result    

# =====================================================================================================================
#                 UTILISATION DU QCM PAR UN STAGIAIRE, SAUVEGARDE DES RESULTATS DS table.qcm_result
# =====================================================================================================================
# ENREGITREMENT, en fin de questions du QCM pour un stagiaire
@anvil.server.callable 
@anvil.tables.in_transaction
def qcm_result(user, qcm_numero, nb_bonnes_rep, max_points, points, reponses):      # debut: debut de qcm, enregt du num et user
    import French_zone_server_side
    nb_questions = len(reponses)
    if nb_questions == 0:
        valid = False
        return
    p100_sur_nb_rep = int(nb_bonnes_rep / nb_questions * 100)
    p100_sur_points = int(points / max_points * 100)

    # lecture fichier qcm_decription
    qcm_row=app_tables.qcm_description.get(qcm_nb=qcm_numero)
    
    app_tables.qcm_result.add_row(
                                    user_qcm= user,
                                    qcm_number=qcm_row,
                                    time= French_zone_server_side.time_french_zone(),
                                    liste_rep = reponses,
                                    nb_rep_ok = nb_bonnes_rep,
                                    p100_sur_nb_rep = p100_sur_nb_rep,
                                    p100_sur_points = p100_sur_points
                            )

    qcm_result_row = app_tables.qcm_result.search(qcm_number = qcm_row,
                                                  user_qcm= user,
                                            )
    if qcm_result_row:
        valid=True
    else:
        valid=False
    return valid


# ==================================================================================================
# modify the column temp of table user during qcm (nb of questions)
# ==================================================================================================
@anvil.server.callable
def temp_user_qcm(user, nb_questions_in_qcm, numero_qcm):
    #user.update(temp = int(nb_questions_in_qcm))
    result = False
    if user:
        try:
            user.update(temp = int(nb_questions_in_qcm),        # temp2 contient 'test' si le concepteur a testé son qcm     
                        temp3 = str(numero_qcm)                 # temp3 contient num du qcm réel
                       )                                        # temp contient le nb de questions
            result = True
        except:
            result = False
            
    return result
