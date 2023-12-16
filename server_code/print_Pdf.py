
import anvil.server
from anvil import *  #pour les alertes
import anvil.pdf
from anvil.pdf import PDFRenderer
from PIL import Image
import io


@anvil.server.background_task
@anvil.server.callable
def print_pdf(file, file_name="download.pdf"):
    """
    quality :
    "original": All images will be embedded at original resolution. Output file can be very large.
    "screen": Low-resolution output similar to the Acrobat Distiller “Screen Optimized” setting.
    "printer": Output similar to the Acrobat Distiller “Print Optimized” setting.
    "prepress": Output similar to Acrobat Distiller “Prepress Optimized” setting.
    "default": Output intended to be useful across a wide variety of uses, possibly at the expense of a larger output file.
    """
    
    file_name = file_name+".pdf" 
    print("file_name",file_name)
    media_object = PDFRenderer(page_size ='A4',
                            filename = file_name,
                            landscape = False,
                            margins = {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0},  # en cm
                            scale = 1.0,
                            quality =  "default"
                            ).render_form('Pre_Visu_img_Pdf',file, file_name, "pdf")
    return media_object

@anvil.server.callable
def run_bg_task_jpg(file, file_name="download.pdf"):
    task = anvil.server.launch_background_task('print_pdf',file, file_name="download.pdf")

    if task.is_completed():
        return task