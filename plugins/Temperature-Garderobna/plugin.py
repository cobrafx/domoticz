"""
<plugin key="Temperature-Garderobna" name="Temperature-Garderobna" author="CobraFX" version="1.0" wikilink="https://github.com/domoticz/domoticz/wiki/Developing-A-Python-Plugin">
    <description>
        <h2>Temperature-Garderobna Plugin</h2><br/>
        This plugin reads data from Temperature Garderobna
    </description>
    <params>
        <param field="Mode1" label="Device Name" width="200px" required="true" default="Температура у гардеробній"/>
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
import re
import serial
import time
import codecs

class BasePlugin:
    def __init__(self):
        self.serial_port = "/dev/ttyUSB0"
        self.serial_connection = None
        self.device_name = ""
        self.debug = False
        self.interval = 20  # Інтервал моніторингу у секундах (20 секунд)
        self.last_update_time = 0

    def createDevice(self):
        if 1 not in Devices:
            Domoticz.Log("Creating new device...")
            device = Domoticz.Device(Name=self.device_name, Unit=1, TypeName="Temp+Hum", Used=1)
            device.Create()
            device.Update(nValue=0, sValue="0;0;0")

    def onStart(self):
        self.device_name = Parameters["Mode1"]
        self.debug = Parameters["Mode2"] == "Debug"
        self.createDevice()
        Domoticz.Heartbeat(int(self.interval / 60))  # Переводимо секунди у хвилини

    def onHeartbeat(self):
        if time.time() - self.last_update_time >= self.interval:
            self.readSensorData()
            self.last_update_time = time.time()

    def readSensorData(self):
        try:
            self.serial_connection = serial.Serial(self.serial_port, 9600, timeout=1)
            data = self.serial_connection.readline()

            if data:
                try:
                    decoded_data = data.decode("utf-8")
                except UnicodeDecodeError:
                    decoded_data = codecs.decode(data, 'latin-1', errors='replace')
                    if self.debug:
                        Domoticz.Error("Failed to decode using UTF-8, using Latin-1 instead")

                humidity_match = re.search(r'Влажность: (\d{2}\.\d{2})', decoded_data)
                temperature_match = re.search(r'Температура: (\d{2}\.\d{2})', decoded_data)

                if humidity_match and temperature_match:
                    humidity = float(humidity_match.group(1))
                    temperature = float(temperature_match.group(1))

                    if self.debug:
                        Domoticz.Log(f"Humidity: {humidity}%")
                        Domoticz.Log(f"Temperature: {temperature}°C")

                    Devices[1].Update(nValue=0, sValue=f"{temperature};{humidity};0")

        except serial.SerialException as e:
            Domoticz.Error(f"Failed to open serial port: {e}")

        finally:
            if self.serial_connection:
                self.serial_connection.close()

    def onStop(self):
        if self.debug:
            Domoticz.Log("onStop called")
        if self.serial_connection:
            self.serial_connection.close()

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()