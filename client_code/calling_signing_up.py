from anvil import *
import anvil.server
from anvil import open_form
"""
Je constate que je ne peux pas appeler open_form d'une form
mais seulement d'un module !
"""
""" ************************************************************************"""  
"""               Calling SIGN UP app                                       """
""" ************************************************************************"""  
#import sign_up_for_AMS_Data
from sign_up_for_AMS_Data.Form1 import Form1

def calling_form1(h={}, num_stage=0):
   open_form('sign_up_for_AMS_Data.Form1',h, num_stage)


