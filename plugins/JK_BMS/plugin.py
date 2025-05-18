"""
<plugin key="JkongBMS" name="JKONG BMS" author="cobrafx" version="1.0.0">
    <description>
        <h2>Jkong BMS Plugin</h2><br/>
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Monitoring BMS</li>
        </ul><br/>
        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li>SOC</li>
            <li>Delta Cell Voltage</li>
            <li>Current</li>
            <li>Total Voltage</li>
            <li>Max Cell Voltage</li>
            <li>Min Cell Voltage</li>
            <li>Cell Voltage Overvoltage Protection</li>
            <li>Cells Voltage</li>
            <li>Temperature Sensors</li>
            <li>Power</li>
        </ul>
    </description>
    <params>
        <param field="Address" label="MQTT IP Address" width="200px" required="true" default="127.0.0.1"/>
        <param field="Port" label="MQTT Port" width="30px" required="true" default="1883"/>
        <param field="Username" label="MQTT Username" width="150px" required="false"/>
        <param field="Password" label="MQTT Password" width="150px" required="false"/>
        <param field="Mode1" label="Topic" width="150px" required="true" default="jk-bms"/>
        <param field="Mode2" label="Debug" width="75px">
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
import json
import paho.mqtt.client as mqtt

class BasePlugin:
    mqttClient = None

    def __init__(self):
        self.debug = False

    def onStart(self):
        Domoticz.Log("JK BMS Plugin started.")
        if Parameters["Mode2"] == "Debug":
            self.debug = True

        # Створюємо пристрої
        if 1 not in Devices:
            Domoticz.Device(Name="SOC", Unit=1, Type=243, Subtype=6, Used=1).Create()
        if 2 not in Devices:
            Domoticz.Device(Name="Delta Cell Voltage", Unit=2, Type=243, Subtype=8, Used=1).Create()
        if 3 not in Devices:
            Domoticz.Device(Name="Current", Unit=3, Type=243, Subtype=23, Used=1).Create()
        if 4 not in Devices:
            Domoticz.Device(Name="Min Cell Voltage", Unit=4, Type=243, Subtype=8, Used=1).Create()
        if 5 not in Devices:
            Domoticz.Device(Name="Max Cell Voltage", Unit=5, Type=243, Subtype=8, Used=1).Create()
        if 6 not in Devices:
            Domoticz.Device(Name="Cell Voltage Overvoltage Protection", Unit=6, Type=243, Subtype=8, Used=1).Create()
        if 7 not in Devices:
            Domoticz.Device(Name="Cell Voltage 1", Unit=7, Type=243, Subtype=8, Used=1).Create()
        if 8 not in Devices:
            Domoticz.Device(Name="Cell Voltage 2", Unit=8, Type=243, Subtype=8, Used=1).Create()
        if 9 not in Devices:
            Domoticz.Device(Name="Cell Voltage 3", Unit=9, Type=243, Subtype=8, Used=1).Create()
        if 10 not in Devices:
            Domoticz.Device(Name="Cell Voltage 4", Unit=10, Type=243, Subtype=8, Used=1).Create()
        if 11 not in Devices:
            Domoticz.Device(Name="Cell Voltage 5", Unit=11, Type=243, Subtype=8, Used=1).Create()
        if 12 not in Devices:
            Domoticz.Device(Name="Cell Voltage 6", Unit=12, Type=243, Subtype=8, Used=1).Create()
        if 13 not in Devices:
            Domoticz.Device(Name="Cell Voltage 7", Unit=13, Type=243, Subtype=8, Used=1).Create()
        if 14 not in Devices:
            Domoticz.Device(Name="Cell Voltage 8", Unit=14, Type=243, Subtype=8, Used=1).Create()
        if 15 not in Devices:
            Domoticz.Device(Name="Cell Voltage 9", Unit=15, Type=243, Subtype=8, Used=1).Create()
        if 16 not in Devices:
            Domoticz.Device(Name="Cell Voltage 10", Unit=16, Type=243, Subtype=8, Used=1).Create()
        if 17 not in Devices:
            Domoticz.Device(Name="Cell Voltage 11", Unit=17, Type=243, Subtype=8, Used=1).Create()
        if 18 not in Devices:
            Domoticz.Device(Name="Cell Voltage 12", Unit=18, Type=243, Subtype=8, Used=1).Create()
        if 19 not in Devices:
            Domoticz.Device(Name="Cell Voltage 13", Unit=19, Type=243, Subtype=8, Used=1).Create()
        if 20 not in Devices:
            Domoticz.Device(Name="Cell Voltage 14", Unit=20, Type=243, Subtype=8, Used=1).Create()
        if 21 not in Devices:
            Domoticz.Device(Name="Cell Voltage 15", Unit=21, Type=243, Subtype=8, Used=1).Create()
        if 22 not in Devices:
            Domoticz.Device(Name="Cell Voltage 16", Unit=22, Type=243, Subtype=8, Used=1).Create()
        if 23 not in Devices:
            Domoticz.Device(Name="Power Tube Temperature", Unit=23, Type=80, Subtype=5, Used=1).Create()
        if 24 not in Devices:
            Domoticz.Device(Name="Sensor Temperature 1", Unit=24, Type=80, Subtype=5, Used=1).Create()
        if 25 not in Devices:
            Domoticz.Device(Name="Sensor Temperature 2", Unit=25, Type=80, Subtype=5, Used=1).Create()
        if 26 not in Devices:
            Domoticz.Device(Name="Power", Unit=26, TypeName="Custom", Options={"Custom": "1;W"}, Used=1).Create()
        if 27 not in Devices:
            Domoticz.Device(Name="Total Voltage", Unit=27, Type=243, Subtype=8, Used=1).Create()

        for unit in Devices:
            if unit == 1:
                Devices[unit].Update(nValue=0, sValue="100")
            else:
                Devices[unit].Update(nValue=0, sValue="0")

        self.mqttClient = mqtt.Client()
        self.mqttClient.reconnect_delay_set(min_delay=1, max_delay=120)
        self.mqttClient.on_connect = self.onMQTTConnect
        self.mqttClient.on_message = self.onMQTTMessage

        if Parameters["Username"]:
            self.mqttClient.username_pw_set(Parameters["Username"], Parameters["Password"])

        try:
            if self.mqttClient.connect(Parameters["Address"], int(Parameters["Port"])) == 0:
                self.mqttClient.loop_start()
        except Exception as e:
            Domoticz.Error(f"MQTT connection failed: {e}")

    def onStop(self):
        if self.mqttClient:
            self.mqttClient.loop_stop()
            self.mqttClient.disconnect()
        Domoticz.Log("JK BMS Plugin stopped.")

    def onMQTTConnect(self, client, userdata, flags, rc):
        topic = Parameters["Mode1"] + "/sensor/#"
        if self.debug:
            Domoticz.Log(f"Connected to MQTT broker, subscribing to topic '{topic}'")
        client.subscribe(topic)

    def onMQTTMessage(self, client, userdata, msg):
        if self.debug:
            Domoticz.Log(f"MQTT Message: {msg.topic} => {msg.payload.decode()}")

        topic = msg.topic
        value = msg.payload.decode()

        prefix = Parameters["Mode1"]

        topic_map = {
            f"{prefix}/sensor/jk-bms_capacity_remaining/state": 1,
            f"{prefix}/sensor/jk-bms_delta_cell_voltage/state": 2,
            f"{prefix}/sensor/jk-bms_current/state": 3,
            f"{prefix}/sensor/jk-bms_min_cell_voltage/state": 4,
            f"{prefix}/sensor/jk-bms_max_cell_voltage/state": 5,
            f"{prefix}/sensor/jk-bms_cell_voltage_overvoltage_protection/state": 6,
            f"{prefix}/sensor/jk-bms_cell_voltage_1/state": 7,
            f"{prefix}/sensor/jk-bms_cell_voltage_2/state": 8,
            f"{prefix}/sensor/jk-bms_cell_voltage_3/state": 9,
            f"{prefix}/sensor/jk-bms_cell_voltage_4/state": 10,
            f"{prefix}/sensor/jk-bms_cell_voltage_5/state": 11,
            f"{prefix}/sensor/jk-bms_cell_voltage_6/state": 12,
            f"{prefix}/sensor/jk-bms_cell_voltage_7/state": 13,
            f"{prefix}/sensor/jk-bms_cell_voltage_8/state": 14,
            f"{prefix}/sensor/jk-bms_cell_voltage_9/state": 15,
            f"{prefix}/sensor/jk-bms_cell_voltage_10/state": 16,
            f"{prefix}/sensor/jk-bms_cell_voltage_11/state": 17,
            f"{prefix}/sensor/jk-bms_cell_voltage_12/state": 18,
            f"{prefix}/sensor/jk-bms_cell_voltage_13/state": 19,
            f"{prefix}/sensor/jk-bms_cell_voltage_14/state": 20,
            f"{prefix}/sensor/jk-bms_cell_voltage_15/state": 21,
            f"{prefix}/sensor/jk-bms_cell_voltage_16/state": 22,
            f"{prefix}/sensor/jk-bms_power_tube_temperature/state": 23,
            f"{prefix}/sensor/jk-bms_temperature_sensor_1/state": 24,
            f"{prefix}/sensor/jk-bms_temperature_sensor_2/state": 25,
            f"{prefix}/sensor/jk-bms_power/state": 26
        }

        if topic in topic_map:
            unit = topic_map[topic]
            # Devices[unit].Update(nValue=0, sValue=str(value))

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

            if self.debug:
                Domoticz.Log(f"Updated Unit {unit} with value {value}")
        else:
            if self.debug:
                Domoticz.Log(f"Ignored topic: {topic}")

    def onHeartbeat(self):
            total_value = 0.0
            for unit in range(7, 23):  # Прохід по Unit від 7 до 22 включно
                if unit in Devices:  # Перевіряємо, чи пристрій існує
                    try:
                        value = float(Devices[unit].sValue)  # Перетворюємо значення на float
                        total_value += value
                    except ValueError:
                        Domoticz.Error(f"Cannot convert sValue of device with Unit {unit} to float")

            # Заокруглюємо до другого знака після коми
            total_value = round(total_value, 2)
            # Оновлення пристрою, якщо значення змінилося
            if Devices[27].sValue != round(total_value, 2):
                Devices[27].Update(nValue=0, sValue=str(total_value))

global _plugin
_plugin = BasePlugin()

def onStart():
    _plugin.onStart()

def onStop():
    _plugin.onStop()

def onHeartbeat():
     _plugin.onHeartbeat()