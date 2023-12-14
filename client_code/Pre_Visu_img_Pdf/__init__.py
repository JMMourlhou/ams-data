from ._anvil_designer import Pre_Visu_img_PdfTemplate
from anvil import *
import anvil.server

class Pre_Visu_img_Pdf(Pre_Visu_img_PdfTemplate):
    def __init__(self, file, new_file_name, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.new_file_name = new_file_name

        # Any code you write here will run before the form opens.
        self.image_1.source = file

    def Retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form('Visu_stages')

    def download_click(self, **event_args):
        """This method is called when the button is clicked"""
        file = anvil.server.call("print_pdf",self.image_1.source, self.new_file_name)
        anvil.media.download(file) 
