return {
	on = {
		devices = {
	        "Вимикач освітлення сходів"
	    }
	},
	execute = function(domoticz, device)
	   local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
	   local stay = domoticz.variables('Освітлення сходів у хвилинах').value

	   if(svitlo_shodiv.active) then
	       local msg = "Освітлення сходів СТАРТ!"
           domoticz.notify('Освітлення сходів', msg, domoticz.PRIORITY_HIGH)
           domoticz.log(msg)
	       svitlo_shodiv.switchOff().checkFirst().afterMin(stay)
        else
            local msg = "Освітлення сходів СТОП!"
            domoticz.notify('Освітлення сходів', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)
	    end
	end
}