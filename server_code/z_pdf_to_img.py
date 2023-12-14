import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
import anvil.server
import os
import tempfile
from pdf2image import convert_from_path
import requests
from typing import List
from io import BytesIO
from shutil import copyfile

@anvil.server.callable
def pdf_into_images(stage_num, item_requis, email) -> List:   # file est un pdf qui vient d'être choisi par le user
    # finding the stagiaire's row 
    row = app_tables.pre_requis_stagiaire.get(stage_num = stage_num,
                                              stagiaire_email = email,
                                              item_requis = item_requis                                             
                                             )
    if not row:
        print("module pdf_into_images","Erreur: stagiaire not found !")
        return False  
    else:
        print("module pdf_into_images",row['stagiaire_email'], row['item_requis'], row['pdf_doc1'])
   
    media = row["pdf_doc1"]
    return get_pdf_file_images(media=media)
    

@anvil.server.callable
def get_pdf_file_images_from_url(pdf_file_url: str) -> List:
    with tempfile.TemporaryDirectory() as tmpdirname:
        pdf_file_path = os.path.join(tmpdirname, 'tmp.pdf')
        _download_file(pdf_file_url, pdf_file_path)
        return get_images_from_pdf_file(pdf_file_path, tmpdirname)


def get_pdf_file_images(media: anvil.media) -> List:
    with tempfile.TemporaryDirectory() as tmpdirname:
        pdf_file_path = os.path.join(tmpdirname, media.name)
        _write_file(pdf_file_path, media)
        return get_images_from_pdf_file(pdf_file_path, tmpdirname)

def _write_file(file_name, media):
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, "wb") as f:
        if type(media) == BytesIO:
            _write_bytes_io(file_name, media)
        else:
            f.write(media.get_bytes())


def _write_bytes_io(file_name: str, bytes_io_file: BytesIO):
    bytes_io_file.seek(0)
    with open(file_name, 'wb') as f:
        shutil.copyfileobj(bytes_io_file, f)


def _download_file(url, destination):
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            file.write(response.content)
        print("File downloaded successfully.")
    else:
        print("Failed to download the file.")


def get_images_from_pdf_file(pdf_file_path: str, target_folder: str) -> List:
    images = pdf_to_jpg(source_file_path=pdf_file_path, target_folder_path=target_folder)
    return [anvil.media.from_file(fpath) for fpath in images]


def pdf_to_jpg(source_file_path: str, target_folder_path: str) -> List[str]:
    images = convert_from_path(source_file_path)

    im_paths = []
    for i in range(len(images)):
        # Save pages as images in the pdf
        im_name = 'page' + str(i) + '.jpg'
        path = os.path.join(target_folder_path, im_name)
        im_paths.append(path)
        images[i].save(path, 'JPEG')

    return im_paths
  