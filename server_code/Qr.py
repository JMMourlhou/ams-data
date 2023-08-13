
import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# Importing package/library in param of AMS_Data
#import qrcode
import io
import qrcode
#import png
import PIL.Image as Image
import base64

from . import French_zone # importation du module pour le calcul du jour / heure

@anvil.server.callable   
def qr_generator(data="https://sxgqveyu3c2nj5kr.anvil.app/BBDLB54NWHHYKEE3YYGJGU4G"):
    img1 = qrcode.make(data)
    b=base64.b64decode(img1)
    print(b)
    img = Image.open(io.BytesIO(b))
      
        
    # saving the image in my table 'Qr_codes'
    app_tables.qr_codes.add_row(time= French_zone.french_zone_time(),
                          description="essai",
                          qr_code=img)