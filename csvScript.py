import sys, os
import requests
from bs4 import BeautifulSoup

def main(filePath):
	directory = filePath

	# Gets pwd of current directory and adds directory to it
	dir_path = os.getcwd() + "/" + directory + "/"
	# Creates a list of everything in the directory
	dir_list = os.listdir(directory)

	# iterates through every file in the directory
	for file in dir_list[1:]:
		printContent(dir_path + file)

#prints content of specific file
def printContent(fileArg):
	with open(fileArg, 'r') as f:
		f_contents = f.read()
		print(f_contents)

outFileName = sys.argv[1] + "CSV.csv"

outFile = open(outFileName, 'w')
outFile.write("dog")
# Gets commandLine Arg
# 
# Folder containing all relevant files must be in the same 
#	folder that the script is located
main(sys.argv[1])
outFile.write("cat\n")
outFile.close()