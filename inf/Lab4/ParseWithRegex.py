import re

class Tag:
    def __init__(self, name="!!unnamed!!", children=None, attrs=None, value=None, parent=None):
        self.name = name
        self.children = [] if children is None else children
        self.attrs = {} if attrs is None else attrs
        self.value = value
        self.parent = parent

reg_attr_key = re.compile(r'\w+(?==)')
reg_attr_value = re.compile(r'(?<=").*(?=")') 

def extract_key_value(s):
    return reg_attr_key.search(s).group(0), reg_attr_value.search(s).group(0)

reg_attrs = re.compile(r'[\w_:][\w_\-.:]+=".*"')

def parse_attrs(s):
    match = reg_attrs.match(s)
    res = {}

    while match is not None:
        key, value = extract_key_value(match.group(0))
        res[key] = value

        s = s[match.end():].lstrip()
        match = reg_attrs.match(s)
    return res, s

reg_open_tag = re.compile(r'<\w+')
reg_end_of_tag = re.compile(r'>|\/>')
reg_closing_tag = re.compile(r'<\/\w+>')
reg_first_tag = re.compile(r'<\?.*\?>')
reg_value = re.compile(r'[^<>]*')
reg_comment = re.compile(r'<!--.*-->')

def parse(s, root=None):
    root = Tag() if root is None else root
    cur = root

    first_tag = reg_first_tag.match(s)
    if first_tag is not None:
        s = s[first_tag.end():].lstrip()
    
    while True:
        s = s.lstrip()
        open_tag = reg_open_tag.match(s)

        if open_tag is not None:
            if cur.value is not None:
                print("Expected closing tag")
                exit(-1)

            name = open_tag.group(0)[1:]
            s = s[open_tag.end(): ].lstrip()

            attrs, s = parse_attrs(s)

            if s[0] != '>':
                if s[0:2] == '\>':
                    tmp = Tag(name, attrs=attrs, parent=cur)
                    cur.children.append(tmp)
                    
                    s = s[2:].lstrip()
                    continue
                else: 
                    print(s)
                    print("Expected end of tag")
                    exit(-1)

            s = s[1:].lstrip()

            tmp = Tag(name, attrs=attrs, parent=cur)
            cur.children.append(tmp)
            cur = tmp
            
            continue

        closing_tag = reg_closing_tag.match(s)
        if closing_tag is not None:
            name = closing_tag.group(0)[2:-1]

            s = s[closing_tag.end():].lstrip()
            
            if name != cur.name:
                print("Wrong closing tag")
                exit(-1)
            
            cur = cur.parent
            continue
        
        value = reg_value.match(s)
        if value is not None and value.group(0).strip() != '':
            if cur.children:
                print("Expected tag not value")
                exit(-1)
            
            cur.value = value.group(0)
            s = s[value.end():]
            
            continue

        comment = reg_comment.match(s)
        if comment is not None:
            s = s[comment.end():].lstrip()
            
            continue
        break
    return root