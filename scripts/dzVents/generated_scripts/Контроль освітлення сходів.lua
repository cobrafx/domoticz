return {
	on = {
		devices = {
	        "Вимикач освітлення сходів"
	    }
	},
	execute = function(domoticz, device)
	   local riven_svitla = domoticz.devices("Рівень освітлення сходів")
	   local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
	   local stay = 8

	   if(svitlo_shodiv.active) then
	       local msg = "Освітлення сходів СТАРТ! LUX: " .. riven_svitla.lux
           domoticz.notify('Освітлення сходів', msg, domoticz.PRIORITY_HIGH)
           domoticz.log(msg)
	       svitlo_shodiv.switchOff().checkFirst().afterMin(stay)
        else
            local msg = "Освітлення сходів СТОП! LUX: " .. riven_svitla.lux
            domoticz.notify('Освітлення сходів', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)
	    end
	end
}