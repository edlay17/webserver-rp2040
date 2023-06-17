from microdot_asyncio import Microdot, Response, send_file
from microdot_utemplate import render_template
from microdot_asyncio_websocket import with_websocket
from joystick_module import JST
from display_module import DSP
import time

app = Microdot()
Response.default_content_type = 'text/html'

joystick = JST(27, 26, 16)
display = DSP(20, 21)

prevX = 0
prevY = 0
prevB = 0

def checkChanges(xValue, yValue, bValue):
    global prevX
    global prevY
    global prevB
    
    diffX = abs(xValue - prevX)
    diffY = abs(yValue - prevY)
    diffB = abs(bValue - prevB)
    
    isXChanged = diffX > 5000
    isYChanged = diffY > 5000
    isBChanged = diffB > 0
    
    prevX = xValue
    prevY = yValue
    prevB = bValue
    
    return isXChanged or isYChanged or isBChanged

@app.route('/')
async def index(request):
    return render_template('index.html')

@app.route('/ws')
@with_websocket
async def read_sensor(request, ws):
    while True:
        xValue, yValue, bValue = joystick.get_value()
        await ws.send(str(xValue) + "/" + str(yValue) + "/" + str(bValue))
        data = await ws.receive()
        message1, message2 = data.split('///')
        display.show_message(message1, message2);
        sleep(.01)

@app.route("/static/<path:path>")
def static(request, path):
    if ".." in path:
        # directory traversal is not allowed
        return "Not found", 404
    return send_file("static/" + path)

if __name__ == '__main__':
    app.run(debug=True)