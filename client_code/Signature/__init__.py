from ._anvil_designer import SignatureTemplate
from anvil import *
import anvil.server

import anvil.users
import anvil.tables as tables
from anvil.tables import app_tables

class Signature(SignatureTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        # Any code you write here will run when the form opens.
        self.pen_down = False
        self.lastx = self.lasty = 0
    
    def canvas_1_mouse_leave (self, x, y, **event_args):
        # This method is called when the mouse cursor leaves this component
        self.pen_down = False
    
    def canvas_1_mouse_down (self, x, y, button, **event_args):
        # This method is called when a mouse button is pressed on this component
        self.pen_down = True
        self.lastx = x
        self.lasty = y
    
    def canvas_1_mouse_move (self, x, y, **event_args):
        # This method is called when the mouse cursor moves over this component
        if self.pen_down:
        self.canvas_1.begin_path()
        self.canvas_1.move_to(self.lastx, self.lasty)
        self.canvas_1.line_to(x, y)
        self.canvas_1.stroke()
        self.lastx = x
        self.lasty = y
    
    def canvas_1_mouse_up (self, x, y, button, **event_args):
        # This method is called when a mouse button is released on this component
        self.pen_down = False
    
    def form_show (self, **event_args):
        # This method is called when the column panel is shown on the screen
        self.canvas_1.line_width = 5
        self.canvas_1.line_cap = "round"
        
    def get_image(self):
        return self.canvas_1.get_image()
    
    def clear(self):
        self.canvas_1.clear_rect(0, 0, self.canvas_1.get_width(), self.canvas_1.get_height())

    
    def button_save_click (self, **event_args):
    # This method is called when the button is clicked
    self.column_panel_2.visible = True    # contient l'image sauvée
    self.image_1.source = self.get_image()    # Image à sauver
    self.clear()

  def button_erase_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.clear()
