import re
import pprint


def raw(format_string):
    """Replace based irc formatting"""
    stuff = {'col': {'white': '\x030',
                     'black': '\x031',
                     'dblue': '\x032',
                     'dgreen': '\x033',
                     'red': '\x034',
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
                     'lgray': '\x0315', },  # Colours are separate because the text can only have one of them at a time.
             'style': {'b': '\x02',
                       'clear': '\x0f'},  # These are states that can be toggled.
             'sym': {'[point]': '\x07'},  # I'll add these back at some point
             'text': {'[url]': 'http://'}}  # See above

    states = [{'col': "", 'add': [], 'cancel': [], 'ncancel': [], 'pos': (0, 0)}]  # A vanilla state.
    tags = re.finditer(r"\[/?\w+\]", format_string)  # Finds all instances of [x] and [/x] that are one word.
    for x in tags:
        curstate = dict(states[-1])
        curstate['cancel'] = curstate['ncancel']
        curstate['ncancel'] = []
        text = x.group()[1:-1]  # Take out the brackets
        end = 0
        curstate['pos'] = x.span()
        if text[0] == "/":  # check if the tag is a closing one
            end = 1
            text = text[1:]
        if text in stuff['col'] and end == 0:  # Opening colour tag
            curstate['col'] = text
        elif text in stuff['col'] and end == 1:  # Closing colour tag
            for st in states[::-1]:  # Find what colour was set before
                if st['col'] != text:
                    curstate['col'] = st['col']
        elif end == 0:
            curstate['add'].append(text)  # Add the tag to the list of active tags
            if text in curstate['cancel']:  # Remove it from the cancel list
                curstate['cancel'].remove(text)
        elif end == 1 and text in curstate['add']:  # Remove it from the active list
            curstate['cancel'].append(text)
            if text in curstate['add']:
                curstate['add'].remove(text)
        states.append(curstate)  # Add this state to the list of states to be processed.
    if __name__ == "__main__":
        print pprint.pprint(states)
    for x in states[::-1]:  # Apply formatting from the end
        state = ""
        if x['col']:  # Does the current state require colour formatting?
            state += stuff['col'][x['col']]
        else:
            state += '\x0f'  # We can only use this code because other formatting is applied after this point.
        for y in x['add']:  
            state += stuff['style'][y]
        for y in x['cancel']:
            state += stuff['style'][y]
        format_string = format_string[:x['pos'][0]] + state + format_string[x['pos'][1]:]  # Should probably regex.
        #format_string = re.sub(r"\[/?\w+\]", state, format_string)
    return format_string


def err(format_string):
    """Format the string with standard error styling"""
    return "\x034\x02{}\x0f".format(format_string)

if __name__ == "__main__":
    print raw("This text is [dgreen]green[/dgreen] while this [red]red[/red] word is [b]bold[/b] butts blah blah blah")