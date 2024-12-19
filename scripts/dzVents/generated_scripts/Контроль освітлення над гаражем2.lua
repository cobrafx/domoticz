return {
	on = {
		devices = {
	        "Контакт освітлення над гаражем"
	    }
	},
	execute = function(domoticz, device)
	   local projector = domoticz.devices("Контакт освітлення над гаражем")
	   local stay = domoticz.variables('Освітлення над гаражем у хвилинах').value
	   
	   if(projector.active) then
	       	local msg = "Освітлення гаражу прожектор СТАРТ!"
            domoticz.notify('Освітлення гаражу', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)
	        projector.switchOff().checkFirst().afterMin(stay)
	   else
	       	local msg = "Освітлення гаражу прожектор СТОП!"
            domoticz.notify('Освітлення гаражу', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)     
	   end

	end
}