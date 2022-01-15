import sys
import re

def main(argv):
	inp = argv[1]
	res = re.sub(r'(?<!:)((?:[0-1][0-9]|2[0-4])(?::[0-5][0-9]|60){1,2})(?!:)', '(TBD)', inp)
	print("INP = ", inp)
	print("RES = ", res)

if __name__ == "__main__":
	main(sys.argv)
