import sys
import functools
from Parse import Tag

def add_spaces_to_begin(deep, dst, func, *args, **kwargs):
    def res(*args, **kwargs):
        print('  ' * deep, end='', file=dst)
        func(*args, **kwargs)
    return res

def print_tag(tag, deep=0, dst=sys.stdout, with_name=True):
    print_some = functools.partial(print, file=dst)
    print_with_space = add_spaces_to_begin(deep, dst, print_some)

    # Print tag name
    if with_name:
        print_with_space(f"{tag.name}:", end=' ')
    else:
        print_with_space(" -", end=' ')

    if not tag.attrs and not tag.children:
        print_some(tag.value)
        return
    else:
        print_some()

    # Print attrs
    for key, value in tag.attrs.items():
        print_with_space(f"  {key}: {value}")
    
    # Print value
    if tag.value is not None:
        print_with_space(f"  value: {tag.value}")

    # Print children
    children = sorted(tag.children, key=lambda x: x.name)

    for i in range(len(children)):
        if i != 0 and children[i - 1].name == children[i].name:
            print_tag(children[i], deep + 1, dst, False)
        elif i + 1 < len(children) and children[i + 1].name == children[i].name:
            print_with_space(f"  {children[i].name}:")
            print_tag(children[i], deep + 1, dst, False)
        else:
            print_tag(children[i], deep + 1, dst, True)
