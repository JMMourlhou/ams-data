from ._anvil_designer import QrCode_GeneratorTemplate
from anvil import *
import anvil.server

# Génération de QR code à partir du texte saisi pui téléchrgt en pdf
class QrCode_Generator(QrCode_GeneratorTemplate):
    def __init__(self, file="", **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run before the form opens.
        if file != "":
            self.column_panel_1.visible = False
            
    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Main import Main
        open_form('Main',99)

    def text_box_1_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        text = self.text_box_1.text
        print("code",text)
        media=anvil.server.call('mk_qr_code',text)
        self.image_1.source=media

    def button_pdf_click(self, **event_args):
        """This method is called when the button is clicked"""
        file = self.image_1.source
        pdf = anvil.server.call("generate_pdf",file, file_name="document")
        if pdf:
            anvil.media.download(pdf)
            alert("QR code téléchargé !")
        else:
            alert("Pdf du QR code non généré")
