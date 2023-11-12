#import anvil.email
#import anvil.google.auth, anvil.google.drive, anvil.google.mail
#from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from PIL import Image

@anvil.server.callable
def download_img_pdf(file):
    image_1 = Image.open(file)
    im_1 = image_1.convert('RGB')
    #im_1.save(r'path where the pdf will be stored\new file name.pdf')
    anvil.media.download(im_1)