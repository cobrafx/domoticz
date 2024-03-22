return {
	on = {
		devices = {
	        "Датчик руху до гаражу"
	    }
	},
	execute = function(domoticz, device)
	   local ruh_garaz = domoticz.devices("Датчик руху до гаражу") 
	   local riven_svitla = domoticz.devices("Рівень освітлення сходів")
	   local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
	   local projector = domoticz.devices("Контакт освітлення над гаражем")
	   local svitlo_komory = domoticz.devices("Контакт освітлення комори")
	   
	   if(((riven_svitla.lux < 27) or (svitlo_shodiv.state == "On")) and ((projector.state == "Off") and (svitlo_komory.state == "Off")) and (ruh_garaz.state == "On")) then
	        projector.switchOn().checkFirst()
            svitlo_komory.switchOn().checkFirst()
	    end
	   
	end
}
