import Parse
import Serialize
import sys

def printTag(tag, deep=1):
    """
    Prints tag
    """

    print("| "*(deep - 1) + "+ ", end="")
    print(f"{tag.name} : {[(x[0], x[1]) for x in tag.attrs.items()]}, {tag.value}")
    
    for i in tag.children:
        printTag(i, deep + 1)

def convert(src, dst=sys.stdout):
    """
    Converts from xml to yaml
    """
    root = Parse.parse(src.read())
    for i in root.children:
        Serialize.print_tag(i, dst=dst)

if __name__ == "__main__":
    with open("Wednesday.xml", encoding="UTF-8") as src:
        with open("output1.yaml", encoding="UTF-8", mode="w") as dst:
            convert(src, dst)