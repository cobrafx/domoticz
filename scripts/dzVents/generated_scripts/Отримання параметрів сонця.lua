return {
	on = {
		timer = {
			'at 03:15' -- Запускаємо скрипт щодня о 03:15
		  --  'every 1 minutes'
		},
		httpResponses = {
			'trigger'
		}
	},
	logging = {
		level = domoticz.LOG_INFO,
		marker = 'sunrise',
	},
	execute = function(domoticz, item)

		if (item.isTimer) then

            -- local latitude = '49.653149'  -- Широта
            -- local longitude = '23.518314' -- Довгота
            
            local latitude = domoticz.settings.location.latitude  -- Широта
            local longitude = domoticz.settings.location.longitude -- Довгота

            local apiUrl = 'https://api.sunrise-sunset.org/json?lat=' .. latitude .. '&lng=' .. longitude .. '&formatted=0&tzid=Europe/Kyiv'

			domoticz.openURL({
				url = apiUrl,
				method = 'GET',
				callback = 'trigger',
			})
		end

		if (item.isHTTPResponse) then

			if (item.ok) then
				if (item.isJSON) then

                    local sunriseVar = domoticz.variables('Початок громадського дня')
                    local sunsetVar = domoticz.variables('Кінець громадського дня')
                    
                    local twilightBeginLocal =  domoticz.time.makeTime(item.json.results.civil_twilight_begin, false).rawDateTime
                    local twilightEndLocal =  domoticz.time.makeTime(item.json.results.civil_twilight_end, false).rawDateTime

					if not sunriseVar then
                        sunriseVar = domoticz.variables.create('Початок громадського дня', 'string', twilightBeginLocal)
                        domoticz.log('Змінна "Початок громадського дня" створена: ' .. twilightBeginLocal, domoticz.LOG_DEBUG)
                    else
                        sunriseVar.set(twilightBeginLocal)
                        domoticz.log('Змінна "Початок громадського дня" оновлена: ' .. twilightBeginLocal, domoticz.LOG_DEBUG)
                    end
    
                    if not sunsetVar then
                        sunsetVar = domoticz.variables.create('Кінець громадського дня', 'string', twilightEndLocal)
                        domoticz.log('Змінна "Кінець громадського дня" створена: ' .. twilightEndLocal, domoticz.LOG_DEBUG)
                    else
                        sunsetVar.set(twilightEndLocal)
                        domoticz.log('Змінна "Кінець громадського дня" оновлена: ' .. twilightEndLocal, domoticz.LOG_DEBUG)
                    end

				end
			else
				domoticz.log('Не вдалось отримати дані стосовно громадського дня', domoticz.LOG_ERROR)
				domoticz.log(item, domoticz.LOG_ERROR)
			end

		end

	end
}
