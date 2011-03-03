==================
tornadotoad v 0.2
==================

tornadotoad allows one to integrate HoptoadApp.com's service to track exceptions 
inside a tornadoapp.  It can be used outside of a running tornado app, but having
tornado installed is one of the requirements.  If there is an ioloop running, the
request will be asynchronous.

Basic Usage:
------------------

1) Specify the API key and environment. Usually done once before starting up the iolooop.

    import tornadotoad
  
    tornadtoad.register(api_key='your-api-key', environment='production')
  
2) Add the tornadotoad mixin to your RequestHandler.

    import tornadotoad
  
    class BaseHandler(tornadotoad.mixin.RequestHandler, tornado.web.RequestHandler):
        pass

Everytime your application throws an error, the error details will be sent off asynchronously
to Hoptoad.  
