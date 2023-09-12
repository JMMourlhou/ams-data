from ._anvil_designer import Visu_trombiTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

global position
position = 0
global tag_email
tag_email = ""

class Visu_trombi(Visu_trombiTemplate):
    def __init__(self,num_stage, intitule, pdf_mode=False, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.num_stage = num_stage
        self.intitule = intitule
        self.pdf_mode = pdf_mode
        larg = 175 # largeur image en pixel
        inter = 4  # Interval entre image
        size_bt = 100 # largeur du bt transparent pour permettre le click
        
        
        
        if self.pdf_mode == True:
            self.button_annuler.visible = False
            self.button_annuler2.visible = False
            #self.button_pdf.visible = False
            pass
            
        #lecture du fichier père stages
        stage_row = app_tables.stages.get(numero=int(num_stage))    

        cod = stage_row["type"]['code']
        date = str(stage_row["date_debut"].strftime("%d/%m/%Y"))
        self.label_titre.text = "Trombi stagiaires" + cod + " du " + date + "   (num " +num_stage+")"
        
        # extraction de la liste (fonction list())
        rows = list(app_tables.stagiaires_inscrits.search(
            tables.order_by("name", ascending=True),
            stage=stage_row
        ))     
        nb_stagiaires = len(rows)                      # nb de stagiaires
        print("nb-stagiaires", nb_stagiaires)
        
        cpt_stagiaire = 0
        cpt_ligne = 1
        for row in rows:
            #lecture fichier users à partir du mail
            mel=row["user_email"]['email']
            stagiaire = app_tables.users.get(email=mel)    
            if stagiaire :
                cpt_stagiaire += 1                 # compteur 
                #Photo
                orig_pic = stagiaire['photo']
                if orig_pic != None:
                    thumb_pic = anvil.image.generate_thumbnail(orig_pic, 160)
           
                self.im[cpt_stagiaire] = Image(background="white", 
                                    display_mode="shrink_to_fit",
                                    height = larg,
                                    source = thumb_pic,
                                    spacing_below = None,
                                    horizontal_align = "center",
                                    border = "1px solid black",
                                    visible = True,
                                    tag = mel
                                   )
                self.im[cpt_stagiaire].set_event_handler('mouse_down',self.im_mouse_down)
                
                txt = stagiaire['nom'] + " " + stagiaire['prenom']
                self.bt = Button(text=txt, tag = mel, spacing_above = None, background="", foreground="blue", bold=True, font_size = 11, enabled = True)
                self.bt.set_event_handler('click',self.bt_click)
                
                
                print("ligne ", cpt_ligne) 
                print("stagiaire", cpt_stagiaire)
                if cpt_ligne == 1:
                    yy = 1
                    if cpt_stagiaire == 1:
                        xx = 1
                        self.xy_panel.add_component(self.im, x=xx, y=yy, width = larg)
                        self.xy_panel.add_component(self.bt, x=xx, y=yy+larg, width = larg)  #nom,prénom
                        
                        
                    
                    if cpt_stagiaire == 2:
                        xx = xx + inter + larg
                        print(xx)   
                        self.xy_panel.add_component(self.im, x=xx, y=yy, width = larg)
                        self.xy_panel.add_component(self.bt, x=xx, y=yy+larg, width = larg)  #nom,prénom
                        
                    
                    if cpt_stagiaire == 3:
                        xx = xx + inter + larg  
                        print(xx)
                        self.xy_panel.add_component(self.im, x=xx, y=yy, width = larg)
                        # création du lien pour cliquer dessus
                        bt_3 = Button(text="    ", background="", foreground="black", font_size=size_bt)
                        self.xy_panel.add_component(bt_3, x=xx, y=yy)
                        bt_3.set_event_handler('click',self.bt_3_click)
                    
                    if cpt_stagiaire == 4:
                        xx = xx + inter + larg
                        print(xx)
                        self.xy_panel.add_component(self.im, x=xx, y=yy, width = larg)
                        # création du lien pour cliquer dessus
                        bt_4 = Button(text="    ", background="", foreground="black", font_size=size_bt)
                        self.xy_panel.add_component(bt_4, x=xx, y=yy)
                        bt_4.set_event_handler('click',self.bt_4_click)
                        
                        cpt_ligne += 1
                 
                if cpt_ligne == 2:
                    yy = 240
                   
                    if cpt_stagiaire == 5: 
                        xx = 1
                        print(xx)
                        self.xy_panel.add_component(self.im, x=xx, y=yy, width = larg)
                        # création du lien pour cliquer dessus
                        bt_5 = Button(text="    ", background="", foreground="black", font_size=size_bt)
                        self.xy_panel.add_component(bt_5, x=xx, y=yy)
                        bt_5.set_event_handler('click',self.bt_5_click)
                        
                    if cpt_stagiaire == 6: 
                        xx = xx + inter + larg
                        print(xx)
                        self.xy_panel.add_component(self.im, x=xx, y=yy, width = larg)
                        # création du lien pour cliquer dessus
                        bt_6 = Button(text="    ", background="", foreground="black", font_size=size_bt)
                        self.xy_panel.add_component(bt_6, x=xx, y=yy)
                        bt_6.set_event_handler('click',self.bt_6_click)

                    if cpt_stagiaire == 7: 
                        xx = xx + inter + larg
                        print(xx)
                        self.xy_panel.add_component(self.im, x=xx, y=yy, width = larg)
                        # création du lien pour cliquer dessus
                        bt_7 = Button(text="    ", background="", foreground="black", font_size=size_bt)
                        self.xy_panel.add_component(bt_7, x=xx, y=yy)
                        bt_7.set_event_handler('click',self.bt_7_click)

                    if cpt_stagiaire == 8: 
                        xx = xx + inter + larg
                        print(xx)
                        self.xy_panel.add_component(self.im, x=xx, y=yy, width = larg)
                        # création du lien pour cliquer dessus
                        bt_8 = Button(text="    ", background="", foreground="black", font_size=size_bt)
                        self.xy_panel.add_component(bt_8, x=xx, y=yy)
                        bt_8.set_event_handler('click',self.bt_8_click)
            else:
                " si pas de stagiaire "
                print("pas de stagiaire")

    
        
        

    def bt_2_click(self, **event_args):
        """This method is called when the link is clicked"""
        global position
        position = 2
        print("position", position)

    def bt_3_click(self, **event_args):
        """This method is called when the link is clicked"""
        global position
        position = 3
        print("position", position)

    def bt_4_click(self, **event_args):
        """This method is called when the link is clicked"""
        global position
        position = 4
        print("position", position)

    def bt_5_click(self, **event_args):
        """This method is called when the link is clicked"""
        global position
        position = 5
        print("position", position)        
                    
    
    def bt_6_click(self, **event_args):
        """This method is called when the link is clicked"""
        global position
        position = 6
        print("position", position)

    def bt_7_click(self, **event_args):
        """This method is called when the link is clicked"""
        global position
        position = 7
        print("position", position)  

    def bt_8_click(self, **event_args):
        """This method is called when the link is clicked"""
        global position
        position = 8
        print("position", position)  

    def button_annuler_click(self, **event_args):
        """This method is called when the button is clicked"""
        from ..Visu_stages import Visu_stages
        open_form('Visu_stages')

    def button_annuler2_click(self, **event_args):
        """This method is called when the button is clicked"""
        self.button_annuler_click()

    def bt_click(self, **event_args):
        """This method is called when the link is clicked"""
        email_stagiaire= self.bt.tag
        print(email_stagiaire)

  
    def im_mouse_down(self, x, y, sender, **event_args):
        """This method is called when the mouse cursor enters this component"""
        email_stagiaire= sender.tag
        print(email_stagiaire)
        