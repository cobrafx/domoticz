return {
   on = {
      timer = {
            'every 1 minutes',
      },
      devices = {
         "Контакт розетки котла",
         "Powmr - Operation Mode"
      }
   },
   execute = function(domoticz, switch)

      local _u = domoticz.utils
      
      
    --   if _u.deviceExists('Feyree Charger - Ampers') and _u.deviceExists('Feyree Charger - Status') and _u.deviceExists('Контакт розетки котла') and _u.deviceExists('Powmr - Operation Mode') then
      
          
          local feyree_ampers = domoticz.devices('Feyree Charger - Ampers')
          local feyree_status = domoticz.devices('Feyree Charger - Status')
          local kotel = domoticz.devices('Контакт розетки котла')
          local power = domoticz.devices('Powmr - Operation Mode')
          local feyree_control = domoticz.devices('Feyree Charger - Charge Control')
          local off_level = "0A"
          local min_level = "16A"
          local normal_level = "20A"
          local max_level = "25A"


          if(power.nValue == 1) then
            if(domoticz.variables(4).value == 1) then
                feyree_control.switchOn().afterSec(8)
                domoticz.variables(4).set(tostring(0))
                local msg = "Feyree Station продовження зарядки"
                domoticz.notify('Feyree Station', msg, domoticz.PRIORITY_HIGH)
                return
            end
          end


          if feyree_status.text == 'charing' then
 
              local current_level = feyree_ampers.levelName
    
              if(power.nValue == 0) then
                if(domoticz.variables(4).value == 0) then
                    feyree_control.switchOff()
                    domoticz.variables(4).set(tostring(1))
                    local msg = "Feyree Station пауза зарядки"
                    domoticz.notify('Feyree Station', msg, domoticz.PRIORITY_HIGH)
                    return
                end
              end

              if(kotel.state == "On") then
                if(current_level ~= min_level ) then
                    feyree_ampers.switchSelector(min_level)
                    local msg = "Feyree Station переведено на " .. min_level
                    domoticz.notify('Feyree Station', msg, domoticz.PRIORITY_HIGH)
                end
              else
                local Time = require('Time')
                local now = Time()
                if (now.matchesRule('at 23:00-06:00')) then
                    if(current_level ~= max_level ) then
                        feyree_ampers.switchSelector(max_level).afterSec(8)
                        local msg = "Feyree Station переведено на " .. max_level
                        domoticz.notify('Feyree Station', msg, domoticz.PRIORITY_HIGH)
                    end
                else
                    if(current_level ~= normal_level ) then
                        feyree_ampers.switchSelector(normal_level).afterSec(8)
                        local msg = "Feyree Station переведено на " .. normal_level
                        domoticz.notify('Feyree Station', msg, domoticz.PRIORITY_HIGH)
                    end
                end
              end
          end    
    --   end
      
   end
}
