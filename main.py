from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
import time

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
async def index(request):
    return render_template('index.html')

@app.route('/ws')
@with_websocket
async def read_sensor(request, ws):
    while True:
        #data = await ws.receive()
        time.sleep(.1)
        await ws.send(str('hello ws'))

@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)

if __name__ == '__main__':
    app.run(debug=True)