return {
	on = {
		devices = {
			"Сигналізація"
		}
	},
	execute = function(domoticz, device)

        local function telegram(msg)
            local bot_api = "1060079381:AAHlZvRxFpqeRIqp1nJBUexXScRpJWdBiWs"
            local chat_id = "-1001493931760"
            domoticz.openURL('https://api.telegram.org/bot' .. bot_api .. '/sendMessage?chat_id=' .. chat_id .. '&text=' .. msg) 
        end

        local zvuk = domoticz.devices("Xiaomi Gateway Volume")
        local sound = domoticz.devices("Xiaomi Gateway Alarm Ringtone")
        local light = domoticz.devices("Xiaomi RGB Gateway (192.168.0.9)")
        local security = domoticz.devices("Сигналізація")
        local vhidni_dveri = domoticz.devices("Контакт датчика відкриття вхідних дверей")
        local dveri_pidvalu = domoticz.devices("Контакт датчика дверей підвалу")

        if(security.state == "On") then
            local msg = ""
            if(dveri_pidvalu.state == "Open") then
                msg = "Не можу поставити на сигналізацію, оскільки не закрито двері підвалу!"
                telegram(msg)
                domoticz.notify('Сигналізація', msg, domoticz.PRIORITY_HIGH)
                domoticz.log(msg)
                security.switchOff()
                return
            end
            if(vhidni_dveri.state == "Open") then
                msg = "Не можу поставити на сигналізацію, оскільки не закрито вхідні двері!"
                telegram(msg)
                domoticz.notify('Сигналізація', msg, domoticz.PRIORITY_HIGH)
                domoticz.log(msg)
                security.switchOff()
                return
            end
            
            msg = "Поставлено на сигналізацію"
            domoticz.notify('Сигналізація', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)
            domoticz.devices('MiHome Ringtone').dimTo(1)
            domoticz.devices('MiHome Ringtone').switchOff().afterSec(3)

        elseif(security.state == "Off") then
            if(sound.state == "On") then
                sound.switchOff()
            end
            if(light.state == "On") then
                light.switchOff()
            end
            local msg = "Знято з сигналізації"
            domoticz.notify('Сигналізація', msg, domoticz.PRIORITY_HIGH)
            domoticz.log(msg)
            domoticz.devices('MiHome Ringtone').dimTo(1)
            domoticz.devices('MiHome Ringtone').switchOff().afterSec(3)
        end

	end

}