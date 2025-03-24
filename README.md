
# Modern Game AI Algorithms Assignment 1: Procedural Conent Generation 
The program is composed of three python files: 
- _minecraft.py_: this is the main file from which you should run the program. It contains the methods to clear the building region, build the structure of the house and add the external decorations. 
- _find_location.py_: this file contains the methods written in order to find the best house location and it also contains the function that plots the heatmap. If you want to visualize the heatmap uncomment the method createHeatMap()
- _houseInteriors.py_: this file contains the methods used to decorate the interiors of the house
The folder A1 MGAIA also contains the folder _gdpc_, since I've used some of its methods.
- folder *gdpc* contains the GDPC python package.

### How to run the program
To run the program from the command line it is advised to create a virtual environemnt. I've created a pipenv environement with the command _pipenv shell_
Then you will need to install: 
- "termcolor" with the command "pip install termcolor"
- "gdpc" again with _pip install gdpc_
Finally you can run the code by using the relative path of the minecraft.py file:

_python3 myAssignment/minecraft.py_