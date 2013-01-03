def lexPath(d):
    """
    returns an iterator that breaks path data
    identifies command and parameter tokens
    """
    import re

    offset = 0
    length = len(d)
    delim = re.compile(r'[ \t\r\n,]+')
    command = re.compile(r'[MLHVCSQTAZmlhvcsqtaz]')
    parameter = re.compile(r'(([-+]?[0-9]+(\.[0-9]*)?|[-+]?\.[0-9]+)([eE][-+]?[0-9]+)?)')
    while 1:
        m = delim.match(d, offset)
        if m:
            offset = m.end()
        if offset >= length:
            break
        m = command.match(d, offset)
        if m:
            yield [d[offset:m.end()], True]
            offset = m.end()
            continue
        m = parameter.match(d, offset)
        if m:
            yield [d[offset:m.end()], False]
            offset = m.end()
            continue
        #TODO: create new exception
        raise Exception, _('Invalid path data!')
'''
While I am less pleased with my parsing function, I think it works. And that
is important. There will be time for improvement later.
'''

'''
pathdefs = {commandfamily:
    [
    implicitnext,
    #params,
    [casts,cast,cast],
    [coord type,x,y,0]
    ]}
'''

pathdefs = {
    'M':['L', 2, [float, float], ['x','y']],
    'L':['L', 2, [float, float], ['x','y']],
    'H':['H', 1, [float], ['x']],
    'V':['V', 1, [float], ['y']],
    'C':['C', 6, [float, float, float, float, float, float], ['x','y','x','y','x','y']],
    'S':['S', 4, [float, float, float, float], ['x','y','x','y']],
    'Q':['Q', 4, [float, float, float, float], ['x','y','x','y']],
    'T':['T', 2, [float, float], ['x','y']],
    'A':['A', 7, [float, float, float, int, int, float, float], [0,0,0,0,0,'x','y']],
    'Z':['L', 0, [], []]
    }

def parsePath(d):
    """
    Parse SVG path and return an array of segments.
    Removes all shorthand notation.
    Converts coordinates to absolute.
    """
    retval = []
    lexer = lexPath(d)

    pen = (0.0,0.0)
    subPathStart = pen
    lastControl = pen
    lastCommand = ''

    while 1:
        try:
            token, isCommand = lexer.next()
        except StopIteration:
            break
        params = []
        needParam = True
        if isCommand:
            if not lastCommand and token.upper() != 'M':
                raise Exception, _('Invalid path, must begin with moveto.')
            else:
                command = token
        else:
            #command was omited
            #use last command's implicit next command
            needParam = False
            if lastCommand:
                if token.isupper():
                    command = pathdefs[lastCommand.upper()][0]
                else:
                    command = pathdefs[lastCommand.upper()][0].lower()
            else:
                raise Exception, _('Invalid path, no initial command.')
        numParams = pathdefs[command.upper()][1]
        while numParams > 0:
            if needParam:
                try:
                    token, isCommand = lexer.next()
                    if isCommand:
                        raise Exception, _('Invalid number of parameters')
                except StopIteration:
                        raise Exception, _('Unexpected end of path')
            cast = pathdefs[command.upper()][2][-numParams]
            param = cast(token)
            if command.islower():
                if pathdefs[command.upper()][3][-numParams]=='x':
                    param += pen[0]
                elif pathdefs[command.upper()][3][-numParams]=='y':
                    param += pen[1]
            params.append(param)
            needParam = True
            numParams -= 1
        #segment is now absolute so
        outputCommand = command.upper()

        #Flesh out shortcut notation
        if outputCommand in ('H','V'):
            if outputCommand == 'H':
                params.append(pen[1])
            if outputCommand == 'V':
                params.insert(0,pen[0])
            outputCommand = 'L'
        if outputCommand in ('S','T'):
            params.insert(0,pen[1]+(pen[1]-lastControl[1]))
            params.insert(0,pen[0]+(pen[0]-lastControl[0]))
            if outputCommand == 'S':
                outputCommand = 'C'
            if outputCommand == 'T':
                outputCommand = 'Q'

        #current values become "last" values
        if outputCommand == 'M':
            subPathStart = tuple(params[0:2])
        if outputCommand == 'Z':
            pen = subPathStart
        else:
            pen = tuple(params[-2:])

        if outputCommand in ('Q','C'):
            lastControl = tuple(params[-4:-2])
        else:
            lastControl = pen
        lastCommand = command

        retval.append([outputCommand,params])
    return retval


