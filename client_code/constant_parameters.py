import stripe.checkout
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

# Variables globales que j'appelle par:     constant_parameters.logo_client
code_app1 = "https://sxgqveyu3c2nj5kr.anvil.app/BBDLB54NWHHYKEE3YYGJGU4G"   # App "AMS Data"  
code_app2 = "https://2erggvosxp234ktt.anvil.app/EK44RJHJVMRZ7R52DY6NEURF" # App "sign-up_for_AMS_Data"
nom_app_pour_mail = "AMSport Data"                                          
mon_mail = "jmarc@jmm-formation-et-services.fr"
mon_logo = "_/theme/Logo%20F%20S%20small_transparent.png"
logo_client = "_/theme/Logo%20AMS.JPG"
nb_stages_a_montrer = 10      # 10 derniers stages à montrer
nb_fiche_stagiaire_pdf = 5   # 1 fiche avec photo en haut (sinon mettre 6)