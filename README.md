# qubit-control-algorithm
This project contains a class that models the behavior of a quantum qubit under the influence of a control field. The control field mimics the operation of basic quantum gates, such as Pauli gates.

This project contains two classes. The first one is gatecontolsymb.py, it is designed to make symbolic calculations and present them in a visual form. The second class is gatecontorlnum.py which intended to obtain a numerical simulation of the qubit model. In addition, the gatecontorlnum.py class will allow you to get a graphical visualization of numerical calculations.

The display_latex_forms function allows to display equation in latex forms for checking ones in juputer notebook.
GateTargetValus is a function which returns the list of target values. The values of targets determined by quantum Gate. 
The class attribute system_modeling_equation the main equation which model the behavior of a quantum system. The class attribute x_coord_equation, y_coord_equation, z_coord_equation are responsible for modeling each of the coordinates. The objective_function allows to set the type of objective function.
