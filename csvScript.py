import sys, os

def main(filePath):
	directory = filePath

	dir_path = os.getcwd() + "/" + directory
	dir_list = os.listdir(directory)

	for file in dir_list:
		printContent(dir_path + "/" + file)

def printContent(fileArg):
	with open(fileArg, 'r') as f:
		f_contents = f.read()
		print(f_contents)

main(sys.argv[1])