import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def add_ligne_qcm(num_question, question, correction, rep, bareme, image, qcm_nb):
    
    # qcm_nb est la row venant du dropdown choix du qcm

    if rep == True:
        rep_multi = "10"
    else:
        rep_multi = "01"
   
    new_row=app_tables.qcm.add_row(num= int(num_question),
                                   question = question,
                                   correction = correction,
                                   rep_multi = rep_multi,
                                   bareme = str(bareme),
                                   photo = image,
                                   qcm_nb = qcm_nb )

            
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
        if rep == True:
            rep_multi = "10"
        else:
            rep_multi = "01"
        qcm_row.update(question = question,
                     rep_multi = rep_multi,
                     bareme = str(bareme),
                     photo = photo,
                     correction= correction
                    )
        return True



# =====================================================================================================================
#                 UTILISATION DU QCM PAR UN STAGIAIRE, SAUVEGARDE DES RESULTATS DS table.qcm_result
# =====================================================================================================================
# ENREGITREMENT, en fin de questions du QCM pour un stagiaire
@anvil.server.callable 
@anvil.tables.in_transaction
def qcm_result(user, qcm_nb, nb_bonnes_rep, max_points, points, reponses):      # debut: debut de qcm, enregt du num et user
    import French_zone_server_side
    nb_questions = len(reponses)
    if nb_questions == 0:
        valid = False
        return
    p100_sur_nb_rep = int(nb_bonnes_rep / nb_questions * 100)
    p100_sur_points = int(points / max_points * 100)
    app_tables.qcm_result.add_row(
                                    user_qcm= user,
                                    qcm_number=qcm_nb,
                                    time= French_zone_server_side.time_french_zone(),
                                    liste_rep = reponses,
                                    nb_rep_ok = nb_bonnes_rep,
                                    p100_sur_nb_rep = p100_sur_nb_rep,
                                    p100_sur_points = p100_sur_points
                            )

    qcm_result_row = app_tables.qcm_result.search(qcm_number = qcm_nb,
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
def temp_user_qcm(user, nb_questions_in_qcm):
    #user.update(temp = int(nb_questions_in_qcm))
    result = False
    if user:
        try:
            user.update(temp = int(nb_questions_in_qcm))
            result = True
        except:
            result = False
            
    return result