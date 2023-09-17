import anvil.server
from anvil.google.drive import app_files
from anvil import *   # to load the alert 
from anvil import open_form


""" This is the startup module.

Il permet de tester si APP mère est appelé par une URL en cas de sign in ou pw reset 

"""


def start_app():
    print("app lancée par url ?")
    h={}
    h = anvil.get_url_hash()
    print(f"h ds init d'AMS_Data: {h}")
        
    if len(h)!=0 :  # a URL has openned this app
        
    
        # stage number in URL's Hash ? (le user vient-il de flacher le Qr code?)
        # si oui je suis en sign in après flash du qr code par le stagiare
        if "stage" in h:
            num_stage=h["stage"]
            alert(f"num stage test {num_stage}")
            if len(num_stage) != 0 :        
                
                from sign_in_for_AMS_Data.SignupDialog_V2 import SignupDialog_V2
                open_form("sign_in_for_AMS_Data.SignupDialog_V2")
                #self.content_panel.add_component(SignupDialog_V2(h, num_stage), full_width_row=True)
                    
    

