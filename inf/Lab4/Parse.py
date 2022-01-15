class Tag:
    def __init__(self, name="!!unnamed!!", children=None, attrs=None, value=None, parent=None):
        self.name = name
        self.children = [] if children is None else children
        self.attrs = {} if attrs is None else attrs
        self.value = value
        self.parent = parent
        
def check_len(s, c):
    if c >= len(s):
        print("Unexpected end of file")
        exit(-1)

def parse_name(s, c):
    res = ""

    if not s[c].isalpha() and s[c] not in ('_', ':'):
        print("Expected name")
        exit(-1)

    while s[c].isalpha() or s[c].isnumeric() or s[c] in ('_', '-', '.', ':'):
    
        check_len(s, c)
    
        res += s[c]
        c += 1

    return res, c

def parse_attr_value(s, c):
    res = ""

    while s[c] not in ('<', '>', '"', '&'):

        check_len(s, c)

        res += s[c]
        c += 1
    
    return res, c

def parse_anchor(s, c):
    res = ""
    if s[c] == '#':
        # num
        
        res += s[c]
        c += 1
        check_len(s, c)
        
        if s[c].tolower() == 'x':
            # hex

            res += s[c]
            c += 1
            check_len(s, c)
            
            while s[c].isnumeric() or s[c].tolower() in ['a', 'b', 'c', 'd', 'e', 'f']:
                res += s[c]
                c += 1
                check_len(s, c)
        else:
            # dec
            
            while s[c].isnumeric():
            
                res += s[c]
                c += 1
                check_len(s, c)
    else:
        t = 0
        if c + 2 < len(s) and (s[c:c+2] == 'lt' or s[c:c+2] == 'gt'):
            t = 2
        if c + 3 < len(s) and s[c:c+3] == 'amp':
            t = 3
        if c + 4 < len(s) and (s[c:c+4] == 'apos' or s[c:c+4] == 'quot'):
            t = 4
        
        if t == 0:
            print("Wrong anchor!")
            exit(-1)

        res += s[c:c+t] 
        c += t
        check_len(s, c)
    
    if s[c] != ';':
        print("Expected ';' at end of anchor")
        exit(-1)
    
    res += s[c]
    c += 1

    return res, c

def parse_value(s, c):
    res = ""

    while s[c] not in ('<', '>'):

        check_len(s, c)

        if s[c] == '&':
            # Anchor

            res += s[c]
            c += 1
            check_len(s, c)

            tmp, c = parse_anchor(s, c)
            res += tmp
        else:
            res += s[c]
            c += 1

    return res, c

def parse_attr(s, c):
    key, c = parse_name(s, c)
    
    if s[c] != '=':
        print("Expected '='")
        exit(-1)
    c += 1

    if s[c] != '"':
        print("Expected start of value")
        exit(-1)
    c += 1

    value, c = parse_attr_value(s, c)
    
    if s[c] != '"':
        print("Expected end of attr value")
        exit(-1)
    c += 1

    return key, value, c

def parse_not_closing_tag(s, c):
    name, c = parse_name(s, c)

    tmp = Tag(name=name)
    
    empty = False
    while s[c].isspace():
        while s[c].isspace():
            c += 1

        if s[c] == '/':
            # Empty tag
            
            c += 1
            empty = True
            break
        key, value, c = parse_attr(s, c)

        if key in tmp.attrs.keys():
            print("Two or more equal attributes!")
            exit(-1)
        
        tmp.attrs[key] = value

    if s[c] != '>':
        print("Expected end of tag at tag ", tmp.name)
        exit(-1)
    c += 1

    return tmp, empty, c

def parse_comment(s, c):
    while s[c:c+3] != '-->':
        if c > len(s) - 3:
            print("Unexpected end of file")
            exit(-1)
        c += 1
    c += 3
    return c

def parse_first_tag(s, c):
    while s[c] != '?':
        check_len(s, c)
        c += 1
    if s[c + 1] != '>':
        print("Expected end of first tag")
        exit(-1)
    return c + 2

def parse(s, root=None, c=0):
    root = Tag() if root is None else root
    cur = root

    while c < len(s):
        if s[c].isspace():

            c += 1
            continue

        elif s[c] == '<':
            if s[c+1:c+4] == '!--':
                # Comment

                c += 4
                c = parse_comment(s, c)

            elif s[c+1] == '/':
                # Closing tag
                
                c += 2
                name, c = parse_name(s, c)

                if s[c] != '>':
                    print("Expected '>' at closing tag ", name)
                    exit(-1)
                
                if name != cur.name:
                    print("Wrong closing tag")
                    exit(-1)             

                cur = cur.parent
                c += 1

            elif c == 0 and s[c + 1] == '?':
                # First tag

                c += 2
                c = parse_first_tag(s, c)

            else:
                # Opening or empty tag
                c += 1
                
                tmp, empty, c = parse_not_closing_tag(s, c)
                tmp.parent = cur
                
                cur.children.append(tmp)

                if not empty:
                    cur = tmp

        elif s[c] != '>':
            # Parse tag value if expected

            if cur == root:
                print("Expected tag before value")
                exit(-1)
            
            value, c = parse_value(s, c)
            cur.value = value
        else:
            print("Unexpected symbol", s[c], "at", c)
            exit(-1)
    return root