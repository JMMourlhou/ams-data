
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
@anvil.server.callable
def print_pdf(file, file_name):
    media_object = PDFRenderer(page_size ='A4',
                            filename = f"{file_name}.pdf",
                            landscape = False,
                            margins = {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0},  #  cm
                            scale = 1.0,
                            quality =  "default"
                            ).render_form('Pre_Visu_img_Pdf_Generation',file)
    # save mediaobject in table temp
    temp_row = app_tables.temp.search()[0]
    temp_row.update(media = media_object) # save the image object in temp file

@anvil.server.callable
def run_bg_task_jpg(file, file_name):
    task = anvil.server.launch_background_task('print_pdf',file, file_name)
    return task

@anvil.server.callable
def task_killer(task):
    task.kill()
    print("task killed")