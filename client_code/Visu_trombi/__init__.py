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
                    
                if cpt_ligne == 1:
                    if cpt_stagiaire == 1:
                        im1 = Image(background="white", 
                                    display_mode="shrink_to_fit",
                                    height = 160,
                                    source = thumb_pic,
                                    horizontal_align = "center",
                                   )
                        self.xy_panel.add_component(im1, x=1, y=1, width= 160)
                        # création du lien pour cliquer dessus
                        #bt_1 = Button(width=160, background="red")
                        #self.xy_panel.add_component(bt_1, x=1, y=1, width= 160)
                        #self.bt_1.set_event_handler('click', bt_1)

                    if cpt_stagiaire == 2:
                        im2 = Image(background="white",
                                    display_mode="shrink_to_fit",
                                    width = 160,
                                    height = 160,
                                    source = thumb_pic,
                                    horizontal_align = "center",
                                    visible = True
                                )
                        self.xy_panel.add_component(im2, x=180*1, y=1, width = 160)

                    if cpt_stagiaire == 3:
                        im3 = Image(background="white",
                                    display_mode="shrink_to_fit",
                                    width = 160,
                                    height = 160,
                                    source = thumb_pic,
                                    horizontal_align = "center",
                                    visible = True
                                )
                        self.xy_panel.add_component(im3, x=180*2, y=1, width = 160)

                        self.bt_1.visible = True
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


        

                

            
                    
            
