import anvil.tables as tables
import anvil.server
import pathlib
from PIL import Image
import io

@anvil.server.callable
def resize_img(file):
    path = pathlib.Path(file.name)
    name = str(path.name)
    extension = str(path.suffix)  # path, file name, extension
    lg_totale = len(name)
    lg_ext = len(extension)
    suffixe = name[0:lg_totale-lg_ext]
    
    # Convert the 'file' Media object into a Pillow Image
    img = Image.open(io.BytesIO(file.get_bytes()))
    width, height = img.size
    # Resize the image to the required size
    img = img.resize((800,600))
    img = img.convert("RGB")
    
    # Convert the Pillow Image into an Anvil Media object and return it
    bs = io.BytesIO()
    img.save(bs, format="JPEG")
    new_name = suffixe+".jpg"
    return anvil.BlobMedia("image/jpeg", bs.getvalue(), name=new_name)