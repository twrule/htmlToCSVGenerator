import sys

def main(filePath):
	print("Hello World")
	print(filePath)
	f = open("../../../Desktop/12.1.3_12.2.9/12.1.3_12.2.9_products.txt", "r")
	print(f.read())

main(sys.argv[1])