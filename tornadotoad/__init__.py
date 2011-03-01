from tornadotoad import my
from tornadotoad import mixin

def register(api_key=None, environment="production"):
    """
    Use to register an API key to be used with HoptoadAPI.
    
    Needs to be called early, usually when creating Tornado Application. 
    """
    my.registered = True
    my.api_key = api_key
    my.environment = environment

