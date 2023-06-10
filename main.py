from microdot import Microdot, Response
from microdot_utemplate import render_template
import time

app = Microdot()
Response.default_content_type = 'text/html'

@app.route('/')
def index(request):
    return 'Hello, world!'

@app.route('/orders', methods=['GET'])
def index2(req):
    gamename = "cool game"
    score = ["1000", "2000", "3000"]

    #return 'orders'
    return render_template('game.html', gamename=gamename, score=score)

#@app.route('/ws')
#@with_websocket
#async def read_sensor(request, ws):
#    while True:
        # data = await ws.receive()W
#        time.sleep(.1)
#        await ws.send(str('hello ws'))

if __name__ == '__main__':
    app.run(debug=True)