return {
	on = {
		devices = {
	        "Датчик дверей гаражу"
	    }
	},
	execute = function(domoticz, device)
	   local dveri_garazu = domoticz.devices("Датчик дверей гаражу") 
	   local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
	   local projector = domoticz.devices("Контакт освітлення над гаражем")
	   local svitlo_komory = domoticz.devices("Контакт освітлення комори")

	   -- Отримуємо значення змінних "Початок громадського дня" та "Кінець громадського дня"
	   local twilightBegin = domoticz.variables('Початок громадського дня').value
	   local twilightEnd = domoticz.variables('Кінець громадського дня').value

	   -- Отримуємо поточний час
	   local currentTime = os.date("%H:%M:%S")  -- Поточний час у форматі "HH:MM:SS"

	   -- Функція для порівняння часу
	   local function isTimeInRange(timeToCheck, startTime, endTime)
	       return (timeToCheck >= startTime and timeToCheck <= endTime)
	   end

        -- Перевірка, чи поточний час не знаходиться в межах громадського дня
	   if (not isTimeInRange(currentTime, twilightBegin:sub(12), twilightEnd:sub(12)) or svitlo_shodiv.state == "On") then
    	   if(projector.state == "Off" and svitlo_komory.state == "Off" and dveri_garazu.state == "Open") then
                projector.switchOn().checkFirst()
                svitlo_komory.switchOn().checkFirst()
    	        local msg = "Освітлення гаражу при піднятті дверей СТАРТ! LUX: " .. riven_svitla.lux
                domoticz.notify('Освітлення гаражу при піднятті дверей', msg, domoticz.PRIORITY_HIGH)
                domoticz.log(msg)
    	    end
	    end
	   
	end
}