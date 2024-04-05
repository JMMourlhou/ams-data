#import anvil.files
#from anvil.files import data_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

@anvil.server.callable
def search_on_name_only(c_nom):
    liste = app_tables.users.search(
                                        q.fetch_only("nom","prenom","email","tel","role"),
                                        tables.order_by("nom", ascending=True),
                                        q.all_of                  # all of queries must match
                                        (
                                            #role   = q.ilike(c_role),   # ET
                                            nom    = q.ilike(c_nom),    # ET
                                            #role =q.not_("A")   # on n'affiche pas l'admin !                 
                                        )
                                    )
    return liste