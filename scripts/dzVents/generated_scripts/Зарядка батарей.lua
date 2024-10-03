return {
   on = {
      timer = {
            'every 1 minutes'
      },
      devices = {
         "Контакт розетки котла"
      }
   },
   execute = function(domoticz, switch)

      local _u = domoticz.utils
      
      if _u.deviceExists('Powmr - Active Max Utility Charging') and _u.deviceExists('Контакт розетки котла') and _u.deviceExists('Powmr - Max Utility Charging') then
          local kotel = domoticz.devices('Контакт розетки котла')
          local max_utility_charging = domoticz.devices('Powmr - Active Max Utility Charging')
          local utility_charging = domoticz.devices('Powmr - Max Utility Charging')
          
        --   local msg = "State: " .. utility_charging.sValue
        --   domoticz.notify('Powmr', msg, domoticz.PRIORITY_HIGH)
          
          if(kotel.state == "On") then
            if(utility_charging.sValue ~= "10.0") then
                max_utility_charging.switchOff()
                local msg = "Переведено зарядку акумуляторів на 10A!"
                domoticz.notify('Powmr', msg, domoticz.PRIORITY_HIGH)
            end
          else
            if(utility_charging.sValue ~= "90.0") then
                local msg = "Переведено зарядку акумуляторів на 90A!"
                domoticz.notify('Powmr', msg, domoticz.PRIORITY_HIGH)
                max_utility_charging.switchOn()
            end
          end
      end
    end
}