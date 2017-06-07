widget = {
    plugin = 'xkb',
    cb = function(t)
        if t.name == 'us' then
            return {full_text = ' \\En\\ ', color = '#9c9c9c'}
        elseif t.name == 'ru' then
            return {full_text = ' \\Ru\\ ', color = '#eab93d'}
        else
            return {full_text = ' \\' .. t.name .. '\\ '}
        end
    end,
}
