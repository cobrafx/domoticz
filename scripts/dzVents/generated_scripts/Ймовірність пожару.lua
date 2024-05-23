return {
	on = {
		devices = {
		    "Температура у кухні",
	        "Температура у ванній"
	    }
	},
	execute = function(domoticz, device)
	   local temp_kuhnya = domoticz.utils.round(domoticz.devices("Температура у кухні").temperature,1)
	   local temp_vanna = domoticz.utils.round(domoticz.devices("Температура у ванній").temperature,1)
       local zvuk = domoticz.devices("Xiaomi Gateway Volume")
       local sound = domoticz.devices("Xiaomi Gateway Alarm Ringtone")
       local light = domoticz.devices("Xiaomi RGB Gateway (192.168.0.9)")
       local alert_temperatura = 40.0

       local function telegram(msg)
          local bot_api = "1060079381:AAHlZvRxFpqeRIqp1nJBUexXScRpJWdBiWs"
          local chat_id = "-1001493931760"
          domoticz.openURL('https://api.telegram.org/bot' .. bot_api .. '/sendMessage?chat_id=' .. chat_id .. '&text=' .. msg) 
       end
	   
        if(temp_kuhnya >= alert_temperatura or temp_vanna >= alert_temperatura) then
            local msg = "УВАГА! Надзвичайно висока температура!!!"
            local body = ""
            if(temp_kuhnya >= alert_temperatura) then
                body = "Висока температура у кухні! Перевірте це будь ласка!"
            elseif(temp_vanna >= alert_temperatura) then
                body = "Висока температура у ванній! Перевірте це будь ласка!"
            end
            domoticz.email(msg, body, 'cobrafx@gmail.com')
            domoticz.email(msg, body, 'tetyana.holynska@gmail.com')
            telegram(msg)
            domoticz.log(msg)
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
            zvuk.dimTo(50)
            sound.switchOff().afterSec(90)
            zvuk.switchOff().afterSec(90)
        end

	end
}