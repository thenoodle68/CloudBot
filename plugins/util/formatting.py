import re


def raw(format_string):
    """Replace based irc formatting"""
    stuff = {'col': {'white': '\x030',
                     'black': '\x031',
                     'dblue': '\x032',
                     'dgreen': '\x033',
                     'dred': '\x034',
                     'brown': '\x035',
                     'purple': '\x036',
                     'gold': '\x037',
                     'yellow': '\x038',
                     'green': '\x039',
                     'cyan': '\x0310',
                     'lblue': '\x0311',
                     'blue': '\x0312',
                     'pink': '\x0313',
                     'gray': '\x0314',
                     'lgray': '\x0315',},
             'style': {'b': '\x02',
                       'clear': '\x0f'},
             'sym': {'[point]': '\x07'},
             'text': {'[url]': 'http://'}}
    final = {}
    for x in stuff:
        final.update(stuff[x])

    states = [{'col': "", 'add': [], 'cancel': [], 'pos': (0, 0)}]
    tags = re.finditer(r"\[/?\w+\]", format_string)
    for x in tags:
        curstate = dict(states[-1])
        text = x.group()[1:-1]
        end = 0
        curstate['pos'] = x.span()
        if text[0] == "/":
            end = 1
            text = text[1:]
        if text in stuff['col'] and end == 0:
            curstate['col'] = text
        elif text in stuff['col'] and end == 1:
            for st in states[::-1]:
                if st['col'] != text:
                    curstate['col'] = text
        elif end == 0:
            curstate['add'].append(text)
            if text in curstate['cancel']:
                curstate['cancel'].remove(text)
        elif end == 1 and text in curstate['add']:
            curstate['cancel'].append(text)
            if text in curstate['add']:
                curstate['add'].remove(text)
        states.append(curstate)

    for x in states[::-1]:
        state = ""
        if x['col']:
            state += stuff['col'][x['col']]
        for y in x['add']:
            state += stuff['style'][y]
        for y in x['cancel']:
            state += stuff['style'][y]
        format_string = format_string[:x['pos'][0]] + state + format_string[x['pos'][1]:]
        #for x in final:
    #    format_string = format_string.replace(x, final[x])
    return format_string


def err(format_string):
    """Format the string with standard error styling"""
    return "\x034\x02{}\x0f".format(format_string)