return {
   on = {
      devices = {
         "Температура у гардеробній",
         "Powmr - AC Status"
      }
        -- timer = {'Every minute'}
   },
   execute = function(domoticz, switch)
      local ac_status = domoticz.devices('Powmr - AC Status')
      local temp = domoticz.utils.round(domoticz.devices("Температура у гардеробній").temperature,1)
      local kotel = domoticz.devices('Контакт розетки котла')
      local thermostat = domoticz.devices('Термостат будинку')
      local delta = 0.2

      if(ac_status.nValue == 0) then

         if(kotel.state == "On") then
           kotel.switchOff()
           local msg = "Котел ЗУПИНКА! Резервне живлення. Температура: " .. temp
           domoticz.notify('Котел', msg, domoticz.PRIORITY_HIGH)
           domoticz.log(msg)
         end

      else

         local need_temp = 19.0
           -- Гості
         if(thermostat.levelVal == 40) then
             need_temp = 19.7
           -- Ташкент
         elseif(thermostat.levelVal == 10) then
             need_temp = 19.3
          -- Нормальний
         elseif(thermostat.levelVal == 20) then
             need_temp = 18.9
         -- Економний
         elseif(thermostat.levelVal == 30) then
            need_temp = 18.2
         -- За кордоном
         elseif(thermostat.levelVal == 50) then
            need_temp = 14.6
         end
    
         if((kotel.state == "On") and (temp >= need_temp + delta)) then
           kotel.switchOff()
           local msg = "Котел ЗУПИНКА! Температура: " .. temp
           domoticz.notify('Котел', msg, domoticz.PRIORITY_HIGH)
           domoticz.log(msg)
         elseif((kotel.state == "Off") and (temp <= need_temp - delta)) then
           kotel.switchOn()
           local msg = "Котел СТАРТ! Температура: " .. temp
           domoticz.notify('Котел', msg, domoticz.PRIORITY_HIGH)
           domoticz.log(msg)
         end
      
      end
      
   end
}