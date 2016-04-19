from bottle import Bottle, route, run, template, request
import os
import uuid

pi = Bottle()

@pi.route('/switch/<pin:int>/<state:re:(On|Off)>')
def switch(pin=None, state='On'):
    #switch on/off a pin here
    return template('switch_template', pin=pin, state=state)

@pi.route('/send/<pin:int>/<data>')
def send(pin=None, data=''):
    if not pin or not data:
        return template("Fail");
    #Send data through pin here
    return template('send_template', pin=pin, data=data)

@pi.route('/upload', method="GET")
def upload():
    return template('upload_form')

@pi.route('/do_upload', method="POST")
def do_upload():
    upload = request.files.get('upload')
    name, ext = os.path.splitext(upload.filename)
    save_path = "/home/pi/uploads"
    if not os.path.exists(save_path):
        if os.path.exists(os.path.expanduser("~/uploads")):
            save_path = os.path.expanduser("~/uploads")
        else:
            save_path = os.makedirs(os.path.expanduser("~/uploads"))
    i = 1
    while os.path.exists(os.path.join(save_path, upload.filename)):
        upload.filename = upload.filename + str(i)
        i += 1
    upload.save(save_path)

run(pi, host='localhost', port=8080, debug=True, reloader=True)
