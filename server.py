from flask import Flask, request, render_template
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

PELAAJAT = []
app = Flask(__name__) 

@app.route('/')
def aula():
	return render_template('aula.html')

@app.route('/peli.html')
def peli():
	return render_template('peli.html')

@app.route('/api')
def api():
	if request.environ.get('wsgi.websocket'):
		ws = request.environ['wsgi.websocket'] 
		PELAAJAT.append(ws)
		while True:
			message = ws.receive()
			for websocket in PELAAJAT: 
				try :
					websocket.send(message)
				except :
					# yhteys on katkennut
					PELAAJAT.remove(websocket)
	return

app.debug = False

if __name__ == '__main__':
	http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
	http_server.serve_forever()
