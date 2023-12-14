
import anvil.server

import anvil.pdf
from anvil.pdf import PDFRenderer
from PIL import Image
import io

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
    """
    # Convert the 'file' Media object into a Pillow Image
    img = Image.open(io.BytesIO(file.get_bytes()))
    width, height = img.size
    print('size', width, height)
    """
    
            
    media_object_pdf = PDFRenderer(page_size ='A4',
                            filename = file_name,
                            landscape = False,
                            margins = {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0},  # en cm
                            scale = 1.0,
                            quality =  "prepress"
                            ).render_form('image_Pdf',file)
    return media_object_pdf