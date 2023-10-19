from anvil_extras.messaging import Publisher
publisher = Publisher()

"""
From Anvil extras

This library provides a mechanism for forms (and other components)
within an Anvil app to communicate in a 'fire and forget' manner.
It's an alternative to raising and handling events,
 instead you 'publish' messages to a channel and, from anywhere else,
 you subscribe to that channel and process those messages as required.

1-  this module must be imported in my app's startup module/form  'from .. import common'
-----------------------------------------------------------
Then, 
2- From anywhere in my app, I can import the publisher and publish messages to a channel.
  
from .common import publisher
...
...
    def __init__(self, **properties):
        publisher.publish(channel="general", title="Hello world")
        self.init_components(**properties)

The publish method also has an optional 'content' parameter which can be passed any object.

--------------------------------------------------------------------------------
3- On any form, I can subscribe to the 'general' channel and print any 'Hello world' messages:

from .common import publisher
...
...

    def __init__(self, **properties):
        publisher.subscribe(
            channel="general", subscriber=self, handler=self.general_messages_handler
        )
        self.init_components(**properties)



    def general_messages_handler(self, message):
        if message.title == "Hello world":
            print(message.title)


"""