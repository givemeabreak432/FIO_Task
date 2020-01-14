import PySimpleGUI as ui
from datetime import datetime

timeFormat = "%m/%d/%Y, %H:%M:%S"


class Reagent:
	reagentList = []
	reagentFile = "reagents.txt"

	def __init__(self, name,  quantity, timestamp, additionalProperties = []):
		self.name = name
		self.quantity = quantity
		self.timestamp = timestamp
		self.additionalProperties = additionalProperties


	#create new instance of reagent to save to list
	#returns false/true depending on if reagent was saved
	@staticmethod
	def newReagent(name, quantity, timestamp):
		name = name[0:25].replace(";","").replace("\\", "")
		if isinstance(Reagent.searchByName(name), Reagent) or name == "":
			return False

		reagent = Reagent(name, quantity, timestamp, [])
		Reagent.reagentList.append(reagent)	

		#append reagent to end of file list
		reagent.saveReagent()
		return True

	#delete reagent from list and document
	#returns false if unable to delete
	@staticmethod
	def deleteReagent(reagent):
		try:
			Reagent.reagentList.remove(reagent)
		except:
			return False

		f = open(Reagent.reagentFile, "r")	
		doc = ""	
		for line in f.read().split("\n"):
			s = line.split(';')
			if reagent.name != s[0]:
				doc = doc + line + "\n"
		f.close()
		f = open(Reagent.reagentFile, "w");
		f.write(doc)
		f.close()

		return True

	#startup static method. Reads in reagent file and starts reagentList
	@staticmethod
	def startup():
		try:
			f = open(Reagent.reagentFile)
		except IOError:
			f = open(Reagent.reagentFile, "w+") #createfile

		#populate reagent list on startup
		f = open(Reagent.reagentFile, "r")
		for line in f.read().split("\n"):
			s = line.split(";");
			if len(s) > 1:
				properties = []
				if len(s) > 4: #add additional properties if they exist
					i = 4
					while(True):
						try:
							if(s[i+1].isdigit()):
								properties.append([s[i], Quantity(s[i+1], s[i+2])])
								i = i + 3
							else:
								properties.append([s[i], s[i+1]])
								i = i + 2
						except:
							break

				Reagent.reagentList.append(Reagent(s[0], Quantity(s[1], s[2]), s[3], properties))

	#returns matchingReagents from reagentList
	#returns False if no reagents found
	@staticmethod
	def searchByName(name):
		for each in Reagent.reagentList:
			if each.name == name:
				return each
		return False


	#appends new reagent to end of text file
	def saveReagent(self):
		f = open(Reagent.reagentFile, "a")
		f.write(self.name + ";" + self.quantity.amount + ";" + self.quantity.unit + ";" + self.timestamp + "\n")
		f.close()

	def toText(self):
		outText = "Reagent: " + self.name + "\nQuantity: " + self.quantity.amount + " " + self.quantity.unit + "\nAdded: " + self.timestamp + "\n"
		for each in self.additionalProperties: 
			if(isinstance(each[1], Quantity)): #check if AdditionalProperty is a quantity
				outText = outText + each[0] + " " + each[1].toText() + "\n"
			else:
				outText = outText + each[0] + " " + each[1] + "\n"
		return outText

	#adds custom property to reagent, appends it to document
	def addProperty(self, key, value, unit):
		key = key[0:25].replace(";","").replace("\\", "")
		value = value[0:25].replace(";","").replace("\\", "")

		if(key == "" or value == ""):
			return False

		if(value.isdigit()):
			value = Quantity(value, unit)
		self.additionalProperties.append([key, value])

		f = open(Reagent.reagentFile, "r")
		doc = ""
		for line in f.read().split("\n"):
			s = line.split(";");
			if s[0] == self.name:
				if(isinstance(value, Quantity)):
					line = line + ";" + key + ";" + value.amount + ";" + value.unit
				else:
					line = line + ";" + key + ";" + value
			if(len(line) != 0): #prevents erroneous whitespace in txt doc
				doc = doc + line + "\n"
		f.close()
		f = open(Reagent.reagentFile, "w")
		f.write(doc)
		f.close()

		return True


#Quantity class for handling units. 
#Quantity is an amount paired with unit
#TODO: unit is currently a string rather than instance of Unit
class Quantity:
	def __init__(self, amount, unit):
		self.amount = amount
		self.unit = unit
	def toText(self):
		return self.amount + " " + self.unit

#TODO
#UNIT class
#measurement = what unit is measuring
#m = ratio of unit vs predefined base unit
#b = offset from base unit
#m = 1, b = 0 defines *base unit*.
#example: farenheit m = 1.8, b = 40 while celsius has m = 1, b = 0
class Unit:
	units = ["N/A", "uL", "x", "mM", "nM", "mg/mL", "U/uL", "U/uL"] 
	def __init__(self, name, measurement, m, b ):
		self.name = name
		self.measurement = measurement
		self.m = m
		self.b = b


