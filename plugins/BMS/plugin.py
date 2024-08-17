"""
<plugin key="BMS" name="BMS" author="CobraFX" version="1.0" wikilink="https://github.com/domoticz/domoticz/wiki/Developing-A-Python-Plugin">
    <description>
        <h2>BMS JK Plugin</h2><br/>
        This plugin reads data from BMS JK.
    </description>
    <params>
        <param field="Address" label="MQTT Server Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="MQTT Server Port" width="30px" required="true" default="1883"/>
        <param field="Username" label="MQTT Username" width="200px" required="false" default=""/>
        <param field="Password" label="MQTT Password" width="200px" required="false" default=""/>
        <param field="Mode1" label="Debug" width="75px">
            <options>
                <option label="True" value="True"/>
                <option label="False" value="False" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""


import Domoticz
import paho.mqtt.client as mqtt
import time
import datetime

class BasePlugin:

    def __init__(self):
        self.mqttClient = None
        self.debug = False
        self.update_attempts = {}

    def onStart(self):
        Domoticz.Log("onStart called")
        self.debug = Parameters["Mode1"] == "True"
        self.mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.mqttClient.on_connect = self.onConnect
        self.mqttClient.on_message = self.onMessage
        self.mqttClient.username_pw_set(Parameters["Username"], Parameters["Password"])
        # self.mqttClient.connect(Parameters["Address"], int(Parameters["Port"]))
        # self.mqttClient.loop_start()


        device_info = {
            1: ("Bank 1 Voltage", "Voltage"),
            2: ("Bank 2 Voltage", "Voltage"),
            3: ("Bank 3 Voltage", "Voltage"),
            4: ("Bank 4 Voltage", "Voltage"),
            5: ("Bank 5 Voltage", "Voltage"),
            6: ("Bank 6 Voltage", "Voltage"),
            7: ("Bank 7 Voltage", "Voltage"),
            8: ("Bank 8 Voltage", "Voltage"),
            9: ("Bank 9 Voltage", "Voltage"),
            10: ("Bank 10 Voltage", "Voltage"),
            11: ("Bank 11 Voltage", "Voltage"),
            12: ("Bank 12 Voltage", "Voltage"),
            13: ("Bank 13 Voltage", "Voltage"),
            14: ("Bank 14 Voltage", "Voltage"),
            15: ("Bank 15 Voltage", "Voltage"),
            16: ("Bank 16 Voltage", "Voltage"),
            17: ("Battery SoC", "General", 6),
            18: ("Voltage Delta", "Voltage"),
            19: ("Battery Current", "General", 23),
            20: ("Temperature 0", "Temp", 5),
            21: ("Temperature 1", "Temp", 5),
            22: ("Temperature 2", "Temp", 5),
            23: ("Cycle Capacity", "Custom", 31, {'Custom': '1;Ah'}),
            24: ("Battery Cycles", "General", 28, {}, 3),
            25: ("Charge", "Switch", 2),
            26: ("DisCharge", "Switch", 2),
            27: ("Bank Min Voltage", "Voltage"),
            28: ("Bank Max Voltage", "Voltage"),
            29: ("Total Battery Voltage", "Voltage")
        }

        for unit, device_info_tuple in device_info.items():
            name, type_name = device_info_tuple[:2]
            subtype = device_info_tuple[2] if len(device_info_tuple) > 2 else None
            options = device_info_tuple[3] if len(device_info_tuple) > 3 else None
            switchtype = device_info_tuple[4] if len(device_info_tuple) > 4 else None
            icon_index = device_info_tuple[5] if len(device_info_tuple) > 5 else None

            if unit not in Devices:
                Domoticz.Log(f"Creating device {name} ...")
                if subtype is not None:
                    if options is not None:
                        device = Domoticz.Device(Name=name, Unit=unit, TypeName=type_name, Subtype=subtype, Options=options, Used=1)

                        if switchtype is not None:
                            device = Domoticz.Device(Name=name, Unit=unit, TypeName=type_name, Subtype=subtype, Switchtype=switchtype, Options=options, Used=1)

                        if icon_index is not None:
                            device = Domoticz.Device(Name=name, Unit=unit, TypeName=type_name, Subtype=subtype, Switchtype=switchtype, Options=options, Image=icon_index,  Used=1)
                    else:
                        device = Domoticz.Device(Name=name, Unit=unit, TypeName=type_name, Subtype=subtype, Used=1)
                else:
                    if options is not None:
                        device = Domoticz.Device(Name=name, Unit=unit, TypeName=type_name, Options=options, Used=1)
                    else:
                        device = Domoticz.Device(Name=name, Unit=unit, TypeName=type_name, Used=1)
                device.Create()
                device.Update(nValue=0, sValue="0");
            else:
                Domoticz.Log(f"Device {name} already exists")
                Devices[unit].Update(nValue=Devices[unit].nValue, sValue=Devices[unit].sValue);

    def onStop(self):
        Domoticz.Log("onStop called")
        self.mqttClient.loop_stop()

    def onConnect(self, client, userdata, flags, rc):
        Domoticz.Log("Connected to MQTT with result code "+str(rc))
        self.mqttClient.subscribe("BMS_1/#")

    def onMessage(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")

        device_mapping = {
            "BMS_1/Vbank0": 1,
            "BMS_1/Vbank1": 2,
            "BMS_1/Vbank2": 3,
            "BMS_1/Vbank3": 4,
            "BMS_1/Vbank4": 5,
            "BMS_1/Vbank5": 6,
            "BMS_1/Vbank6": 7,
            "BMS_1/Vbank7": 8,
            "BMS_1/Vbank8": 9,
            "BMS_1/Vbank9": 10,
            "BMS_1/Vbank10": 11,
            "BMS_1/Vbank11": 12,
            "BMS_1/Vbank12": 13,
            "BMS_1/Vbank13": 14,
            "BMS_1/Vbank14": 15,
            "BMS_1/Vbank15": 16,
            "BMS_1/RSOC": 17,
            "BMS_1/Vdelta": 18,
            "BMS_1/Abat": 19,
            "BMS_1/Temp0": 20,
            "BMS_1/Temp1": 21,
            "BMS_1/Temp2": 22,
            "BMS_1/AhCycl": 23,
            "BMS_1/NumbCycl": 24,
            "BMS_1/MOS_chrg_stat": 25,
            "BMS_1/MOS_Dischrg_stat": 26,
            "BMS_1/Vmin": 27,
            "BMS_1/Vmax": 28
        }

        if topic in device_mapping:
            unit = device_mapping[topic]
            value = float(payload)
            message = f"Received {Devices[unit].Name}: {value}"
            if self.debug:
                Domoticz.Log(message)

            current_nValue = Devices[unit].nValue
            current_sValue = Devices[unit].sValue

            if current_sValue != str(value):

                if Devices[unit].Type == 243:
                    if Devices[unit].SubType == 31:
                        options = str(Devices[unit].Options)
                        if options == "{'Custom': '1;Ah'}":
                            Devices[unit].Update(nValue=0, sValue=str(value) + ";Ah")
                        else:
                            Devices[unit].Update(nValue=0, sValue=str(value))
                    else:
                         Devices[unit].Update(nValue=0, sValue=str(value))

                elif Devices[unit].Type == 244:
                        Devices[unit].Update(nValue=int(value), sValue=str(value))

                else:
                    Devices[unit].Update(nValue=0, sValue=str(value))

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
            self.mqttClient.publish("BMS_1/keep_alive", current_time)

        total_value = 0.0

        for unit in range(1, 17):  # Прохід по Unit від 1 до 16 включно
            if unit in Devices:  # Перевіряємо, чи пристрій існує
                try:
                    value = float(Devices[unit].sValue)  # Перетворюємо значення на float
                    total_value += value
                except ValueError:
                    Domoticz.Error(f"Cannot convert sValue of device with Unit {unit} to float")

        # Заокруглюємо до другого знака після коми
        total_value = round(total_value, 2)

        Devices[29].Update(nValue=0, sValue=str(total_value))





global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(client, userdata, flags, rc):
    global _plugin
    _plugin.onConnect(client, userdata, flags, rc)

def onMessage(client, userdata, msg):
    global _plugin
    _plugin.onMessage(client, userdata, msg)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()
