import PySimpleGUI as ui
from datetime import datetime

timeFormat = "%m/%d/%Y, %H:%M:%S"

#TODO make reagents more modulable for data
#TODO handle duplicate reagent names. 
class Reagent:
	reagentList = []
	reagentFile = "reagents.txt"

	def __init__(self, name,  quantity, timestamp):
		self.name = name
		self.quantity = quantity
		self.timestamp = timestamp
		self.additionalProperties = []


	#create new instance of reagent to save to list
	#TODO clean string (remove delimiters)
	@staticmethod
	def newReagent(name, quantity, timestamp):
		reagent = Reagent(name, quantity, timestamp)
		Reagent.reagentList.append(reagent)

		#append reagent to end of file list
		reagent.saveReagent()

	#startup static method. Reads in reagent file and starts reagentList
	#TODO additionalProperties storage
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
				Reagent.reagentList.append(Reagent(s[0], Quantity(s[1], s[2]), s[3]))

	#returns matchingReagents from reagentList
	#TODO handle duplicate names
	@staticmethod
	def searchByName(name):
		for each in Reagent.reagentList:
			if each.name == name:
				return each


	#saves reagent to text document
	def saveReagent(self):
		f = open(Reagent.reagentFile, "a")
		f.write(self.name + ";" + self.quantity.amount + ";" + self.quantity.unit + ";" + self.timestamp + "\n")
		f.close()
	#append reagent
	def appendReagent(self):
		pass

	def toText(self):
		return "Reagent: " + self.name + "\nQuantity: " + self.quantity.amount + " " + self.quantity.unit + "\nAdded: " + self.timestamp

	#TODO save add additionalProperties to document. 
	def addProperty(key, value):
		self.additionalProperties.append[[key, value]]

	def addProperty(list):
		self.additionalProperties.append[list[0:1]]

#Quantity class for handling units. 
#Quantity is an amount paired with unit
#TODO: unit is currently a string rather than instance of Unit
class Quantity:
	def __init__(self, amount, unit):
		self.amount = amount
		self.unit = unit

#TODO
#UNIT class
#measurement = what unit is measuring
#m = ratio of unit vs predefined base unit
#b = offset from base unit
#m = 1, b = 0 defines *base unit*.
#example: farenheit m = 1.8, b = 40 while celsius has m = 1, b = 0
class Unit:
	units = ["uL", "x", "mM", "nM", "mg/mL", "U/uL", "U/uL"] 
	def __init__(self, name, measurement, m, b ):
		self.name = name
		self.measurement = measurement
		self.m = m
		self.b = b



def main():
	Reagent.startup()

	#default to input menu
	drawInput()

#TODO class for drawing/managing window?
#Window for input of reagents
#takes message to display to user
def drawInput(message = ""):
	layout = [  [ui.Text(message)],
				[ui.Text("Enter Reagent Name", size = (20, 1)), ui.InputText()],
				[ui.Text("Enter Amount", size=(20, 1)), ui.InputText(), ui.InputCombo(Unit.units)],
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
			 [ui.Button("View List"), ui.Button("Update Reagent")]]

	window = ui.Window(reagent.name, layout)

	windowManager(window)

#update fields for amending reagent data
def drawReagentUpdate(reagent, message = ""):
	pass

#detects button presses from current window
def windowManager(window):
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

	    #find reagent based on reagent name. send it 
	    if event in (None, "View Reagent"):
	    	window.close()
	    	drawReagentProperties(Reagent.searchByName(values[0][0]))
	    #Amount entered is valid
	    #saves and timestamps new reagents
	    if event in (None, "Save Reagent"):
		    if values[1].isdigit():
		    	Reagent.newReagent(values[0], values[1], "NA", datetime.now().strftime(timeFormat))
		    	text = values[0] + " saved!"
		    	window.close()
		    	drawInput(text)

		    #Amount entered is invalid
		    else:
		    	window.close()
		    	drawInput("Entered amount must be a number")

if __name__ == "__main__":
	main()