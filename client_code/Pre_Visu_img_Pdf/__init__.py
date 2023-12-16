from ._anvil_designer import Pre_Visu_img_PdfTemplate
from anvil import *
import anvil.server

class Pre_Visu_img_Pdf(Pre_Visu_img_PdfTemplate):
    def __init__(self, file, new_file_name, mode="visu", **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
     
        # Any code you write here will run before the form opens.

        self.new_file_name = new_file_name
        if mode == "visu":
            self.download.visible = True
            self.retour.visible = True
        self.image_1.source = file

    def retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form('Visu_stages')

    def download_click(self, **event_args):
        """This method is called when the button is clicked"""
        with anvil.server.no_loading_indicator:
            file = anvil.server.call("run_bg_task_jpg",self.image_1.source, self.new_file_name)
            
           
            anvil.media.download(file) 