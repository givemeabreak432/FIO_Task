import PySimpleGUI as ui
from datetime import datetime

units = ["uL", "x", "mM", "nM", "mg/mL", "U/uL", "U/uL"] #TODO make into seperate file to allow for more units/custom units
timeFormat = "%m/%d/%Y, %H:%M:%S"

#TODO make reagents more modulable for data
class Reagent:
	reagentList = []
	reagentFile = "reagents.txt"

	def __init__(self, name, amount, unit, timestamp):
		self.name = name
		self.amount = amount
		self.unit = unit
		self.timestamp = timestamp


	#create new instance of reagent to save to list
	@staticmethod
	def newReagent(name, amount, unit, timestamp):
		reagent = Reagent(name, amount, unit, timestamp)
		Reagent.reagentList.append(reagent)

		#append reagent to end of file list
		reagent.saveReagent()

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
				Reagent.reagentList.append(Reagent(s[0], s[1], s[2], s[3]))

	#saves reagent to text document
	def saveReagent(self):
		f = open(Reagent.reagentFile, "a")
		f.write(self.name + ";" + self.amount + ";" + self.unit + ";" + self.timestamp + "\n")
		f.close()

	def toText(self):
		return self.name + ": " + self.amount + self.unit + " | " + self.timestamp

def main():
	Reagent.startup()

	#default to input menu
	drawInput()

#TODO class for drawing/managing window?
#Window for input of reagents
#takes message to display to user
def drawInput(message = ""):
	layout = [  [ui.Text(message)],
				[ui.Text("Enter Reagent Name"), ui.InputText()],
				[ui.Text("Enter Amount"), ui.InputText(), ui.InputCombo(units)],
	            [ui.Button('Save Reagent'), ui.Button('Close'), ui.Button('View List')]]

	window = ui.Window('Reagent', layout)

	windowManager(window)

#Window to view reagents
#TODO make reagents selectable and add make new window based on selected reagent.
#TODO multiple reagents selectable at once. Seperate windows? Tables?
def drawReagentSelector(message = ""):
	listText = ""
	for each in Reagent.reagentList:
		listText = listText + each.toText() + "\n"

	layout = [[ui.Text(message)],
			 [ui.Text(listText)],
			 [ui.Button("View Reagent"), ui.Button("Add New Reagent")]]

	window = ui.Window('Reagent List', layout)

	windowManager(window)


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

	    #Amount entered is valid
	    #save reagent, timestamp reagent
	    #TODO save reagent as an instance of reagent
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