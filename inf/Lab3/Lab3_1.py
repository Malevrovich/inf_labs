import re
import sys

def main(argv):
	inp = argv[1]

	print("INP: ", inp)
	print("RES: ", len(re.findall(r';-{\(', inp)))

if __name__ == "__main__":
	main(sys.argv)
	__a__ = 1
	print(__a__)

#TESTS
#;-{( abs;-{(  ;-}( :+;{ ;--{(;;-{(;-{(  ::;-{()( => 5
#;-{( => 1
#;;--{{(( => 0
#"" => 0
#;:;-{()  ;-{) => 1
#i'm sad... ;-{( i'm happy ;-{) => 1
