==================
tornadotoad v 0.3
==================

tornadotoad allows one to integrate HoptoadApp.com's service to track exceptions 
inside a tornadoapp.  It can be used outside of a running tornado app, but having
tornado installed is one of the requirements.  If there is an ioloop running, the
request will be asynchronous.

Basic Usage:
------------------

1) Specify the API key and environment. Usually done once before starting up the iolooop.

    import tornadotoad
    tornadotoad.register(api_key='your-api-key', environment='production')
  
2) Add the tornadotoad mixin to your RequestHandler.

    import tornadotoad
    class BaseHandler(tornadotoad.mixin.RequestHandler, tornado.web.RequestHandler):
        pass

Everytime your application throws an error, the error details will be sent off asynchronously
to Hoptoad.  


Send deploy notification
------------------

When hoptoad receives a deploy notification, it will clear all the errors for the environment
you have registered. 

    import tornadotoad
    tornadotoad.register(api_key='your-api-key', environment='production')
    client = tornadotoad.api.TornadoToad()
    client.deploy()

