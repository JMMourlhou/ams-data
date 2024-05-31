from anvil import *
import anvil.files
from anvil.files import data_files
import anvil.email
import tables
from tables import app_tables
import anvil.users
import anvil.server

from anvil.http import url_encode
#import bcrypt

#import uuid   # this library generates codes (API keys for exemple)
#import sys
from . import French_zone_server_side
from . import Variables_globales # importation du module de lecture des variables globales (sauf mon logo)
from . import _Constant_parameters_public_ok

"""Send an email to the specified user"""
@anvil.server.callable
def send_mail(user_row, subject_txt, rich_text="Rich_text à insérer"):
    time=French_zone_server_side.time_french_zone() # time will be text form 
    # Récupération des variables globales
    dict_var_glob = Variables_globales.get_variable_names()   # var_globale du mail d'AMS, stockées ds table 
        
    client_mail = dict_var_glob["client_mail"]   # var globalenMail ams
    code_app2 = dict_var_glob["code_app2"]      # var_globale de l'apli AMS DATA
    logo = app_tables.files.get(path="Logo_F_S_small.png")
    #logo = dict_var_glob["logo_client"]         # var_globale du logo AMSport
    #logo_address = code_app2+logo
    #logo_address = code_app1+"/_/theme/"+logo['path']
    logo_address = code_app2+"/_/theme/"+_Constant_parameters_public_ok.ams_logo
    print(logo_address)
    
    anvil.email.send(
        to=user_row['email'],
        subject=subject_txt,
        html=f"""
            <p><img src = {logo_address} width="200" height="100"> </p> 
            <b> {user_row["prenom"]},</b><br>
            <br>
            <b>{rich_text}</b>
             <br>
            <b>  https://sxgqveyu3c2nj5kr.anvil.app/32M6REZ23NPHINCU26GAZBNM   </b><br><br>
            <b><i>         L'équipe d'AMSport,</i></b>
            <br>
            <b>{client_mail}</b> <br>
            <br>
            <b>(Mail envoyé le {time})</b>
        """
    )
      
    return True

