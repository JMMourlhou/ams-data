import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# MODIF du QCM
@anvil.server.callable           #modif d'une ligne de Qcm
def modif_qcm(qcm_descro_row, num_question, question, reponse, bareme, photo, correction):
    """ lecture fichier père code stages
    code_stage = app_tables.codes_stages.get(code="PSE1")          # A MODIFIER QD RAJOUTE DIFFERENRS QCM
    if not code_stage:   
        alert("Code stage non trouvé ds fichier param Code_stages")
        valid=False
        return valid        
    """

    # lecture de la ligne à modifier par son numéro             
    qcm_row = app_tables.qcm.get(num=num_question,
                                qcm_nb=qcm_descro_row)
    if not qcm_row:
        print("Ligne qcm non trouvée ds fichier qcm")
        return False
    else:   
        qcm_row.update(question = question,
                     reponse = reponse,
                     bareme = str(bareme),
                     photo = photo,
                     correction= correction
                    )
        return True

# ENREGITREMENT du QCM pour un stagiaire
@anvil.server.callable 
@anvil.tables.in_transaction
def qcm_result(user, qcm_descro_row, qcm_nb, nb_bonnes_rep, max_points, points, reponses, mode="debut"):      # debut: debut de qcm, enregt du num et user
    
    if mode == "debut":
        #lire le fichier père qcm à partir du qcm number
        #
        #
        
        new_row=app_tables.qcm_result.add_row(
                                                user_qcm= user,
                                                qcm_number=qcm_number
                                                
                                )
    if mode == "fin":  
        import French_zone_server_side
        
        # finding the qcm row 
        row = app_tables.qcm_result.get(qcm_number=qcm_number)
        if not row:
            result = "QCM Row non trouvé"
        else:           
            row.update(
                        time= time_french_zone(),
                        liste_rep = reponses,
                        nb_rep_ok = nb_bonnes_rep,
                        pourcentage_ok=0
                              )
            result = "Résultats du QCM enregistrés"
        return result    