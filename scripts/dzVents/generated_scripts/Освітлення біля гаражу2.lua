return {
	on = {
		devices = {
	        "Датчик руху до гаражу"
	    }
	},
	execute = function(domoticz, device)
	   local ruh_garaz = domoticz.devices("Датчик руху до гаражу") 
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
	   
    	   if(projector.state == "Off" and svitlo_komory.state == "Off" and ruh_garaz.state == "On") then
    	        projector.switchOn().checkFirst()
                svitlo_komory.switchOn().checkFirst()
    	    end
	    
	    end
	   
	end
}
