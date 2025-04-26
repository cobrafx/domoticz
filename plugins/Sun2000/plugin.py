"""
<plugin key="Sun2000" name="Sun2000" author="CobraFX" version="1.0" wikilink="https://github.com/domoticz/domoticz/wiki/Developing-A-Python-Plugin">
    <description>
        <h2>Sun2000 Plugin</h2><br/>
        This plugin reads data from Inverter Sun2000
    </description>
    <params>
        <param field="Mode1" label="Адреса Modbus TCP" width="200px" required="true" default="192.168.0.44"/>
        <param field="Mode2" label="Порт Modbus TCP" width="200px" required="true" default="502"/>
        <param field="Mode3" label="Debug" width="75px" required="true">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal" default="true"/>
            </options>
        </param>
    </params>
</plugin>
"""


import time
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from datetime import datetime

# Import Domoticz module
try:
    import Domoticz
except ImportError:
    import fakeDomoticz as Domoticz  # Use a fake Domoticz module for testing if necessary

class BasePlugin:
    def __init__(self):
        self.interval = 10  # Інтервал зчитування даних (секунди)
        self.host = "192.168.0.44"  # Адреса сервера Modbus TCP
        self.port = 502  # Порт сервера Modbus TCP
        self.debug = False
        self.unit_id = 1  # ID slave-пристрою
        self.last_update_time = 0
        self.device_info = {
        }

    def onStart(self):
        self.host = Parameters["Mode1"]
        self.port = int(Parameters["Mode2"])
        self.debug = Parameters["Mode3"] == "Debug"
        self.interval = 10
        if self.debug:
            Domoticz.Log("Plugin started")

        self.device_info = {
            1: ("Виробляється зараз", "Usage", 1, 32080, 2, 32),
            2: ("Вироблено за день", "Usage", 1, 32114, 2, 32),
            3: ("Фаза А", "General", 8, 32069, 1, 16),
            4: ("Фаза B", "General", 8, 32070, 1, 16),
            5: ("Фаза С", "General", 8, 32071, 1, 16),
            6: ("За місяць", "Usage", 1, 32116, 2, 32)
        }

        for unit, device_info_tuple in self.device_info.items():
            name, type_name = device_info_tuple[:2]
            subtype = device_info_tuple[2] if len(device_info_tuple) > 2 else None
            reg_address = device_info_tuple[3] if len(device_info_tuple) > 3 else None

            if unit not in Devices:
                if self.debug:
                    Domoticz.Log(f"Creating device {name} ...")
                device = Domoticz.Device(Name=name, Unit=unit, TypeName=type_name, Subtype=subtype, Used=1)
                device.Create()
                device.Update(nValue=0, sValue="0");
            else:
                if self.debug:
                    Domoticz.Log(f"Device {name} already exists")
                Devices[unit].Update(nValue=Devices[unit].nValue, sValue=Devices[unit].sValue);


    def onHeartbeat(self):
        if time.time() - self.last_update_time >= self.interval:
            try:
                now = datetime.now()
                hour = int(now.strftime("%H"))
                if hour >= 5 and hour <= 23:
                    self.readModbusData()
                time.sleep(self.interval)
            except Exception as e:
                Domoticz.Error(f"An error occurred: {str(e)}")
            self.last_update_time = time.time()


    def onStop(self):
        if self.debug:
            Domoticz.Log("Plugin stopped")


    def readModbusData(self):
        try:
            client = ModbusTcpClient(self.host, port=self.port)
            client.connect()
            client.unit_id = self.unit_id

            for unit, device_info_tuple in self.device_info.items():
                name, type_name = device_info_tuple[:2]
                subtype = device_info_tuple[2] if len(device_info_tuple) > 2 else None
                reg_address = device_info_tuple[3] if len(device_info_tuple) > 3 else None
                quantity = device_info_tuple[4] if len(device_info_tuple) > 4 else None
                decode = device_info_tuple[5] if len(device_info_tuple) > 5 else None


                result = client.read_holding_registers(address=reg_address, count=quantity, unit=self.unit_id)
                if not result.isError():
                    decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                    value = decoder.decode_32bit_int() if decode == 32 else decoder.decode_16bit_int() / 10
                    value = value * 10 if unit == 2 else value
                    value = value * 10 if unit == 6 else value
                    if unit in Devices:
                        try:
                            Devices[unit].Update(nValue=0, sValue=str(value));
                            if self.debug:
                                Domoticz.Log(f"Device {name} updated: {value}")
                        except Exception as e:
                            if self.debug:
                                Domoticz.Error(f"An error occurred while updating device {name}: {str(e)}")
                else:
                    if self.debug:
                        Domoticz.Error(f"Failed to read data for {name}")

            client.close()
        except Exception as e:
            if self.debug:
                Domoticz.Error(f"An error occurred while reading Modbus data: {str(e)}")


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
