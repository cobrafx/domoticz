"""
<plugin key="Powmr" name="Powmr" author="CobraFX" version="1.0" wikilink="https://github.com/domoticz/domoticz/wiki/Developing-A-Python-Plugin">
    <description>
        <h2>Powmr Plugin</h2><br/>
        This plugin reads data from inverter Powmr.
    </description>
    <params>
        <param field="Mode1" label="MQTT Server Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Mode2" label="MQTT Server Port" width="30px" required="true" default="1883"/>
        <param field="Username" label="MQTT Username" width="200px" required="false" default=""/>
        <param field="Password" label="MQTT Password" width="200px" required="false" default=""/>
        <param field="Mode3" label="Debug" width="75px">
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

class BasePlugin:

    def __init__(self):
        self.mqttClient = None
        self.debug = False
        self.levels = [
            {"level": 0, "text": "Uknown"},
            {"level": 10, "text": "Power On"},
            {"level": 20, "text": "Standby"},
            {"level": 30, "text": "Mains"},
            {"level": 40, "text": "Off-Grid"},
            {"level": 50, "text": "Bypass"},
            {"level": 60, "text": "Charging"},
            {"level": 70, "text": "Fault"}
        ]
        self.update_attempts = {}

    def onStart(self):
        Domoticz.Log("onStart called")
        self.debug = Parameters["Mode3"] == "True"
        self.mqttClient = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        self.mqttClient.on_connect = self.onConnect
        self.mqttClient.on_message = self.onMessage
        self.mqttClient.username_pw_set(Parameters["Username"], Parameters["Password"])
        self.mqttClient.connect(Parameters["Mode1"], int(Parameters["Mode2"]))
        self.mqttClient.loop_start()


        specialOptions = {
            "LevelNames": "|".join([level["text"] for level in self.levels]),
            "LevelOffHidden": "true",
            "SelectorStyle": "1",
            "protected": "true"
        }

        # specialOptions = {
        #     "LevelActions": "|*|" * len(self.levels),
        #     "LevelNames": "|".join([level["text"] for level in self.levels]),
        #     "LevelOffHidden": "true",
        #     "SelectorStyle": "1",
        #     "protected": "true"
        # }

        device_info = {
            1: ("AC Voltage", "Voltage"),
            2: ("Output Voltage", "Voltage"),
            3: ("PV Voltage", "Voltage"),
            4: ("Battery Voltage", "Voltage"),
            5: ("AC Frequency", "Custom", 31, {'Custom': '1;Hz'}),
            6: ("Output Frequency", "Custom", 31, {'Custom': '1;Hz'}),
            7: ("Battery Charge Current", "General", 23),
            8: ("Battery Discharge Current", "General", 23),
            9: ("PV Power", "Usage", 1),
            10: ("Output Apparent Power", "Usage", 1),
            11: ("Output Active Power", "Usage", 1),
            12: ("PV Power", "General", 6),
            13: ("Battery SoC", "General", 6),
            14: ("AC Output Load", "General", 6),
            15: ("Operation Mode", "Selector Switch", 18, specialOptions, 0)
        }

        for unit, device_info_tuple in device_info.items():
            name, type_name = device_info_tuple[:2]
            subtype = device_info_tuple[2] if len(device_info_tuple) > 2 else None
            options = device_info_tuple[3] if len(device_info_tuple) > 3 else None
            icon_index = device_info_tuple[4] if len(device_info_tuple) > 4 else None

            if unit not in Devices:
                Domoticz.Log(f"Creating device {name} ...")
                if subtype is not None:
                    if options is not None:
                        device = Domoticz.Device(Name=name, Unit=unit, TypeName=type_name, Subtype=subtype, Options=options, Used=1)
                        if icon_index is not None:
                            device = Domoticz.Device(Name=name, Unit=unit, TypeName=type_name, Subtype=subtype, Options=options, Image=icon_index,  Used=1)
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
        self.mqttClient.subscribe("powmr/#")

    def onMessage(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")

        device_mapping = {
            "powmr/ac_voltage": 1,
            "powmr/output_voltage": 2,
            "powmr/pv_voltage": 3,
            "powmr/battery_voltage": 4,
            "powmr/ac_frequency": 5,
            "powmr/output_frequency": 6,
            "powmr/battery_charge_current": 7,
            "powmr/battery_discharge_current": 8,
            "powmr/pv_power": 9,
            "powmr/output_apparent_power": 10,
            "powmr/output_active_power": 11,
            "powmr/pv_power": 12,
            "powmr/battery_state_of_charge": 13,
            "powmr/ac_output_load": 14,
            "powmr/operation_mode": 15
        }

        operation_modes = [
            ["Power On", 1, 10],
            ["Standby", 0, 20],
            ["Mains", 0, 30],
            ["Off-Grid", 0, 40],
            ["Bypass", 1, 50],
            ["Charging", 1, 60],
            ["Fault", 0, 70]
        ]

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
                        if options == "{'Custom': '1;Hz'}":
                            Devices[unit].Update(nValue=0, sValue=str(value) + ";Hz")
                        else:
                            Devices[unit].Update(nValue=0, sValue=str(value))
                    else:
                         Devices[unit].Update(nValue=0, sValue=str(value))

                elif Devices[unit].Type == 244:
                    try:
                        operation_mode_index = int(value)
                        if 0 <= operation_mode_index < len(operation_modes):
                            operation_mode, state, level = operation_modes[operation_mode_index]
                            if current_sValue != str(level):
                                attempt = self.update_attempts.get(unit, 0)
                                if attempt < 3:
                                    self.update_attempts[unit] = attempt + 1
                                else:
                                    Devices[unit].Update(nValue=state, sValue=str(level))
                                    self.update_attempts[unit] = 0
                        else:
                            Domoticz.Error(f"Received invalid operation mode index: {operation_mode_index}")
                    except ValueError:
                        Domoticz.Error("Received non-integer value for operation mode")

                else:
                    Devices[unit].Update(nValue=0, sValue=str(value))

    def onHeartbeat(self):
        if not self.mqttClient.is_connected():
            Domoticz.Log("Attempting MQTT reconnection...")
            self.mqttClient.connect(Parameters["Mode1"], int(Parameters["Mode2"]))
            self.mqttClient.loop_start()

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