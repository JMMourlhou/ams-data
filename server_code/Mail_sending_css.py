import anvil.stripe
import anvil.files
from anvil.files import data_files
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
def send_mail_css(emails_list, subject_txt, rich_text, attachments=[]):
    #time=str(French_zone_server_side.time_french_zone())[0:16] # time will be text form 
    
    # Récupération des variables globales
    dict_var_glob = Variables_globales.get_variable_names()   # var_globale du mail d'AMS, stockées ds table 
        
    client_mail = dict_var_glob["client_mail"]   # var globale Mail AMS
    code_app2 = dict_var_glob["code_app2"]      # var_globale de l'apli AMS DATA
    logo_address = code_app2+"/_/theme/"+_Constant_parameters_public_ok.ams_logo
    print("logo address ok: ",logo_address)
    
    for email, prenom in emails_list:
        anvil.email.send(
            
            to=email,
            subject=subject_txt,
            attachments=attachments,

            
            html= """
                <!DOCTYPE html>
                <html lang="fr">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <style>
                        .top-two-backgrounds {
                            background-image: url(_/theme/Logo_AMS.png), 
                                            url(_/theme/AMS_ext_flou.png);
                            width: 100% auto;
                            height: 300px;
                            background-position: left top, center center;
                            background-size: 120px 60px, cover;
                            background-repeat: no-repeat, no-repeat;
                        }
                        .background-bottom {
                            background: url(_/theme/fonds_bleu_marin.png);
                            background-size: cover; /* Couvre toute la zone */ 
                            height: 100vh; /* 100% de la hauteur de la fenêtre */
                        }      
                    </style>
                    <title>Multiple Backgrounds</title>
                </head>
                <body>
                    <div class="top-two-backgrounds"></div>
                    <div class="background-bottom"></div>
                    
                </body>
                </html>
                <p><p style="color:blue;">{prenom},</p><br>
                <br>
                {rich_text} <br>
                <br>
                <i>"L'équipe d'AMSport,"</i>
                <br>
                {client_mail} <br>   
             """   
        
        )
        # possible de changer la couleur d'un texte:   <b><p style="color:blue;"> {user_row["prenom"]}, </p></b>
        
        return True

