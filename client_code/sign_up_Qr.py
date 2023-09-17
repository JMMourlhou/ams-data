import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



def signup_with_qr(h={}, num_stage=0):
    
    from .Main import Main
    self=Main()
    from sign_in_for_AMS_Data.SignupDialog_V2 import SignupDialog_V2
    Main.content_panel.clear()
    Main.content_panel.add_component(SignupDialog_V2(h, num_stage), full_width_row=True)
