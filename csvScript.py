import sys, os, csv
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

# Opens file in directory and uses beautiful soup to find the module Column
def printContent(fileArg):
	moduleCol = " "
	objectTypeCol = "temp"
	updateCol = " "
	objectNameCol = " "
	subobjectTypeCol = " "
	subObjectNameCol = " "
	with open(fileArg, 'r') as f:
		fileContents = f.read()

		soup = BeautifulSoup(fileContents, 'html.parser')

		tempModuleCol = soup.find(lambda tag:tag.name=="p" and "Product:" in tag.text)
		if tempModuleCol is None:
			return
		moduleCol = moduleColSplitter(tempModuleCol.text)

		for tr in soup.find_all('tr'):
			flag = 0;
			data = []
			data.append(moduleCol)
			data.append(objectTypeCol)
			for td in tr.find_all('td'):
				if(len(data) == 2 and flag == 0):
					objectNameCol = td.text.strip()
					flag = 1;
				elif(len(data) == 2 and flag == 1):
					updateCol = updateColSplitter(td.text.strip())
					data.append(updateCol)
					data.append(objectNameCol)
					flag = 0
				else:
					data.append("nop")
			if(len(data) > 2):
				csvWriter.writerow(data)

		print(moduleCol)


# Stome string manipulation to Parse and get correct productName
def moduleColSplitter(temp):
	moduleCol = temp[8:]
	tempModuleCol = moduleCol.split(" ", 1)
	moduleCol = tempModuleCol[0]
	return moduleCol

def updateColSplitter(change):
	updateCol = change.split(" ", 1)
	return updateCol[0] 





outFile = sys.argv[1] + "CSV.csv"
colHeaders = ["Module", "Object_Type", "Update", "Object_Name", 
	"Subobject_Type", "Subobject_Name"]
csvWriter = csv.writer(open(outFile, 'w'))
csvWriter.writerow(colHeaders)

# Gets commandLine Arg
# 
# Folder containing all relevant files must be in the same 
#	folder that the script is located
main(sys.argv[1])

csvWriter.close()