return {
   on = {
      timer = {
            'every 1 minutes'
      },
      devices = {
         "Контакт розетки котла",
         "JK_BMS - SOC",
         'JK_BMS - Max Cell Voltage'
      }
   },
   execute = function(domoticz, switch)

      local _u = domoticz.utils
      
      if _u.deviceExists('Powmr - Active Max Utility Charging') and _u.deviceExists('Контакт розетки котла') and _u.deviceExists('Powmr - Max Utility Charging') and _u.deviceExists('JK_BMS - SOC') and _u.deviceExists('JK_BMS - Cell Voltage Overvoltage Protection') and _u.deviceExists('JK_BMS - Max Cell Voltage') and _u.deviceExists('JK_BMS - Total Voltage') then
          local kotel = domoticz.devices('Контакт розетки котла')
          local max_utility_charging = domoticz.devices('Powmr - Active Max Utility Charging')
          local utility_charging = domoticz.devices('Powmr - Max Utility Charging')
          local charging_only_from_sun = domoticz.devices('Powmr - Active Charging Only From Sun')
          local charging_priority = tonumber(domoticz.devices('Powmr - Charger Source Priority').sValue)
          local bms_soc = domoticz.devices('JK_BMS - SOC')
          local soc_value = tonumber(bms_soc.sValue)
          local current_value = tonumber(utility_charging.sValue)
          local total_bms_voltage = tonumber(domoticz.devices('JK_BMS - Total Voltage').sValue)
          local max_cell_voltage = tonumber(domoticz.devices('JK_BMS - Max Cell Voltage').sValue)
          local limit_max_cell_voltage = tonumber(domoticz.devices('JK_BMS - Cell Voltage Overvoltage Protection').sValue) - 0.025
          
          if(soc_value < 100) then
              if(charging_priority ~= 0 and soc_value < 92) then
                charging_only_from_sun.switchOff()
                local msg = "Почато зарядку акумуляторів (SOC " .. bms_soc.sValue .. "%)!"
                domoticz.notify('BMS', msg, domoticz.PRIORITY_HIGH)
              end
          else
              if(charging_priority ~= 2 and max_cell_voltage >= limit_max_cell_voltage) then
                charging_only_from_sun.switchOn()
                local msg = "Закінчено зарядку акумуляторів (SOC " .. bms_soc.sValue .. "%). ".. "Напруга батареї: " .. total_bms_voltage .. "В!"
                domoticz.notify('BMS', msg, domoticz.PRIORITY_HIGH)
              end
          end

          if(kotel.state == "On") then
            if(charging_priority ~= 2 and current_value ~= 20) then
                max_utility_charging.switchOff()
                local msg = "Переведено зарядку акумуляторів (SOC " .. bms_soc.sValue .. "%) на 20A!"
                domoticz.notify('Powmr', msg, domoticz.PRIORITY_HIGH)
            end
          else
            if(current_value ~= 100) then
                local msg = "Переведено зарядку акумуляторів (SOC " .. bms_soc.sValue .. "%) на 100A!"
                domoticz.notify('Powmr', msg, domoticz.PRIORITY_HIGH)
                max_utility_charging.switchOn()
            end
          end
      end
    end
}