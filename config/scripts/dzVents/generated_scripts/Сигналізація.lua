return {
	on = {
		devices = {
			"Контакт датчика відкриття вхідних дверей",
			"Контакт датчика дверей підвалу",
-- 			"Сигналізація"
		}
	},
	execute = function(domoticz, device)

        local zvuk = domoticz.devices("Xiaomi Gateway Volume")
        local sound = domoticz.devices("Xiaomi Gateway Alarm Ringtone")
        local light = domoticz.devices("Xiaomi RGB Gateway (192.168.0.9)")
        local security = domoticz.devices("Сигналізація")
        local vhidni_dveri = domoticz.devices("Контакт датчика відкриття вхідних дверей")
        local dveri_pidvalu = domoticz.devices("Контакт датчика дверей підвалу")

        local function telegram(msg)
            local bot_api = "1060079381:AAHlZvRxFpqeRIqp1nJBUexXScRpJWdBiWs"
            local chat_id = "-1001493931760"
            domoticz.openURL('https://api.telegram.org/bot' .. bot_api .. '/sendMessage?chat_id=' .. chat_id .. '&text=' .. msg) 
        end

        if(security.state == "On") then
            if((vhidni_dveri.state == 'Open') or (dveri_pidvalu.state == 'Open')) then
                local msg = "УВАГА! Спрацювала сигналізація!!!"
                local body = "Бажано перевірити, чому в хаті спрацювала сигналізація!!!"
                domoticz.email(msg, body, 'cobrafx@gmail.com')
                domoticz.email(msg, body, 'tetyana.holynska@gmail.com')
                telegram(msg)
                domoticz.log(msg)
                local svitlo_shodiv = domoticz.devices("Вимикач освітлення сходів")
                svitlo_shodiv.switchOn().checkFirst().forSec(2).repeatAfterSec(1, 60)
                local i = 0
                while (i < 40) do
                        light.setRGB(255, 0, 0).afterSec(i)
                        i = i + 2
                        light.setRGB(0, 0, 255).afterSec(i)
                        i = i + 2
                end
                light.switchOff().afterSec(i + 1)
                sound.switchSelector(10);
                -- sound.switchOn().checkFirst();
                zvuk.dimTo(100)
                sound.switchOff().afterSec(90)
                zvuk.switchOff().afterSec(90)
            end
        end
	end
}