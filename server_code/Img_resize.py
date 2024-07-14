import anvil.tables as tables
import anvil.server
import pathlib
from PIL import Image
import io

@anvil.server.callable
def resize_img(file, name):
    path = pathlib.Path(file.name)
    name = str(path.name)
    extension = str(path.suffix)  # path, file name, extension
    # Convert the 'file' Media object into a Pillow Image
    img = Image.open(io.BytesIO(file.get_bytes()))
    
    # Resize the image to the required size
    img = img.resize((800,600))
    img = img.convert("RGB")
    # Convert the Pillow Image into an Anvil Media object and return it
    bs = io.BytesIO()
    img.save(bs, format="JPEG")
    new_name = name+".jpg"
    return anvil.BlobMedia("image/jpeg", bs.getvalue(), name=new_name)