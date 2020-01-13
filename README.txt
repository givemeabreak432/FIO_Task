
python version 3.7
required libraries:
PySimpleGUI
---
Classes:
Reagent:
  variables:
    reagentList: list of current instances of reagent
    reagentFile: directory for reagent list
    additionalProperties: additional data stored in 2 dimensional list for each element.
    Quantity: amount of reagent used
    timestamp: date entered into system
  functions:
    __init__: constructor for reagent class. Reagents can also carry additional data stored in list.
    newReagent: static method that creates new instance of reagent class by calling constructor and calls saveReagent
    startup: static method. populates reagentList with reagents from reagentFile
    searchByName: Static method. Accepts a string (name) and does a simple brute force search for a reagent with matching name.
	***TODO handle duplicate names, make more efficient for large data sets. Sort reagents by name?
    saveReagent: Saves new reagent to text document. 
    appendReagent: appends additional data for already defined reagent. 
    toText: to string method, returns all pre-defined data. Does not return additional stored data
    addProperty: add a new additional property. Overloaded to allow a key and value, or a list of length 2.
Quantity:
  variables:
    amount: measuread value of quantity
    unit: quantity amount was measured in
Unit:
   variables:
    measurement: Type of unit (temp, volume, etc)
    m: ratio of unit vs base unit
    b: offset from base unit

draw:
  Input menu - default menu. This menu is for accepting new reagents, does not define their additional properties
  Reagent Selector - list of currently saved reagents. Can select a reagent to view properties
  Reagent Properties - Displays predefined and additional properties of reagent
  Reagent Update - Allows for input of additional properties for reagents.

windowManager: This function is called by all draw functions. Responsible for event checking and calling draw functions

TODO:
delete reagent or additional property
add units to additional property
reagent interactions list (new txt doc?) - 2 d array [[reg 1, reg 2], [result 1, result 2, ...]]
expand Unit class - create base units, expand custom units. 