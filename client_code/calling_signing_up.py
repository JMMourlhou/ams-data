from anvil import *
from anvil import open_form
"""
Je constate que je ne peux pas appeler open_form d'une form
mais seulement d'un module !
"""
""" ************************************************************************"""  
"""               Calling SIGN UP app                                       """
""" ************************************************************************"""  
import sign_in_for_AMS_Data
from sign_up_for_AMS_Data.Form1 import Form1

def calling_form1(h={}):
    #component=Form1() # I create the object 
    #form=navigation.get_form()
    #form.load_component(component)
    #alert(h)
    open_form('fr_custom_signup.Form1',h)


