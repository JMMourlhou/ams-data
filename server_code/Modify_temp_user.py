import anvil.stripe
import anvil.files
from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# modify the temp of user during qcm (nb of questions)
@anvil.server.callable
def temp_user_qcm(user, nb_questions_in_qcm):
    try:
        user.update(temp = nb_questions_in_qcm)
        result == True
    except:
        result == False
    return

