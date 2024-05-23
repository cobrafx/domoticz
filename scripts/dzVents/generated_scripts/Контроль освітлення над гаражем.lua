return {
	on = {
		devices = {
	        "Контакт освітлення над гаражем"
	    }
	},
	execute = function(domoticz, device)
	   local riven_svitla = domoticz.devices("Рівень освітлення сходів")
	   local projector = domoticz.devices("Контакт освітлення над гаражем")
	   local stay = 8
	   
	   if(projector.active) then
	       	local msg = "Освітлення гаражу прожектор СТАРТ! LUX: " .. riven_svitla.lux
            domoticz.notify('Освітлення гаражу', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)
	        projector.switchOff().checkFirst().afterMin(stay)
	   else
	       	local msg = "Освітлення гаражу прожектор СТОП! LUX: " .. riven_svitla.lux
            domoticz.notify('Освітлення гаражу', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)     
	   end

	end
}