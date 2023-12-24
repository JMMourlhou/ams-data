
import anvil.files
from anvil.files import data_files
import anvil.tables as tables
from anvil.tables import app_tables
import anvil.tables.query as q
import anvil.server
from anvil import *  #pour les alertes

import anvil.media
import anvil.pdf
from anvil.pdf import PDFRenderer

@anvil.server.background_task
#@anvil.server.callable
def create_doc_img_into_pdf(file, file_name, stage_num, email, item_requis):
    media_object = PDFRenderer(page_size ='A4',
                            filename = f"{file_name}.pdf",
                            landscape = False,
                            margins = {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0},  #  cm
                            scale = 1.0,
                            quality =  "default"
                            ).render_form('Pre_Visu_img_Pdf_Generation',file)
                            #).render_form('Pre_Visu_img_Pdf',file, file_name, stage_num, email, item_requis)
    # save mediaobject in table pre requi du stage/stagiaire/pre requi  
    # finding the row
    pr_requis_row = app_tables.pre_requis_stagiaire.get(stage_num = stage_num,
                                              stagiaire_email = email,
                                              item_requis = item_requis                                             
                                             )                                      
    if not pr_requis_row:
        print("Erreur: stagiaire not found !")
    else: 
        pr_requis_row.update(
                            pdf_doc1 = media_object
                          )

@anvil.server.callable
def run_bg_task_jpg(file, file_name, stage_num, email, item_requis):
    task = anvil.server.launch_background_task('create_doc_img_into_pdf',file, file_name, stage_num, email, item_requis)
    return task

