from flask import Flask, request, render_template, views
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer


PELAAJAT = []
app = Flask(__name__) 


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
					# connection lost
					PELAAJAT.remove(websocket)
	return

class Aula(views.MethodView):
	def get(self):
		return render_template('aula.html')

class Peli(views.MethodView):
	def get(self):
		return render_template('peli.html')

app.add_url_rule('/', view_func=Aula.as_view('index'))
app.add_url_rule('/peli.html', view_func=Peli.as_view('main'))
app.debug = False

if __name__ == '__main__':

	http_server = WSGIServer(('',5000), app, handler_class=WebSocketHandler)
	http_server.serve_forever()
