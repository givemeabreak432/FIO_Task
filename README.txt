python version 3.7
required libraries:
PySimpleGUI
---
Classes:
Reagent:
  variables:
    reagentList: list of current instances of reagent
    reagentFile: directory for reagent list
  functions:
    __init__: constructor for reagent class. Reagents can also carry additional data stored in list.
    newReagent: static method that creates new instance of reagent class by calling constructor and calls saveReagent
    startup: static method. populates reagentList with reagents from reagentFile
    searchByName: Static method. Accepts a string (name) and does a simple brute force search for a reagent with matching name.
	***TODO handle duplicate names, make more efficient for large data sets. Sort reagents by name?
    saveReagent: Saves new reagent to text document. 
    appendReagent: appends additional data for already defined reagent. 
    toText: to string method, returns all pre-defined data. Does not return additional stored data
Windows:
  Input menu - default menu. This menu is for accepting new reagents, does not define their additional properties
  Reagent Selector - list of currently saved reagents. Can select a reagent to view properties
  Reagent Properties - Displays predefined and additional properties of reagent
  Reagent Update - Allows for input of additional properties for reagents.

windowManager function: This function is called by all draw functions. Responsible for event checking and calling draw functions