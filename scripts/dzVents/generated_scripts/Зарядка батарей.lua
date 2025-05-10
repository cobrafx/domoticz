return {
   on = {
      timer = {
            'every 1 minutes'
      },
      devices = {
         "Контакт розетки котла",
         "BMS JK - Battery SoC"
      }
   },
   execute = function(domoticz, switch)

      local _u = domoticz.utils
      
      if _u.deviceExists('Powmr - Active Max Utility Charging') and _u.deviceExists('Контакт розетки котла') and _u.deviceExists('Powmr - Max Utility Charging') and _u.deviceExists('BMS JK - Battery SoC') then
          local kotel = domoticz.devices('Контакт розетки котла')
          local max_utility_charging = domoticz.devices('Powmr - Active Max Utility Charging')
          local utility_charging = domoticz.devices('Powmr - Max Utility Charging')
          local charging_only_from_sun = domoticz.devices('Powmr - Active Charging Only From Sun')
          local charging_priority = tonumber(domoticz.devices('Powmr - Charger Source Priority').sValue)
          local bms_soc = domoticz.devices('BMS JK - Battery SoC')
          local soc_value = tonumber(bms_soc.sValue)
          local current_value = tonumber(utility_charging.sValue)
            
          local need_charge = false

          if(soc_value < 100) then
              need_charge = true
              if(charging_priority ~= 0) then
                charging_only_from_sun.switchOff()
              end
          else
              need_charge = false
              if(charging_priority ~= 2) then
                charging_only_from_sun.switchOn()
              end
          end

          if(kotel.state == "On") then
            if(need_charge == true and current_value ~= 2) then
                max_utility_charging.switchOff()
                local msg = "Переведено зарядку акумуляторів (SOC " .. bms_soc.sValue .. "%) на 2A!"
                domoticz.notify('Powmr', msg, domoticz.PRIORITY_HIGH)
            end
          else
            if(need_charge == true and current_value ~= 90) then
                local msg = "Переведено зарядку акумуляторів (SOC " .. bms_soc.sValue .. "%) на 90A!"
                domoticz.notify('Powmr', msg, domoticz.PRIORITY_HIGH)
                max_utility_charging.switchOn()
            end
            if(need_charge == false and current_value ~= 2) then
                max_utility_charging.switchOff()
                local msg = "Переведено зарядку акумуляторів (SOC " .. bms_soc.sValue .. "%) на 2A!"
                domoticz.notify('Powmr', msg, domoticz.PRIORITY_HIGH)                
            end
          end
      end
    end
}