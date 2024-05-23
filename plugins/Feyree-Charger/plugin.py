"""
<plugin key="TuyaCharger" name="Tuya Charger Plugin" author="CobraFX" version="1.0" wikilink="https://github.com/YourGithubAccount" externallink="">
    <params>
        <param field="Address" label="IP Address" width="200px" required="true" default="192.168.0.78"/>
        <param field="Mode1" label="Device ID" width="200px" required="true" default="bfc9b828c62aa43667rdug"/>
        <param field="Mode2" label="Local Key" width="200px" required="true" default="zP=pynGe%7IT%_q5"/>
	<param field="Mode3" label="Debug" width="75px">
	    <description><h2>Debugging</h2>Select the desired level of debug messaging</description>
	    <options>
        	<option label="True" value="Debug"/>
	        <option label="False" value="Normal" default="true"/>
   	    </options>
	</param>
    </params>
</plugin>
"""

import Domoticz
import tinytuya
import time

class BasePlugin:

    def __init__(self):

        self.debug = False
        self.ip_address = ""
        self.device_id = ""
        self.local_key = ""
        self.tuya_device = None
        self.levels = [
            {"level": 0, "text": "0A"},
            {"level": 10, "text": "8A"},
            {"level": 20, "text": "10A"},
            {"level": 30, "text": "16A"},
            {"level": 40, "text": "20A"},
            {"level": 50, "text": "25A"},
            {"level": 60, "text": "28A"},
            {"level": 70, "text": "30A"}
        ]
        return

    def onStart(self):
        Domoticz.Log("onStart called")
        self.ip_address = Parameters["Address"]
        self.device_id = Parameters["Mode1"]
        self.local_key = Parameters["Mode2"]

        if Parameters["Mode3"] == "Debug":
            Domoticz.Debug("Debug mode is enabled")
        else:
            Domoticz.Debug("Debug mode is disabled")

        Domoticz.Log("Connecting to Tuya device...")
        self.tuya_device = tinytuya.OutletDevice(self.device_id, self.ip_address, self.local_key)
        self.tuya_device.set_version(3.3)

        Options = {
            "LevelActions": "|*|" * len(self.levels),
            "LevelNames": "|".join([level["text"] for level in self.levels]),
            "LevelOffHidden": "false",
            "SelectorStyle": "0"
        }

        if 1 in Devices:
            # Пристрій вже існує, оновлюємо його
            Devices[1].Update(nValue=Devices[1].nValue, sValue=Devices[1].sValue)
            if Parameters["Mode3"] == "Debug":
                Domoticz.Log("Device Ampers updated.")
        else:
            # Пристрій ще не існує, створюємо його
            Domoticz.Log("Creating device Ampers ...")
            device = Domoticz.Device(Name="Ampers", Unit=1, TypeName="Switch", Switchtype=18, Image=5, Options=Options, Used=1)
            device.Create()
            device.Update(0, "0")

        if 2 in Devices:
            # Пристрій вже існує, оновлюємо його
            Devices[2].Update(nValue=Devices[2].nValue, sValue=Devices[2].sValue)
            if Parameters["Mode3"] == "Debug":
                Domoticz.Log("Device Status updated.")
        else:
            # Пристрій ще не існує, створюємо його
            Domoticz.Log("Creating device Status ...")
            device = Domoticz.Device(Name="Status", Unit=2, TypeName="Text", Used=1)
            device.Create()
            device.Update(0, "Unknown")


        if 3 in Devices:
            Devices[3].Update(nValue=Devices[3].nValue, sValue=Devices[3].sValue)
            if self.debug:
                Domoticz.Log("Device Charge Control updated.")
        else:
            Domoticz.Log("Creating device Charge Control ...")
            device = Domoticz.Device(Name="Charge Control", Unit=3, TypeName="Switch", Image=9, Used=1)
            device.Create()
            device.Update(0, "Off")


    def onStop(self):
        if Parameters["Mode3"] == "Debug":
            Domoticz.Log("onStop called")

    def onHeartbeat(self):
        if Parameters["Mode3"] == "Debug":
            Domoticz.Log("onHeartbeat called")

        data = self.tuya_device.status()
        amper = data['dps'].get('115', 'Unknown')
        status = data['dps'].get('101', 'Unknown')
        current_level = Devices[1].sValue
        level = self.get_level_by_text(str(amper))
        # if Parameters["Mode3"] == "Debug":
        #     Domoticz.Log("Must be Level {}".format(level))
        #     Domoticz.Log("Present Level {}".format(current_level))

        Devices[2].Update(nValue=0, sValue=str(status))

        if current_level != '':

            if int(current_level) != int(level):
                Devices[1].Update(0, str(level))
                Domoticz.Log("Switch Level to {}".format(level))
        else:
                Devices[1].Update(0, str(level))
                Domoticz.Log("Switch Level to {}".format(level))

        if status == 'charing':
            Devices[3].Update(nValue=1, sValue="On")
        else:
            Devices[3].Update(nValue=0, sValue="Off")


    def onCommand(self, Unit, Command, Level, Hue):
        if Parameters["Mode3"] == "Debug":
            Domoticz.Log("onCommand called for Unit {}: Command '{}', Level: {}, Hue: {}".format(Unit, Command, Level, Hue))
        if Unit == 1:
            # Обробка натискання на кнопки
            amper = self.get_amper_by_level(Level)
            self.changeLevelAmper(amper)
            Domoticz.Log("Changed to {}A".format(amper))

        elif Unit == 3:
            if Command == "On":
                self.setCharge(True)
                Devices[3].Update(nValue=1, sValue="On")
            elif Command == "Off":
                self.setCharge(False)
                Devices[3].Update(nValue=0, sValue="Off")


    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        if Parameters["Mode3"] == "Debug":
            Domoticz.Log("onNotification: Name: '{}', Subject: '{}', Text: '{}', Status: {}, Priority: {}, Sound: {}, ImageFile: {}".format(Name, Subject, Text, Status, Priority, Sound, ImageFile))

    def onDisconnect(self):
        if Parameters["Mode3"] == "Debug":
            Domoticz.Log("onDisconnect called")

    def onConnect(self, Connection, Status, Description):
        if Parameters["Mode3"] == "Debug":
            Domoticz.Log("onConnect called")

    def onMessage(self, Connection, Data):
        if Parameters["Mode3"] == "Debug":
            Domoticz.Log("onMessage called")

    def get_amper_by_level(self, level):
        for item in self.levels:
            if item["level"] == level:
                return int(item["text"].rstrip("A"))
        return 0

    def get_level_by_text(self, text):
        for item in self.levels:
            if item["text"] == text + "A":
                return item["level"]
        return 0


    def setCharge(self, charge):
        try:
            data = self.tuya_device.status()
            status = data['dps'].get('101', 'Unknown')

            if charge:
                if status != 'charing':
                    self.tuya_device.set_value(124, "OpenCharging")
                    Domoticz.Log("Started charging")
            else:
                if status == 'charing':
                    self.tuya_device.set_value(124, "CloseCharging")
                    Domoticz.Log("Stopped charging")

        except Exception as e:
            Domoticz.Error(f"Failed to set charge status: {e}")


    def changeLevelAmper(self, Amper):
        data = self.tuya_device.status()
        status = data['dps'].get('101', 'Unknown')
        current_amper = data['dps'].get('115', 'Unknown')
        if current_amper == Amper:
            return
        if status == 'charing':
            # Відправляємо команду зупинки зарядки
            self.tuya_device.set_value(124, "CloseCharging")

            # Очікуємо, поки статус не стане 'WaitOperation'
            while True:
                data = self.tuya_device.status()
                if data['dps']['124'] == "WaitOperation":
                   if Parameters["Mode3"] == "Debug":
                      Domoticz.Log("Статус 'WaitOperation' досягнутий.")
                   break
                else:
                   if Parameters["Mode3"] == "Debug":
                      Domoticz.Log("Поточний статус: {}".format(data['dps']['124']))
                time.sleep(1)

        # Після досягнення 'WaitOperation' відправляємо наступну команду
        self.tuya_device.set_value(115, Amper)

        # Очікуємо, поки статус не стане 'WaitOperation'
        while True:
           data = self.tuya_device.status()
           if data['dps']['115'] == Amper:
             if Parameters["Mode3"] == "Debug":
                Domoticz.Log("Встановлено: {} A".format(Amper))
             Devices[1].Update(nValue=0, sValue=str(Amper))



             break
           else:
             if Parameters["Mode3"] == "Debug":
                Domoticz.Log("Поточний {} A".format(data['dps']['115']))
           time.sleep(1)

        # Очікуємо, поки статус не стане 'charing'
        if status == 'charing':
            while True:
                try:
                    data = self.tuya_device.status()
                    if data['dps']['101'] == "charing":
                       if Parameters["Mode3"] == "Debug":
                          Domoticz.Log("Статус 'charing' досягнутий.")
                       break
                    else:
                       self.tuya_device.set_value(124, "OpenCharging")
                       if Parameters["Mode3"] == "Debug":
                          Domoticz.Log("Поточний статус: {}".format(data['dps']['101']))
                except RuntimeError as error:
                    if Parameters["Mode3"] == "Debug":
                        Domoticz.Error(f"Failed to read status: {error}")

                time.sleep(1)

global _plugin
_plugin = BasePlugin()


def onStart():
    global _plugin
    _plugin.onStart()


def onStop():
    global _plugin
    _plugin.onStop()


def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)


def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

