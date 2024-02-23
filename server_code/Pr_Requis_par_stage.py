
import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server


@anvil.server.callable           #modif du dico pré_requis pour un stage
@anvil.tables.in_transaction
def modif_pre_requis_codes_stages(code_stage, pr_requis_dico):

    
    valid=""
    # lecture fichier père stages
    stage_r = app_tables.codes_stages.get(code=code_stage)
    if not stage_r :
        valid="Stage non trouvé ds table codes_stages !"
    else:
        stage_r.update(pre_requis=pr_requis_dico)
        valid="Stage mis à jour"
    return valid
