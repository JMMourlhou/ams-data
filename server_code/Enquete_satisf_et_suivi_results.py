import anvil.email
from anvil.tables import app_tables
import anvil.server
from anvil.pdf import PDFRenderer

import time   # Pour calculer le tps de traitement
from datetime import datetime  # pour mettre la date et heure ds nomde fichier pdf (temporaire pour test)
from pytz import timezone      # 

"""
    quality :
    "original": All images will be embedded at original resolution. Output file can be very large.
    "screen": Low-resolution output similar to the Acrobat Distiller “Screen Optimized” setting.
    "printer": Output similar to the Acrobat Distiller “Print Optimized” setting.
    "prepress": Output similar to Acrobat Distiller “Prepress Optimized” setting.
 ** "default": Output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.
    """
# Calculer la taille du file et ajuster la qualité (screen : pas assez bon)

"""----------------------------------------------------------------------------------------------------------
                   BG task    Formulaire de SATISFACTION  Génération du PDF et sauvegarde en table stage
   ---------------------------------------------------------------------------------------------------------
"""
@anvil.server.background_task
def generate_satisf_results(stage_num, type, row):
    start = time.time()   # pour calcul du tpsde traitement (environ 25 sec)
    now_utc = datetime.now(timezone('UTC'))
    date_time = now_utc.astimezone(timezone('Europe/Paris')) # initialisation of the date & time of writing

    pdf_object = PDFRenderer(page_size ='A4',
                            filename = f"Enquete_satisf_{type}_{stage_num}_{date_time}.pdf",
                            #filename = f"Enquete_satisf_{type}_{stage_num}.pdf",
                            landscape = False,
                            margins = {'top': 0.3, 'bottom': 0.1, 'left': 0.2, 'right': 0.2},  #  cm
                            scale = 1.0,                                                       
                            quality = "screen"      
                            ).render_form('Stage_satisf_statistics',True,row)    # True: pdf mode, j'efface le bt return et passe le row du stage qui avait été sélectionné
   
    # sauvegarde du résultat de l'enquete media
    row.update(satis_pdf = pdf_object) 
    end = time.time()
    print("Temps de traitement: ", end-start)
    
# A FAIRE APPELER from client side
@anvil.server.callable
def run_bg_task_satisf(stage_num, type, row):
    task = anvil.server.launch_background_task('generate_satisf_results',stage_num, type, row)
    return task


"""----------------------------------------------------------------------------------------------------------
                   BG task    Formulaire de SUIVI Génération du PDF et sauvegarde en table stage
    ---------------------------------------------------------------------------------------------------------
"""
@anvil.server.background_task
def generate_suivi_results(type_suivi, stage_num, type, row):
    start = time.time()   # pour calcul du tpsde traitement (environ 25 se)
    now_utc = datetime.now(timezone('UTC'))
    date_time = now_utc.astimezone(timezone('Europe/Paris')) # initialisation of the date & time of writing

    pdf_object = PDFRenderer(page_size ='A4',
                            filename = f"Enquete_satisf_{type}_{stage_num}_{date_time}.pdf",
                            #filename = f"Enquete_satisf_{type}_{stage_num}.pdf",
                            landscape = False,
                            margins = {'top': 0.3, 'bottom': 0.1, 'left': 0.2, 'right': 0.2},  #  cm
                            scale = 1.0,                                                       
                            quality = "screen"      
                            ).render_form('Stage_suivi_results',type_suivi, True,row)    # True: pdf mode, j'efface le bt return et passe le row du stage qui avait été sélectionné
   
    # sauvegarde du résultat de l'enquete media
    row.update(suivi_pdf = pdf_object) 
    end = time.time()
    print("Temps de traitement: ", end-start)
    
# A FAIRE APPELER from client side
@anvil.server.callable
def run_bg_task_suivi(type_suivi, stage_num, type, row):
    task = anvil.server.launch_background_task('generate_suivi_results', type_suivi, stage_num, type, row)
    return task

# Appelé par Stage_visu_modif
# Inclure pour tous les stagiaires du stage_num les formulaires de satisfaction quand on a créé ou maj ce formulaire 
@anvil.server.callable
def update_satisf_pour_un_stage(stage_row, satis_dico2_q_ouv, satis_dico1_q_ferm):   # stage_row : 1 row table 'stages' 
    stage_row.update( satis_dico1_q_ferm = satis_dico1_q_ferm,
                      satis_dico2_q_ouv = satis_dico2_q_ouv
                        )
    return


 # Appelé par Stage_visu_modif   
# Inclure pour tous les stagiaires du stage_num les formulaires de suivi quand on a créé ou maj ce formulaire
@anvil.server.callable
def update_suivi_pour_un_stage(stage_row, suivi_dico1_q_ouv, suivi_dico1_q_ferm):   # stage_row : 1 row table 'stages' 
    stage_row.update( suivi_dico1_q_ferm = suivi_dico1_q_ferm,
                      suivi_dico1_q_ouv = suivi_dico1_q_ouv
                        )
    return