return {
active = true,
on = {
devices = {'MiHome Ringtone'},
},
execute = function(domoticzfaq, switch);
local Dinamik = domoticzfaq.devices('Xiaomi Gateway MP3')
local Zvuk = domoticzfaq.variables('XiaomiMP3')
if (switch.changed)
then
Zvuk.set(switch.level + 10004)
-- Dinamik.switchOn().afterSec(3)
Dinamik.switchOn()
end
end 
}