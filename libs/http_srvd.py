import eventlet
from eventlet import wsgi
from eventlet import websocket
from eventlet.support import six

# demo app
import os
import random


@websocket.WebSocketWSGI
def handle(ws):
    """  This is the websocket handler function.  Note that we
    can dispatch based on path in here, too."""

    if ws.path == '/echo':
        while True:
            m = ws.wait()
            if m is None:
                break
            ws.send(m)

    elif ws.path == '/data':
        for i in six.moves.range(10000):
            ws.send("0 %s %s\n" % (i, random.random()))
            eventlet.sleep(0.1)
    else:
        ws.send("helo world !")


def dispatch(environ, start_response):
    """ This resolves to the web page or the websocket depending on
    the path."""
    #print environ

    if environ['PATH_INFO'] in ['/data']:
        return handle(environ, start_response)
    elif environ['PATH_INFO'] == '/echo':
        start_response('200 OK', [('content-type', 'text/html')])
        return str(environ)
    else:
        return ""
        start_response('200 OK', [('content-type', 'text/html')])
        return [open(os.path.join(
                     os.path.dirname(__file__),
                     'websocket.html')).read()]

if __name__ == "__main__":
    # run an example app from the command line
    listener = eventlet.listen(('127.0.0.1', 1982))
    print("\nVisit http://localhost:7000/ in your websocket-capable browser.\n")
    wsgi.server(listener, dispatch)