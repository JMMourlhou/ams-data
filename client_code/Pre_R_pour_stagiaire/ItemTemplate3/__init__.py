from ._anvil_designer import ItemTemplate3Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media
from ...import Pre_R_doc_name        # Pour générer un nouveau nom au document chargé

class ItemTemplate3(ItemTemplate3Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.test_img_just_loaded = False  # pour savoir si l'image vient d'être chargée (voir visu image)
        self.text_box_1.text = self.item['requis_txt']
        
        if self.item['doc1'] is not None:    # Si doc existant
            self.image_1.source = self.item['thumb']              # DIPLAY L'image thumb
            self.button_del.visible = True
            self.button_visu.visible = True
            self.file_loader_1.visible = False
        else:                                 # si doc none
            self.button_del.visible = False 
            self.button_visu.visible = False
            """
            try:     # si pas de doc en table, erreur
                self.button_visu.visible = False
            except:
                pass
            """
        self.stage_num =   self.item['stage_num']        # Row stage
        self.item_requis = self.item['item_requis']      # Row Item requis
        self.email =       self.item['stagiaire_email']  # Row user

    def file_loader_1_change(self, file, **event_args):
        if file is not None:  #pas d'annulation en ouvrant choix de fichier
   
            # nouveau nom doc SANS extension
            new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse 
            print("new file name: ",new_file_name)
            
            # Type de fichier ?
            path_parent, file_name, file_extension = anvil.server.call('path_info', str(file.name))

            
            # sauvegarde du 'file' image en jpg, resized 1000 x 800   ou   800x1000  plus thumnail 150 x 100   ou  100 x 150
            if file_extension == ".jpg" or file_extension == ".jpeg" or file_extension == ".bmp"or file_extension == ".gif" or file_extension == ".jif" or file_extension == ".png":
                self.save_file(file, new_file_name, file_extension)
                    
            if file_extension == ".pdf":      
                # génération du JPG à partir du pdf bg task en bg task
                #liste_images = anvil.server.call('pdf_into_jpg', file, new_file_name)
                self.new_file_name = new_file_name   # pour timer2
                self.task_pdf = anvil.server.call('pdf_into_jpg_bgtasked', file, new_file_name, self.item['stage_num'], self.item['stagiaire_email'])    
                self.timer_2.interval=0.5
                
        self.file_loader_1.visible = False

    def button_visu_click(self, **event_args):
        """This method is called when the button is clicked"""
        # nouveau nom doc
        new_file_name = Pre_R_doc_name.doc_name_creation(self.stage_num, self.item_requis, self.email)   # extension non incluse
        # si doc type jpg ds table
        if self.image_1.source != "":
            self.button_visu.visible = True
            from ...Pre_Visu_img_Pdf import Pre_Visu_img_Pdf  # pour visu du doc
            if self.test_img_just_loaded:   # image vient d'etre chargée et self.item['doc1'] n'est pas à jour, re lecture avant affichage
                row = app_tables.pre_requis_stagiaire.get(stage_num=self.stage_num,
                                                          stagiaire_email=self.email,
                                                          item_requis=self.item_requis)
                if row:
                    open_form('Pre_Visu_img_Pdf', row['doc1'], new_file_name, self.stage_num, self.email, self.item_requis, origine="admin")
            else:  
                open_form('Pre_Visu_img_Pdf', self.item['doc1'], new_file_name, self.stage_num, self.email, self.item_requis, origine="admin")

    def button_del_click(self,  **event_args):
        """This method is called when the button is clicked"""
        result = anvil.server.call('pr_stagiaire_del',self.email, self.stage_num, self.item_requis )
        if result:
            self.image_1.source = None
            self.button_visu.visible = False
            self.button_del.visible = False
            self.file_loader_1.visible = True
        else:
            alert("Pré Requis non enlevé")
            
    def save_file(self, file, new_file_name, file_extension):
        # Sauvegarde du 'file' jpg
        # Avec loading_indicator, appel BG TASK
        self.test_img_just_loaded = True  # indique que l'image, donc self.item['doc1'], a changé
        self.task_img = anvil.server.call('run_bg_task_save_jpg', self.item, file, new_file_name, file_extension)    
        self.timer_1.interval=0.5

    def timer_1_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""

        if self.task_img.is_completed(): # lecture de l'image sauvée en BG task
            print("fin")
            row = app_tables.pre_requis_stagiaire.get(q.fetch_only('thumb'),
                                                        stage_num=self.stage_num,
                                                        item_requis=self.item_requis,
                                                        stagiaire_email=self.email
                                                    )
            
            if row:
                self.image_1.source = row['thumb']
                self.button_visu.visible = True  
                self.button_del.visible = True
            else:
                alert("timer_1_tick: Row stagiaire non trouvé")
                self.button_visu.visible = False  
                self.button_del.visible = False
            self.timer_1.interval=0
            anvil.server.call('task_killer',self.task_img)

    def timer_2_tick(self, **event_args):
        """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
        if self.task_pdf.is_completed(): # lecture de l'image sauvée en BG task
            # lecture de la liste sauvée par bg task ds row du stagiaire_inscrit
            row = app_tables.stagiaires_inscrits.get(q.fetch_only("temp_pr_pdf_img_liste"),
                                                      stage=self.item['stage_num'],
                                                      user_email=self.item['stagiaire_email']
                                                      )
            liste_images=[]
            if row:
                liste_images=row['temp_pr_pdf_img_liste']
                #extraction 1ere image de la liste (il peut y avoir plusieurs pages)
                #print("nb d'images jpg crées par pdf_into_jpg:", len(liste_images))
                file = liste_images[0]
    
                # module de sauvegarde du 'file'  jpg
                self.save_file(file, self.new_file_name, ".jpg")
            else:
                alert('timer_2_tick: row stagiaire inscrit non trouvée')
            
            self.timer_2.interval=0
            anvil.server.call('task_killer',self.task_img)

            

            