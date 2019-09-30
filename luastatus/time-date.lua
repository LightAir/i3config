months = {'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'}

widget = {
    plugin = 'timer',
    cb = function()
        local d = os.date('*t')
        return {
            {full_text = string.format(' %d %s', d.day, months[d.month]), color = '#dc8ca3'},
            {full_text = string.format(' %d:%02d', d.hour, d.min), color = '#dc8ca3'},
        }
    end,
    event = function(t)
        if t.button == 1 then     -- left mouse button
            os.execute('urxvt -e calcurse &')
        end
    end
}
