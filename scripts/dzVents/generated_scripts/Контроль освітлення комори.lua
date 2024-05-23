return {
	on = {
		devices = {
	        "Контакт освітлення комори"
	    }
	},
	execute = function(domoticz, device)
	   local riven_svitla = domoticz.devices("Рівень освітлення сходів")
	   local svitlo_komory = domoticz.devices("Контакт освітлення комори")
	   local stay = 8
	   
	   if(svitlo_komory.active) then
	        local msg = "Освітлення комори СТАРТ! LUX: " .. riven_svitla.lux
            domoticz.notify('Освітлення комори', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)
	        svitlo_komory.switchOff().checkFirst().afterMin(stay)
	    else
	        local msg = "Освітлення комори СТОП! LUX: " .. riven_svitla.lux
            domoticz.notify('Освітлення комори', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)
	    end

	end
}