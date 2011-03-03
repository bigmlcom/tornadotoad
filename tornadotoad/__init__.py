from tornadotoad import my
from tornadotoad import mixin

def register(api_key=None, environment="production", log_403=False, log_404=False, log_405=False):
    """
    Use to register an API key to be used with HoptoadAPI.
    
    Needs to be called early, usually when creating Tornado Application. 
    """
    my.registered = True
    my.api_key = api_key
    my.environment = environment
    my.log_403 = log_403
    my.log_404 = log_404
    my.log_405 = log_405

