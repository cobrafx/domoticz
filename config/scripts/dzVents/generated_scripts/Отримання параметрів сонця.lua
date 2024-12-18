return {
    on = {
        timer = { 'at 00:03' } -- Запускаємо скрипт щодня о 00:03
        -- timer = { 'every 1 minutes' }
    },
    execute = function(domoticz)
        domoticz.log('Скрипт запустився', domoticz.LOG_DEBUG)

        local latitude = '49.653149'  -- Широта
        local longitude = '23.518314' -- Довгота
        local apiUrl = 'https://api.sunrise-sunset.org/json?lat=' .. latitude .. '&lng=' .. longitude .. '&formatted=0'

        domoticz.log('Виконуємо curl для: ' .. apiUrl, domoticz.LOG_DEBUG)

        local handle = io.popen('curl -s "' .. apiUrl .. '"')
        local response = handle:read("*a")
        handle:close()

        if response then
            domoticz.log('Відповідь через curl: ' .. response, domoticz.LOG_DEBUG)
            local json = domoticz.utils.fromJSON(response)

            if json and json.status == 'OK' then
                -- Час початку та кінця громадського сутінку в UTC
                local twilightBeginUTC = json.results.civil_twilight_begin
                local twilightEndUTC = json.results.civil_twilight_end

                -- Функція для перетворення ISO часу у Lua таблицю часу
                local function parseISOTime(isoTime)
                    local pattern = "(%d+)%-(%d+)%-(%d+)T(%d+):(%d+):(%d+)"
                    local year, month, day, hour, min, sec = isoTime:match(pattern)
                    return os.time({
                        year = year, month = month, day = day,
                        hour = hour, min = min, sec = sec
                    })
                end


                -- Конвертуємо час із UTC у локальний час (UTC+2)
                local twilightBeginLocal = os.date("%Y-%m-%d %H:%M:%S", parseISOTime(twilightBeginUTC) + 2 * 3600)  -- Додаємо 2 години для UTC+2
                local twilightEndLocal = os.date("%Y-%m-%d %H:%M:%S", parseISOTime(twilightEndUTC) + 2 * 3600)  -- Додаємо 2 години для UTC+2


                -- -- Конвертуємо час із UTC у локальний час
                -- local twilightBeginLocal = os.date("%Y-%m-%d %H:%M:%S", parseISOTime(twilightBeginUTC))
                -- local twilightEndLocal = os.date("%Y-%m-%d %H:%M:%S", parseISOTime(twilightEndUTC))

                -- Логування результатів
                domoticz.log('Початок громадського дня (локальний час): ' .. twilightBeginLocal .. ', Кінець громадського дня (локальний час): ' .. twilightEndLocal, domoticz.LOG_DEBUG)

                -- Перевіряємо та створюємо змінні, якщо їх немає
                local sunriseVar = domoticz.variables('Початок громадського дня')
                local sunsetVar = domoticz.variables('Кінець громадського дня')

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
            else
                domoticz.log('Помилка при отриманні даних: ' .. (json and json.status or 'Невірна відповідь API'), domoticz.LOG_ERROR)
            end
        else
            domoticz.log('Помилка: curl не повернув відповідь', domoticz.LOG_ERROR)
        end
    end
}
