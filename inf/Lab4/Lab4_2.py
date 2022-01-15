import xmltodict
# import oyaml
import sys

def convert(src, dst=sys.stdout):
    # oyaml.dump(xmltodict.parse(src.read()), dst)
    pass

if __name__ == "__main__":
    with open("Wednesday.xml", encoding="UTF-8") as src:
        with open("output2.yaml", encoding="UTF-8", mode="w") as dst:
            convert(src, dst)