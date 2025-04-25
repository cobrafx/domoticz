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
	   
       local dzherelo = device.name  -- Отримуємо назву пристрою, який спрацював
       local msg = "Дзвінок у двері! Джерело: " .. dzherelo
	   
       domoticz.notify("Дзвінок", msg, domoticz.PRIORITY_HIGH)
       domoticz.log(msg)

	   -- Отримуємо значення змінних "Початок громадського дня" та "Кінець громадського дня"
	   local twilightBegin = domoticz.variables('Початок громадського дня').value
	   local twilightEnd = domoticz.variables('Кінець громадського дня').value


	   -- Отримуємо поточний час
	   local currentTime = os.date("%H:%M:%S")  -- Поточний час у форматі "HH:MM:SS"

	   -- Функція для порівняння часу
	   local function isTimeInRange(timeToCheck, startTime, endTime)
	       return (timeToCheck >= startTime and timeToCheck <= endTime)
	   end


	    local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
	    if(not isTimeInRange(currentTime, twilightBegin:sub(12), twilightEnd:sub(12)) and svitlo_shodiv.state == "Off") then
	        local msg2 = "Освітлення сходів СТАРТ!"
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