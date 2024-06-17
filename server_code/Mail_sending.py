from anvil import *
import anvil.files
from anvil.files import data_files
import anvil.email
import tables
from tables import app_tables
import anvil.users
import anvil.server
from anvil.http import url_encode

from . import French_zone_server_side
from . import Variables_globales # importation du module de lecture des variables globales (sauf mon logo)
from . import _Constant_parameters_public_ok

"""Send an email to the specified user"""
@anvil.server.callable
def send_mail(emails_list, subject_txt, rich_text, attachments=[]):
    #time=str(French_zone_server_side.time_french_zone())[0:16] # time will be text form 
    
    # Récupération des variables globales
    dict_var_glob = Variables_globales.get_variable_names()   # var_globale du mail d'AMS, stockées ds table 
        
    client_mail = dict_var_glob["client_mail"]   # var globale Mail AMS
    code_app2 = dict_var_glob["code_app2"]      # var_globale de l'apli AMS DATA
    logo_address = code_app2+"/_/theme/"+_Constant_parameters_public_ok.ams_logo
    print(logo_address)

    for user_row in emails_list:
        anvil.email.send(
            to=user_row['email'],
            subject=subject_txt,
            attachments=attachments,
            html=f"""
                <p><img src = {logo_address} width="150" height="75"> </p>
                <b>{user_row["prenom"]},</b><br>
                <br>
                {rich_text} <br>
                <br>
                <i>L'équipe d'AMSport,</i>
                <br>
                <b>{client_mail}</b> <br>
                
            """
        )
        # possible de changer la couleur d'un texte:   <b><p style="color:blue;"> {user_row["prenom"]}, </p></b>
        
        return True

