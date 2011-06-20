import tornado

from tornadotoad import api
from tornadotoad import my

class RequestHandler(object):
    """Mix in functionality for tornado tornado.web.RequestHandler objects
    to override exception handling.
    
    You probably have a modified tornado.web.RequestHandler that you use as
    the base class for all your request handlers.  Just include this class
    and you're all set.
    
    example:
        class BaseHandler(tornadotoad.mixin.RequestHandler, tornado.web.RequestHandler):
    """
    def send_error(self, status_code, **kwargs):
        if status_code == 403 and my.log_403 == False:
            return super(RequestHandler, self).send_error(status_code, **kwargs)
        
        if status_code == 404 and my.log_404 == False:
            return super(RequestHandler, self).send_error(status_code, **kwargs)
                
        if status_code == 405 and my.log_405 == False:
            return super(RequestHandler, self).send_error(status_code, **kwargs)
    
        tornado_toad = api.TornadoToad()
        exception = kwargs['exception'] if 'exception' in kwargs else None
        if exception:
            tornado_toad.post_notice(exception, request=self._td_build_request_dict())
        return super(RequestHandler, self).send_error(status_code, **kwargs)
    
    def _td_build_request_dict(self):
        """Build a dict with request details to pass along to TornadoToad for
        logging.
        
        Flattens request arguments into a comma-seperated string.
        """
        formatted_arguments = {}
        for key in self.request.arguments.keys():
            formatted_arguments[key] = ','.join(self.request.arguments[key])
        return {
            'url' : self.request.full_url(),
            'component' : self.__class__.__name__,
            'cgi-data' : self.request.headers,
            'params' : formatted_arguments,
        }


def catcher(original, *args, **kwargs):
    """A decorator to intercept exception in arbitrary functions and pass
    along to Hoptoad.
    
    This is good for stand-alone scripts or something like celery tasks -
    so you can log the exceptions in the same manner as your web application.
    """
    def wrapped_in_exceptions(*args, **kwargs):
        try:
            original(*args, **kwargs)
        except Exception, e:
            tornado_toad = api.TornadoToad()
            tornado_toad.post_notice(e)
    wrapped_in_exceptions.__name__ = original.__name__
    wrapped_in_exceptions.__dict__ = original.__dict__
    wrapped_in_exceptions.__doc__ = original.__doc__
    return wrapped_in_exceptions