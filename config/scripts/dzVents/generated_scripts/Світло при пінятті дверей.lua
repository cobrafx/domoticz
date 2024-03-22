return {
	on = {
		devices = {
	        "Датчик дверей гаражу"
	    }
	},
	execute = function(domoticz, device)
	   local dveri_garazu = domoticz.devices("Датчик дверей гаражу") 
	   local riven_svitla = domoticz.devices("Рівень освітлення сходів")
	   local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
	   local projector = domoticz.devices("Контакт освітлення над гаражем")
	   local svitlo_komory = domoticz.devices("Контакт освітлення комори")
	   
	   if(((projector.state == "Off") and (svitlo_komory.state == "Off")) and (((riven_svitla.lux < 27) or (svitlo_shodiv.state == "On")) and (dveri_garazu.state == "Open"))) then
            projector.switchOn().checkFirst()
            svitlo_komory.switchOn().checkFirst()
	        local msg = "Освітлення гаражу при піднятті дверей СТАРТ! LUX: " .. riven_svitla.lux
            domoticz.notify('Освітлення гаражу при піднятті дверей', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)
	    end
	   
	end
}