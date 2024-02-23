
import anvil.files
from anvil.files import data_files
import anvil.server
import qrcode
import qrcode.image.svg
from io import BytesIO
import anvil.media

@anvil.server.callable
def mk_qr_code(qr_code_data, **params):
    qr_code_obj = qrcode.make(qr_code_data, 
                              image_factory=qrcode.image.svg.SvgPathImage, 
                              error_correction=qrcode.constants.ERROR_CORRECT_Q,
                              box_size=25, version=2)
    data = BytesIO()
    qr_code_obj.save(data)
    data.seek(0)
    svg_text = data.read()
    
    b = anvil.BlobMedia("image/svg+xml", svg_text, name="qrcode.svg")
    return b