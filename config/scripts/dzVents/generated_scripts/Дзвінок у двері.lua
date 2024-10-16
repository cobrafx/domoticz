return {
	on = {
		devices = {
	        "Кнопка дзвінка",
	        "Дзвінок на вулиці"
	    }
	},
	execute = function(domoticz, device)
	   local knopka = domoticz.devices("Кнопка дзвінка")
	   local dzvinok = domoticz.devices("Xiaomi Gateway Doorbell")
	   local zvuk = domoticz.devices("Xiaomi Gateway Volume")
	   local light = domoticz.devices("Xiaomi RGB Gateway (192.168.0.9)")
	   local msg = "Дзвінок у двері!"
       domoticz.notify("Дзвінок", msg, domoticz.PRIORITY_HIGH)
       domoticz.log(msg)
       
       	local riven_svitla = domoticz.devices("Рівень освітлення сходів")
	    local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
	    if((riven_svitla.lux < 27) and (svitlo_shodiv.state == "Off")) then
	        local msg2 = "Освітлення сходів СТАРТ! LUX: " .. riven_svitla.lux
	        svitlo_shodiv.switchOn()
	        domoticz.notify('Освітлення сходів', msg2, domoticz.PRIORITY_HIGH)
	        domoticz.log(msg2)
		end
       
	   zvuk.dimTo(45)
	   dzvinok.dimTo(10)
	   local i = 1
       light.setRGB(0, 128, 255).afterSec(i)
       i = i + 1
       light.setRGB(255, 0, 0).afterSec(i)
       i = i + 1
       light.setRGB(255, 255, 0).afterSec(i)
       i = i + 1
       light.switchOff().afterSec(i+1)	   
	end
}