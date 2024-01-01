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
                     