from ._anvil_designer import plotTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import stripe.checkout
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

from plotly import graph_objects as go

class plot(plotTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
       

        # Plot some data
        self.plot_1.data = [
        go.Scatter(
                    x = [1, 2, 3],
                    y = [3, 1, 6],
                    marker = dict(
                                     color= 'rgb(16, 32, 77)'
                                 )
                ),
        go.Bar(
            x = [1, 2, 3],
            y = [3, 1, 6],
            name = 'Bar Chart Example'
        )
        ]
    
        # Configure the plot layout
        self.plot_1.layout = {
                                'title': 'Simple Example',
                                'xaxis':    {
                                                'title': 'time'
                                            }
                            }
        self.plot_1.layout.yaxis.title = 'carbon emissions'
        self.plot_1.layout.annotations = [
                                             dict(
                                                    text = 'Simple annotation',
                                                    x = 0,
                                                    xref = 'paper',
                                                    y = 0,
                                                    yref = 'paper'
                                                 )
                                        ]