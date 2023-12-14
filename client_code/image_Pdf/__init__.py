from ._anvil_designer import image_PdfTemplate
from anvil import *


class image_Pdf(image_PdfTemplate):
    def __init__(self, file, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.image_1.source = file