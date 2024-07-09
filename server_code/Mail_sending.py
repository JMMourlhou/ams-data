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
def send_mail(emails_list, subject_txt, rich_text, attachments=[], old_stagiaires=False):
    #time=str(French_zone_server_side.time_french_zone())[0:16] # time will be text form 
    
    # Récupération des variables globales
    dict_var_glob = Variables_globales.get_variable_names()   # var_globale du mail d'AMS, stockées ds table 
        
    client_mail = dict_var_glob["client_mail"]   # var globale Mail AMS
    code_app2 = dict_var_glob["code_app2"]      # var_globale de l'apli AMS DATA
    logo_address = code_app2+"/_/theme/"+_Constant_parameters_public_ok.ams_logo
    en_tete_address = code_app2+"/_/theme/"+_Constant_parameters_public_ok.ams_en_tete
    print("logo address ok: ",logo_address)
    
    print(emails_list)
    for email, prenom in emails_list:
        try:
            anvil.email.send(
                to=email,
                subject=subject_txt,
                attachments=attachments,
                html=f"""
                    <p><img src = {en_tete_address} width="772" height="263"> </p>
                    <b>{prenom},</b><br>
                    <br>
                    {rich_text} <br>
                    <br>
                    <i>L'équipe d'AMSport,</i>
                    <br>
                    {client_mail} <br>
                    
                """
            )
            if old_stagiaires is True:
                print("ok", email)
                # sauver la date et l'heure
        
        except:
            if old_stagiaires is True:
                print("Email erroné", email)
                # sauver l'erreur
            
        # possible de changer la couleur d'un texte:   <b><p style="color:blue;"> {user_row["prenom"]}, </p></b>
        # insertion du logo     <p><img src = {en_tete_address} width="150" height="75"> </p>
    return True

