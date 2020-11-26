"""

HR20 mqtt gateway

"""

import eventlet
import json
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO

import sqlite3
import datetime
import time
import sys
import threading
import logging

lock = threading.Lock()

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECRET'] = ''
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = '192.168.188.22'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = 'openhabian'
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'home/hass/hr20'
app.config['MQTT_LAST_WILL_MESSAGE'] = ''
app.config['MQTT_LAST_WILL_QOS'] = 2

HR20_TEMP_TOPIC = 'haus/+/hr20/temp'
HR20_MODE_TOPIC = 'haus/+/hr20/mode'

DB_FILE = '/config/db/openhr20.sqlite'

# Parameters for SSL enabled
# app.config['MQTT_BROKER_PORT'] = 8883
# app.config['MQTT_TLS_ENABLED'] = True
# app.config['MQTT_TLS_INSECURE'] = True
# app.config['MQTT_TLS_CA_CERTS'] = 'ca.crt'

mqtt = Mqtt(app)
socketio = SocketIO(app)
logger = logging.getLogger('mqttlistener')

address = {}
address['saal'] = 1
address['vraum'] = 2
address['k_stuuv'] = 3
address['kabuff'] = 4
address['wc1'] = 5
address['wc2'] = 6
address['kueche'] = 7
address['g_stuuv_1'] = 8
address['g_stuuv_2'] = 9
address['eingang'] = 10
address['gr_zimmer'] = 11
address['zimmer_m_1'] = 12
address['zimmer_m_2'] = 13
address['studio'] = 14
address['wc3'] = 15
address['h_verein_1'] = 16
address['h_verein_2'] = 17
address['musik'] = 18
address['wc4'] = 19
address['heizung'] = 20
address['fwh'] = 21

def execute_command(addr, data):
  with lock:
    logger.warning("Executing command: " + str(addr) + " " + data)
    try:
      dt = datetime.datetime.now()
      timestamp = int(time.mktime(dt.timetuple()))
      conn = sqlite3.connect(DB_FILE)
      conn.execute("INSERT INTO command_queue (time,addr,data) VALUES (?, ?, ?)", (timestamp, addr, data))
      conn.commit()
    except:
      logger.error('unable to execute command: ' + str(addr) + " " + data)
    finally:
      conn.close()
    logger.warning("Done executing command: " + str(addr) + " " + data)


def set_temperature(addr, temp):
    temp = int(2*float(temp))
    command = "A%0.2x" % (temp)
    execute_command(addr, command)

    
def set_mode(addr, mode):
    if mode == 'MANU':
        execute_command(addr, "M00")
    if mode=='AUTO':
        execute_command(addr, "M01")

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=message.payload.decode(),
        qos=message.qos,
    )
    print(data['topic'] + ": " + data['payload'])
    device = data['topic'].split('/')[1]
    command = data['topic'].split('/')[3]

    if device in address:
        dev_address = address[device]
        
        if (command == "temp"):
            temp = data['payload']
            logger.info("Change wanted temperature on " + device + ": ", temp)
            set_temperature(dev_address, temp)
            
        if (command == "mode"):
            mode = data['payload']
            logger.info("Change mode on " + device + ": ", mode)
            set_mode(dev_address, mode)
    else:
        logger.error("Unknown device address: " + device)


@mqtt.on_log()
def handle_logging(client, userdata, level, buf):
    print(level, buf)


if __name__ == '__main__':
    mqtt.subscribe(HR20_TEMP_TOPIC, 2)
    mqtt.subscribe(HR20_MODE_TOPIC, 2)
    socketio.run(app, host='0.0.0.0', port=5000)

