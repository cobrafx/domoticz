"""
<plugin key="Tongou" name="Tongou" author="CobraFX" version="1.0" wikilink="https://github.com/domoticz/domoticz/wiki">
    <description>
        <h2>Tongou Plugin</h2><br/>
        This plugin reads data by mqtt from Tongou
    </description>
    <params>
        <param field="Address" label="MQTT Broker Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="MQTT Broker Port" width="75px" required="true" default="1883"/>
        <param field="Mode1" label="MQTT zigbee2mqtt Topic" width="300px" required="true" default="Бойлер"/>
        <param field="Mode2" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import json
import paho.mqtt.client as mqtt
import time
import datetime


class BasePlugin:
    enabled = False

    def __init__(self):
        self.mqttClient = None
        self.topic = None

    def onStart(self):
        Domoticz.Debug("onStart called")

        if "Mode1" in Parameters:
            self.topic = 'zigbee2mqtt/' +  Parameters["Mode1"]
        else:
            Domoticz.Error("Topic parameter not found in Parameters")
            return
        
        broker_address = Parameters["Address"]
        broker_port = int(Parameters["Port"])

        self.mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.mqttClient.on_connect = self.onConnect
        self.mqttClient.on_message = self.onMessage
        # self.mqttClient.username_pw_set('', '')

        #try:
         #   self.mqttClient.connect(broker_address, broker_port, 60)
            #self.mqttClient.loop_start()
        #except Exception as e:
        #    Domoticz.Error("Unable to connect to MQTT broker: " + str(e))
        
        Domoticz.Heartbeat(10)

        if len(Devices) == 0:
            Domoticz.Device(Name="Current", Unit=1, Type=243, Subtype=23).Create()
            Domoticz.Device(Name="Energy", Unit=2, Type=248, Subtype=1).Create()
            Domoticz.Device(Name="State", Unit=3, Type=244, Subtype=73).Create()
            Domoticz.Device(Name="Voltage", Unit=4, Type=243, Subtype=8).Create()

    def onConnect(self, client, userdata, flags, rc):
        if rc == 0:
            Domoticz.Debug("Connected successfully to MQTT broker")
            self.mqttClient.subscribe(self.topic + "/#")
            Domoticz.Debug("Subscribe to: " + str(self.topic))
        else:
            Domoticz.Error("Failed to connect to MQTT broker, return code " + str(rc))

    def onMessage(self, client, userdata, message):
        try:
            message_content = message.payload.decode("utf-8")
            Domoticz.Debug("onMessage called: " + message_content)
            data = json.loads(message_content)
            if 'current' in data:
                UpdateDevice(1, 0, str(data['current']))
            if 'energy' in data:
                UpdateDevice(2, 0, str(data['energy'] * 1000))
            if 'state' in data:
                state = 1 if data['state'] == 'ON' else 0
                UpdateDevice(3, state, data['state'])
            if 'voltage' in data:
                UpdateDevice(4, 0, str(data['voltage']))
        except Exception as e:
            Domoticz.Error("Error parsing MQTT message: " + str(e))

    def onDisconnect(self):
        Domoticz.Debug("onDisconnect called")
        self.mqttClient.loop_stop()

    def onCommand(self, Unit, Command, Level, Color):
        Domoticz.Debug("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "'")
        if Unit == 3:  # Device "State"
            if Command == "On":
                self.mqttClient.publish(self.topic + "/set", json.dumps({"state": "ON"}))
                UpdateDevice(3, 1, "On")
            elif Command == "Off":
                self.mqttClient.publish(self.topic + "/set", json.dumps({"state": "OFF"}))
                UpdateDevice(3, 0, "Off")

    def onHeartbeat(self):
        if not self.mqttClient.is_connected():
            Domoticz.Log("Attempting MQTT reconnection...")
            try:
                self.mqttClient.connect(Parameters["Address"], int(Parameters["Port"]))
                self.mqttClient.loop_start()
            except Exception as e:
                Domoticz.Error(f"Failed to reconnect to MQTT server: {e}")
        else:
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.mqttClient.publish(str(self.topic) + "/keep_alive", json.dumps({"time": str(current_time)}))


#        if self.mqttClient is not None and not self.mqttClient.is_connected():
#            Domoticz.Debug("Reconnecting to MQTT broker")
#            self.mqttClient.reconnect()

def UpdateDevice(Unit, nValue, sValue):
    if Unit in Devices:
        if Devices[Unit].nValue != nValue or Devices[Unit].sValue != sValue:
            Devices[Unit].Update(nValue, sValue)
            Domoticz.Log("Updated device: " + str(Unit) + " with nValue: " + str(nValue) + " and sValue: " + sValue)
    return

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onDisconnect()

def onConnect(Connection, Status, Description):
    pass

def onMessage(Topic, Message):
    global _plugin
    _plugin.onMessage(Topic, Message)

def onCommand(Unit, Command, Level, Color):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Color)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

