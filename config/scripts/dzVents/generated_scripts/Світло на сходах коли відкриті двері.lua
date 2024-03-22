return {
	on = {
		devices = {
	        "Контакт датчика відкриття вхідних дверей"
	    }
	},
	execute = function(domoticz, device)
	    local riven_svitla = domoticz.devices("Рівень освітлення сходів")
	    local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
	    local vhidni_dveri = domoticz.devices("Контакт датчика відкриття вхідних дверей")
	    if((riven_svitla.lux < 27) and (vhidni_dveri.state == "Open") and (svitlo_shodiv.state == "Off")) then
	   -- if((vhidni_dveri.state == "Open") and (svitlo_shodiv.state == "Off")) then
	        local msg = "Освітлення сходів СТАРТ! LUX: " .. riven_svitla.lux
	        svitlo_shodiv.switchOn()
	        domoticz.notify('Освітлення сходів', msg, domoticz.PRIORITY_HIGH)
	        domoticz.log(msg)
		end
	end
}