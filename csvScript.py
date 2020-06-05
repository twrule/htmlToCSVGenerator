import sys, os, csv, re
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
		print("Currently Working on " + file + " file.")
		nzdCheck = nzdChecker(file)
		printContent(dir_path + file, nzdCheck)

# Opens file in directory and uses beautiful soup to find the module Column
def printContent(fileArg, nzdCheck):
	moduleCol = " " # This is Working
	objectTypeCol = "temp" # This is Working
	updateCol = " " # This is Working
	objectNameCol = " " # This is Working
	subobjectTypeCol = "" # Needs Work
	subobjectNameCol = "" # Needs Workd

	with open(fileArg, 'r') as f:
		fileContents = f.read()

		soup = BeautifulSoup(fileContents, 'html.parser')

		# Gets the appropriate module column data
		tempModuleCol = soup.find(lambda tag:tag.name=="p" and "Product:" 
			                      in tag.text)
		if tempModuleCol is None:
			return
		moduleCol = moduleColSplitter(tempModuleCol.text, nzdCheck)

		# Begins iterating through tables
		for tr in soup.find_all('tr'):

			# Gets appropriate object_type column data
			objTyList = []
			for th in tr.find_all('th'):
				objTyList.append(th.text)
			if(len(objTyList) > 0):
				objectTypeCol = objTyList[0].replace(" ", "_")

			# flag used for appending columns in the correct order
			flag = 0;
			data = []
			data.append(moduleCol)
			data.append(objectTypeCol)

			for td in tr.find_all('td'):
				if(len(data) == 2 and flag == 0):
					objectNameCol = td.text.strip()
					flag = 1;
				elif(len(data) == 2 and flag == 1):
					updateColChecker = updateColSplitter(td.text.strip())
					# If we get into below if statement that means there are
					#   subobjects and whatnot.  Must get a recursive-type
					#   function going and also empty data becuase everything
					#   will be appended in the recursive section and don't
					#   want it to do duplicate work
					if(len(updateColChecker) > 3):
						if(updateColChecker[1].strip() == "Changes"):
							updateCol = "Changed"
							subobjectTypeParser(td, moduleCol, 
								objectTypeCol, updateCol, objectNameCol)
							del data[:]

						else:
							updateCol = updateColChecker[1]
							subobjectTypeParser(td, moduleCol, 
								objectTypeCol, updateCol, objectNameCol)
							del data[:]
					else:
						updateCol = updateColChecker[0]
					data.append(updateCol)
					data.append(objectNameCol)
					flag = 0
			if(len(data) > 2):
				data.append(subobjectTypeCol)
				data.append(subobjectNameCol)
				csvWriter.writerow(data)


def nzdChecker(fileName):
	if("nonNZD" in fileName):
		return 1
	return 0;

# Stome string manipulation to Parse and get correct productName
def moduleColSplitter(temp, nzdCheck):
	moduleCol = temp[8:]
	tempModuleCol = moduleCol.split(" ", 1)
	moduleCol = tempModuleCol[0]
	if(nzdCheck == 0):
		moduleCol += "_NZD"
	else:
		moduleCol += "_nonNZD"

	return moduleCol

def updateColSplitter(change):
	updateCol = change.split(" ")
	return updateCol

def subobjectTypeParser(phrase, moduleCol, 
						objectTypeCol, updateCol, objectNameCol):
	subobjectType, subobjectName = "", ""
	# used for added/removed/changed etc
	newUpdateList = phrase.find_all('font', style="color: rgb(58, 90, 135); font-weight: bold;")
	# used for string parsing
	newUpdatePhrase = phrase.find_all('font', style="color: rgb(58, 90, 135); font-weight: bold;")

	for i in range(len(newUpdatePhrase)):
		newUpdatePhrase[i] = newUpdatePhrase[i].text

	for i in range(len(newUpdateList)):
		newUpdateList[i] = newUpdateList[i].text.strip()
		temp = newUpdateList[i].split(" ", 2)
		if(len(temp) > 1):
			newUpdateList[i] = temp[1]
		else:
			newUpdateList = temp[0]

	subObjectTypeList = phrase.find_all('strong')
	for i in range(len(subObjectTypeList)):
		subObjectTypeList[i] = subObjectTypeList[i].text.strip()

	phrase = phrase.text.strip()
	
	updateCol = newUpdateList[0]
	subobjectType = subObjectTypeList[0]

	while(len(subObjectTypeList) > 0):
		lenCheck = len(subobjectType)

		updateLoc = 0

		for i in range(len(newUpdatePhrase)):
			temperer = newUpdatePhrase[i]
			newer = len(temperer)

			temp = phrase.find(newUpdatePhrase[i])
			if(temp > updateLoc):
				updateLoc = temp

			if(len(phrase) > newer and phrase[:newer] == newUpdatePhrase[i]):
				updateCol = newUpdateList[i]
				phrase = phrase[newer:]

		if(len(subObjectTypeList) > 1):
			phrase = phrase[len(subObjectTypeList[0])+1:].strip()
			figure = phrase.find(subObjectTypeList[1])
			if(figure < updateLoc):
				subobjectName = phrase[:figure]
			else:
				subobjectName = phrase[:updateLoc]
			if(figure > updateLoc):
				phrase = phrase[figure:]
			else:
				phrase = phrase[updateLoc:]
		else:
			phrase = phrase[len(subObjectTypeList[0]) + 1:].strip()
			subobjectName = phrase

		subObjectType = subObjectTypeList[0]
		if("Att" in subobjectName):
			subobjectName = subobjectName[:-3]

		data = [moduleCol, objectTypeCol, updateCol, objectNameCol]
		data.append(subObjectType)
		data.append(subobjectName)

		csvWriter.writerow(data)
		subObjectTypeList.remove(subObjectTypeList[0])
		updateLoc = 0




outFile = sys.argv[1] + "CSV.csv"
colHeaders = ["Module", "Object_Type", "Update", "Object_Name", 
	"Subobject_Type", "Subobject_Name"]
csvWriter = csv.writer(open(outFile, 'w'))
csvWriter.writerow(colHeaders)

# calls main methon using commandLine Arg
main(sys.argv[1])

csvWriter.close()