return {
	on = {
		devices = {
	        "Контакт датчика відкриття вхідних дверей"
	    }
	},
	execute = function(domoticz, device)
	    local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
	    local vhidni_dveri = domoticz.devices("Контакт датчика відкриття вхідних дверей")

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
	   if (not isTimeInRange(currentTime, twilightBegin:sub(12), twilightEnd:sub(12))) then
    	    if(vhidni_dveri.state == "Open" and svitlo_shodiv.state == "Off") then
    	        local msg = "Освітлення сходів СТАРТ! LUX: " .. riven_svitla.lux
    	        svitlo_shodiv.switchOn()
    	        domoticz.notify('Освітлення сходів', msg, domoticz.PRIORITY_HIGH)
    	        domoticz.log(msg)
    		end
		end
	end
}