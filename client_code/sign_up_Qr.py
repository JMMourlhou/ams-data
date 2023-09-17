import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import open_form


def signup_with_qr(h={}, num_stage=0):
    
    from sign_in_for_AMS_Data.SignupDialog_V2 import SignupDialog_V2
    open_form("sign_in_for_AMS_Data.SignupDialog_V2",h,num_stage)
