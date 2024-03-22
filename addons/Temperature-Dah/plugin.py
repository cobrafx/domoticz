"""
<plugin key="Temperature-Dah" name="Temperature-Dah" author="CobraFX" version="1.0">
    <description>
        <h2>DHT22 Temperature/Humidity Dah Plugin</h2><br/>
        This plugin reads data from DHT22 sensor and sends it to Domoticz.
    </description>
    <params>
        <param field="Mode1" label="GPIO Pin" width="100px" required="true" default="17"/>
        <param field="Mode2" label="Device Name" width="200px" required="true" default="Температура під дахом"/>
        <param field="Mode4" label="Debug" width="75px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""

import Domoticz
import adafruit_dht
import board
import threading
import time

class DHT22Plugin:
    def __init__(self):
        self.pin = 17
        self.device_name = ""
        self.debug = False
        self.interval = 20
        self.monitor_thread = None

    def onStart(self):
        if self.debug:
            Domoticz.Log("DHT22 Plugin onStart called")
        self.pin = int(Parameters["Mode1"])
        self.device_name = Parameters["Mode2"]
        self.debug = Parameters["Mode4"] == "Debug"
        self.createDevice()
        self.startMonitoring()

    def onStop(self):
        if self.debug:
            Domoticz.Log("DHT22 Plugin onStop called")
        self.stopMonitoring()

    def createDevice(self):
        if 1 not in Devices:
            Domoticz.Log("Creating new device...")
            Domoticz.Device(Name=self.device_name, Unit=1, TypeName="Temp+Hum", Used=1).Create()

    def startMonitoring(self):
        self.monitor_thread = threading.Thread(target=self.monitorSensor)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stopMonitoring(self):
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join()

    def monitorSensor(self):
        while True:
            self.readSensorData()
            if self.debug:
                Domoticz.Log("Waiting for next reading...")
            time.sleep(self.interval)

    def readSensorData(self):
        dhtDevice = adafruit_dht.DHT22(getattr(board, f"D{self.pin}"))

        try:
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity

            if self.debug:
                Domoticz.Log(f"Temperature: {temperature}°C, Humidity: {humidity}%")

            self.updateDevice(temperature, humidity)
        except RuntimeError as error:
            if self.debug:
                Domoticz.Error(f"Failed to read data from DHT22 sensor: {error}")
        finally:
            dhtDevice.exit()

    def updateDevice(self, temperature, humidity):
        Devices[1].Update(nValue=0, sValue=f"{temperature};{humidity};0")

global _plugin
_plugin = DHT22Plugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()
