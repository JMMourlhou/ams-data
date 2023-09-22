import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def save_qcm(user_email, result_qcm, qcm_list):
    result = False
    # lecture fichier père users
    row_user = app_tables.users.get(email=user_email)
    if row_user:
        # lecture fichier stagiaires inscrits
        row_stagiaire_inscrit=app_tables.stagiaires_inscrits.get(user_email=row_user) 
        if row_stagiaire_inscrit:
            row_stagiaire_inscrit.update(result_qcm=result_qcm,
                                        qcm_list=qcm_list)
            result = True
    return result