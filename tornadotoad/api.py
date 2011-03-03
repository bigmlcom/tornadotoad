import sys
import traceback
from xml.etree.ElementTree import ElementTree, Element, SubElement, tostring

import tornado.httpclient
import tornado.ioloop

from tornadotoad import my

class TornadoToad(object):
    endpoint = "http://hoptoadapp.com/notifier_api/v2/"
    api_version = "2.0"
    notifier_name = "TornadoToad"
    notifier_version = "0.2"
    notifier_url = "http://github.com/ephramzerb/tornadotoad"

    def post_notice(self, exception, request=None):
        """
        Uses a globally accessible IOloop (created by a started Tornado App) to 
        post the message to hoptoad asynchronously.  If not present, posts synchronously.
        """
        if not my.registered:
            return False
        self._send("notices", body=self._build_notice_body(exception, request=request))
            
    def clear_all_errors(self, exception):
        pass
    
    def _build_notice_body(self, exception, request=None):
        root = Element('notice', {'version' : self.api_version})
        api_key = SubElement(root, "api-key")
        api_key.text = my.api_key
        
        # notifier, notifier/name, notifier/version, notifier/url
        notifier = SubElement(root, "notifier")
        notifier_name = SubElement(notifier, "name")
        notifier_name.text = self.notifier_name
        notifier_version = SubElement(notifier, "version")
        notifier_version.text = self.notifier_version
        notifier_url = SubElement(notifier, "url")
        notifier_url.text = self.notifier_url
        
        # error
        error = SubElement(root, "error")
        error_class = SubElement(error, "class")
        error_class.text = exception.__class__.__name__
        
        # error/message
        error_message = SubElement(error, "message")
        error_message.text = '%s: %s' % (exception.__class__.__name__, str(exception))
        
        # error/backtrace
        backtrace = SubElement(error, "backtrace")
        _type, _value, tb = sys.exc_info()
        tracebacks = traceback.extract_tb(tb)
        tracebacks.reverse()
        for tb in tracebacks:
            file_name, number, method, _  = tb
            line = SubElement(backtrace, "line", {'number' : str(number), 'method' : method, 'file' : file_name })

        # request (optional)
        request_el = self._build_request_el(request) if request else None
        if request_el:
            root.append(request_el)

        # server-environment
        server_environment = SubElement(root, "server-environment")
        environment = SubElement(server_environment, "environment-name")
        environment.text = my.environment
        
        return '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, 'utf-8')        
    
    def _build_request_el(self, request):
        """
        Returns an xml element to be inserted into XML request.
        """
        # make sure we have all the requisite pieces.
        if 'url' not in request and 'component' not in request:
            return False
                
        # request
        request_el = Element("request")
        url = SubElement(request_el, "url")
        url.text = request['url']
        
        # request/component
        component = SubElement(request_el, "component")
        component.text = request['component']

        # request/cgi-data/var
        if 'cgi-data' in request and len(request['cgi-data'].keys()) > 0:            
            cgi_data = SubElement(request_el, "cgi-data")        
            for key in request['cgi-data'].keys():
                # don't send cookie data, for now.
                if key not in ['Cookie']:
                    key_el = SubElement(cgi_data, "var", {'key' : key})
                    key_el.text = request['cgi-data'][key]
        
        # request/params/var
        if 'params' in request and len(request['params'].keys()) > 0:            
            params = SubElement(request_el, "params")
            for key in request['params'].keys():
                key_el = SubElement(params, "var", {'key' : key})
                key_el.text = str(request['params'][key])

        return request_el
        
    def _send(self, path, body=None):
        url = self.endpoint + path
        headers = { 'Content-Type': 'text/xml' }
        request = tornado.httpclient.HTTPRequest(url=url, method="POST", body=body, headers=headers)
        if tornado.ioloop.IOLoop.initialized():
            http = tornado.httpclient.AsyncHTTPClient()
            http.fetch(request, self._done)
        else:
            http = tornado.httpclient.HTTPClient()
            http.fetch(request)
        
    def _done(self, response):
        pass
