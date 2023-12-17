from ._anvil_designer import Pre_Visu_img_PdfTemplate
from anvil import *
import stripe.checkout
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Pre_Visu_img_Pdf(Pre_Visu_img_PdfTemplate):
    def __init__(self, file, new_file_name, mode="visu", **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        self.image_1.source = file
        self.new_file_name = new_file_name
        print("new file name:", new_file_name)
        with anvil.server.no_loading_indicator:
            self.task = anvil.server.call("run_bg_task_jpg",self.image_1.source, self.new_file_name)
       
        if mode == "visu":
            self.download.visible = True
            self.retour.visible = True
        

    def retour_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form('Visu_stages')

    def download_click(self, **event_args):
        """This method is called when the button is clicked"""
        with anvil.server.no_loading_indicator:
            if self.task.is_completed():
                # recup file pdf de table temp
                temp_row = app_tables.temp.search()[0]
                file = temp_row['media']
                anvil.media.download(file) 
                # kill the task
            

    def timer_1_tick(self, **event_args):
        """This method is called Every 0.5 seconds. Does not trigger if [interval] is 0."""
        if self.task.is_completed():
            self.timer_1.interval = 0


 