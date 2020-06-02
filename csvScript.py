import sys, os
from bs4 import BeautifulSoup

def main(filePath):
	directory = filePath

	# Gets pwd of current directory and adds directory to it
	dir_path = os.getcwd() + "/" + directory + "/"
	# Creates a list of everything in the directory
	dir_list = os.listdir(directory)

	dir_list.sort()

	# iterates through every file in the directory
	# when I run on my computer must start at second index, 0 index 
	# 	is .DS_Store and 1 index is .txt
	for file in dir_list[2:]:
		printContent(dir_path + file)

# Opens file in directory and uses beautiful soup to find the productCol row
def printContent(fileArg):
	with open(fileArg, 'r') as f:
		fileContents = f.read()

		soup = BeautifulSoup(fileContents, 'html.parser')

		tempProductCol = soup.find(lambda tag:tag.name=="p" and "Product:" in tag.text)
		if tempProductCol is None:
			return
		productCol = productColSplitter(tempProductCol.text)

		print(productCol)


# Stome string manipulation to Parse and get correct productName
def productColSplitter(temp):
	productCol = temp[8:]
	productCols = productCol.split(" ", 1)
	productCol = productCols[0]
	return productCol







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