#TODO class for drawing/managing window?
#Window for input of reagents
#takes message to display to user
def drawInput(message = ""):
	layout = [  [ui.Text(message)],
				[ui.Text("Enter Reagent Name", size = (20, 1)), ui.InputText()],
				[ui.Text("Enter Amount", size=(20, 1)), ui.InputText(), ui.InputCombo(Unit.units, readonly=True, default_value = Unit.units[0])],
	            [ui.Button('Save Reagent'), ui.Button('Close'), ui.Button('View List')]]

	window = ui.Window('Reagent', layout)

	windowManager(window)

#Window to view reagents
#TODO multiple reagents selectable at once. Seperate windows? Tables?
def drawReagentSelector(message = ""):
	#add reagent to list with index for selection
	reagentList = []
	for each in Reagent.reagentList:
		reagentList.append(each.name)

	layout = [[ui.Text(message)],
			 [ui.Listbox(reagentList, enable_events=True, select_mode = 'single', size = (30, 10))],
			 [ui.Button("View Reagent"), ui.Button("Add New Reagent")]]

	window = ui.Window('Reagent List', layout)

	windowManager(window)

#pass a reagent, displays information about reagent. 
def drawReagentProperties(reagent, message = ""):
	layout = [[ui.Text(reagent.toText())],
			 [ui.Button("View List"), ui.Button("Update Reagent"), ui.Button("Delete Reagent")]]

	window = ui.Window(reagent.name, layout)

	windowManager(window, reagent)

#update fields for adding new properties to reagent
def drawReagentUpdate(reagent, message = ""):
	layout = [  [ui.Text(message)],
				[ui.Text("Enter Property Name", size = (20, 1)), ui.InputText()],
				[ui.Text("Enter Value", size=(20, 1)), ui.InputText(), ui.InputCombo(Unit.units, readonly=True, default_value=Unit.units[0])],
	            [ui.Button('Save Property'), ui.Button('Close'), ui.Button('View Reagent')]]
	window = ui.Window(reagent.name, layout)

	windowManager(window, reagent)

def drawConfirmDelete(reagent):
	layout = [ [ui.Text("Are you sure you want to delete " + reagent.name)],
				[ui.Button("Yes"), ui.Button("No")]]
	window = ui.Window(reagent.name, layout)
	windowManager(window, reagent)

#detects button presses from current window
def windowManager(window, reagent = ""):
	while True:

		#Event Selector
	    event, values = window.read()

	    if event in (None, "Close"):
	        window.close()
	        break

	    if event in (None, "View List"):
	    	window.close()
	    	drawReagentSelector()
	    	break

	    if event in (None, "Add New Reagent"):
	    	window.close()
	    	drawInput()
	    	break


	    #Calls drawReagentProperties based on selected reagent.
	    #if no selected reagent, checks if there is previously selected reagent and draws that
	    if event in (None, "View Reagent"):
	    	if(len(values[0]) != 0):
	    		reagent = Reagent.searchByName(values[0][0])
	    	if(isinstance(reagent, Reagent)):
		    	window.close()
		    	drawReagentProperties(reagent)
		    	break

	    if event in (None, "Update Reagent"):
	    	window.close()
	    	drawReagentUpdate(reagent)
	    	break

	    if event in (None, "Delete Reagent"):
	    	window.close()
	    	drawConfirmDelete(reagent)
	    	break
	    if event in (None, "Yes"):
	    	window.close()
	    	Reagent.deleteReagent(reagent)
	    	drawReagentSelector()
	    	break

	    if event in (None, "No"):
	    	window.close()
	    	drawReagentProperties(reagent)
	    	break


	    #Check for valid quantity. 
	    #saves and timestamps new reagents
	    #redraws window to clear inputs
	    if event in (None, "Save Reagent"):
		    if values[1].isdigit():
		    	if not Reagent.newReagent(values[0], Quantity(values[1], values[2]), datetime.now().strftime(timeFormat)):
		    		window.close()
		    		drawInput("A Reagent with that name already exists")
		    		break
		    	text = values[0] + " saved!"
		    	window.close()
		    	drawInput(text)
		    	break

		    #Amount entered is invalid
		    else:
		    	window.close()
		    	drawInput("Entered amount must be a number")
		    	break

		#Saves additional property to reagent object
		#redraw window to clear inputs
		#property does not need to be a digit
	    if event in (None, "Save Property"):
    		window.close()
    		if reagent.addProperty(values[0], values[1], values[2]):
    			drawReagentUpdate(reagent, "Property Added!")
    		else:
    			drawReagentUpdate(reagent, "Do not leave any field blank")

if __name__ == "__main__":
	Reagent.startup()

	#default to input menu
	drawInput()