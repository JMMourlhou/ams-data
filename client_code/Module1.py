from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
from anvil import open_form
"""
Je constate que je ne peux pas appeler open_form d'une form
mais seulement d'un module !
"""
""" ************************************************************************"""  
"""               Calling SIGN UP app                                       """
""" ************************************************************************"""  
import fr_custom_signup
from fr_custom_signup.Form1 import Form1

def calling_form1(h={}):
    open_form('fr_custom_signup.Form1',h)


