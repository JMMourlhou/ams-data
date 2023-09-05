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

class Visu_trombi(Visu_trombiTemplate):
    def __init__(self,num_stage, intitule, pdf_mode=False, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.num_stage = num_stage
        self.intitule = intitule
        self.pdf_mode = pdf_mode
        if self.pdf_mode == True:
            #self.button_annuler.visible = False
            #self.button_pdf.visible = False
            pass
            
        #lecture du fichier père stages
        stage_row = app_tables.stages.get(numero=int(num_stage))    
        
        # extraction de la liste (fonction list())
        rows = list(app_tables.stagiaires_inscrits.search(
            tables.order_by("name", ascending=True),
            stage=stage_row
        ))     
        nb_stagiaires = len(rows)                      # nb de stagiaires
        
             
        cpt_stagiaire = 0
        cpt_ligne = 0
        
        for row in rows:
            #lecture fichier users à partir du mail
            mel=row["user_email"]['email']
            stagiaire = app_tables.users.get(email=mel)    
            if stagiaire :
                #Photo
                orig_pic = stagiaire['photo']
                if orig_pic != None:
                    thumb_pic = anvil.image.generate_thumbnail(orig_pic, 160)

                cpt_stagiaire += 1                                    # compteur 
                if (cpt_ligne // 4) * 4 == cpt_ligne:                 # chgt de ligne
                    cpt_ligne += 1

                esp = 150 # espace en pixel
                
                if cpt_ligne == 1:
                    if cpt_stagiaire == 1:
                        im1 = Image(background="white", 
                                    display_mode="shrink_to_fit",
                                    height = esp,
                                    source = thumb_pic,
                                    horizontal_align = "center",
                                   )
                        self.xy_panel.add_component(im1, x=1, y=1, width= esp)
                        # création du lien pour cliquer dessus
                        bt_1 = Button(text="    ", background="", foreground="black", font_size=100)
                        self.xy_panel.add_component(bt_1, x=1, y=1)
                        bt_1.set_event_handler('click',self.bt_1_click)
                        
                    if cpt_stagiaire == 2:
                        im2 = Image(background="white",
                                    display_mode="shrink_to_fit",
                                    
                                    height = esp,
                                    source = thumb_pic,
                                    horizontal_align = "center",
                                    visible = True
                                )
                        self.xy_panel.add_component(im2, x=esp*1, y=1, width = esp)
                        # création du lien pour cliquer dessus
                        bt_2 = Button(text="    ", background="", foreground="black", font_size=100)
                        self.xy_panel.add_component(bt_2, x=esp*1, y=1)
                        bt_2.set_event_handler('click',self.bt_2_click)
                        
                    if cpt_stagiaire == 3:
                        im3 = Image(background="white",
                                    display_mode="shrink_to_fit",
                                    
                                    height = esp,
                                    source = thumb_pic,
                                    horizontal_align = "center",
                                    visible = True
                                )
                        self.xy_panel.add_component(im3, x=esp*2, y=1, width = esp)
                        # création du lien pour cliquer dessus
                        bt_3 = Button(text="    ", background="", foreground="black", font_size=100)
                        self.xy_panel.add_component(bt_3, x=esp*2, y=1)
                        bt_3.set_event_handler('click',self.bt_3_click)

                    if cpt_stagiaire == 4:
                        im4 = Image(background="white",
                                    display_mode="shrink_to_fit",
                                    
                                    height = esp,
                                    source = thumb_pic,
                                    horizontal_align = "center",
                                    visible = True
                                )
                        self.xy_panel.add_component(im4, x=esp*3, y=1, width = esp)
                        # création du lien pour cliquer dessus
                        bt_4 = Button(text="    ", background="", foreground="black", font_size=100)
                        self.xy_panel.add_component(bt_4, x=esp*3, y=1)
                        bt_4.set_event_handler('click',self.bt_4_click)

                    if cpt_stagiaire == 5:
                        im5 = Image(background="white",
                                    display_mode="shrink_to_fit",
                                    
                                    height = esp,
                                    source = thumb_pic,
                                    horizontal_align = "center",
                                    visible = True
                                )
                        self.xy_panel.add_component(im5, x=esp*4, y=1, width = esp)
                        # création du lien pour cliquer dessus
                        bt_5 = Button(text="    ", background="", foreground="black", font_size=100)
                        self.xy_panel.add_component(bt_5, x=esp*4, y=1)
                        bt_5.set_event_handler('click',self.bt_5_click)

                    if cpt_stagiaire == 6:
                        im6 = Image(background="white",
                                    display_mode="shrink_to_fit",
                                    
                                    height = esp,
                                    source = thumb_pic,
                                    horizontal_align = "center",
                                    visible = True
                                )
                        self.xy_panel.add_component(im6, x=esp*5, y=1, width = esp)
                        # création du lien pour cliquer dessus
                        bt_6 = Button(text="    ", background="", foreground="black", font_size=100)
                        self.xy_panel.add_component(bt_6, x=esp*5, y=1)
                        bt_6.set_event_handler('click',self.bt_6_click)
                else:
                    " pas premiere ligne "
                    pass
            else:
                " si pas de stagiaire "
                pass

    def bt_1_click(self, **event_args):
        """This method is called when the link is clicked"""
        global position
        position = 1
        print("position", position)

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
            
                    
            
