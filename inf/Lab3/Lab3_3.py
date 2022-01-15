import re
import sys

def repl(m):
	num = int(m[0])
	return str(3 * num ** 2 + 5)

def main(argv):
	inp = argv[1]
	print("INP: ", inp)
	print("RES: ", re.sub(r'-?\d+', repl, inp))

if __name__ == "__main__":
	main(sys.argv)
