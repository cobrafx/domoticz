return {
	on = {
		devices = {
	        "Powmr - Operation Mode"
	    }
	},
	execute = function(domoticz, device)


        local function telegram(msg)
            local bot_api = "1060079381:AAHlZvRxFpqeRIqp1nJBUexXScRpJWdBiWs"
            local chat_id = "-1001493931760"
            domoticz.openURL('https://api.telegram.org/bot' .. bot_api .. '/sendMessage?chat_id=' .. chat_id .. '&text=' .. msg) 
        end

	   local power = domoticz.devices("Powmr - Operation Mode")
	   local msg_power_off = "Пропало живлення будинку! Включено резерв!"
	   local msg_power_on = "Відновилось живлення будинку!"

        -- power.dump()

        if(power.nValue == 0) then
           domoticz.notify("Живлення", msg_power_off, domoticz.PRIORITY_HIGH)
           domoticz.log(msg_power_off)
           telegram(msg_power_off)
        else
            domoticz.notify("Живлення", msg_power_on, domoticz.PRIORITY_HIGH)
            domoticz.log(msg_power_on)
            telegram(msg_power_on)
        end

	end
}