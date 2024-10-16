return {
   on = {
      devices = {
         "Powmr - Operation Mode"
      },
        timer = {'Every minute'}
   },
   execute = function(domoticz, switch)
      local power = domoticz.devices('Powmr - Operation Mode')
      local pv_voltage = domoticz.devices("Powmr - PV Voltage")
      local boiler = domoticz.devices("Бойлер - State")
      
      if(power.nValue == 0) then

        if(boiler.state == "On") then
           
            if(tonumber(pv_voltage.sValue) < 100) then
                boiler.switchOff()
                local msg = "Бойлер ЗУПИНКА! Резервне живлення. PV_Voltage: " .. pv_voltage.sValue
                domoticz.notify('Бойлер', msg)
                domoticz.log(msg)
            end

        else
            if(tonumber(pv_voltage.sValue) > 150) then
                boiler.switchOn()
                local msg = "Бойлер ВКЛЮЧЕННЯ! Резервне живлення. PV_Voltage: " .. pv_voltage.sValue
                domoticz.notify('Бойлер', msg)
                domoticz.log(msg)
            end
        end

      else

        if(boiler.state == "Off") then
          boiler.switchOn()
          local msg = "Бойлер ВКЛЮЧЕННЯ! Відновилось живлення."
          domoticz.notify('Бойлер', msg)
          domoticz.log(msg)
        end

      end
      
   end
}