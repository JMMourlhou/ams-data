import anvil.stripe
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
from PIL import Image
import io


@anvil.server.background_task
@anvil.server.callable
def print_pdf(file, file_name):
    
    """
    quality :
    "original": All images will be embedded at original resolution. Output file can be very large.
    "screen": Low-resolution output similar to the Acrobat Distiller “Screen Optimized” setting.
    "printer": Output similar to the Acrobat Distiller “Print Optimized” setting.
    "prepress": Output similar to Acrobat Distiller “Prepress Optimized” setting.
    "default": Output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.
    """
    
    media_object = PDFRenderer(page_size ='A4',
                            filename = f"{file_name}.pdf",
                            landscape = False,
                            margins = {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0},  # en cm
                            scale = 1.0,
                            quality =  "default"
                            ).render_form('Pre_Visu_img_Pdf_Generation',file)
    # sauver le mediaobject ds table temp
    temp_row = app_tables.temp.search()[0]
    if not temp_row:   
        result = False
    else:
        temp_row.update(media = media_object) # sauvegarde du pdf de l'image
        result = True


@anvil.server.callable
def run_bg_task_jpg(file, file_name):
    task = anvil.server.launch_background_task('print_pdf',file, file_name)
    return task