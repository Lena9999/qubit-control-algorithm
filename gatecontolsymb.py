import sympy as sym
from IPython.display import display


class GateContorlSymb:
    def __init__(self, objective_function = "0.5*(x(t)-x_target)**2+0.5*(y(t)- y_target)**2+0.5*(z(t) - z_target)**2", \
                 x_crd_eq = "x(t)",  y_crd_eq = "y(t)", z_crd_eq = "z(t)",  Gate = "H"):
        self.x, self.y, self.z, self.u, self.G, self.x_target_t, self.y_target_t, self.z_target_t,= sym.symbols('x,y,z,u,G, x_target_t, y_target_t,z_target_t', cls=sym.Function)
        self.w_x, self.w_y, self.w_z, self.t, self.x_target, self.y_target, self.z_target, self.GAMMA = sym.symbols('w_x, w_y, w_z, t, x_target, y_target, z_target, Gamma')
        self.initial_x, self.initial_y, self.initial_z = sym.symbols('self.initial_x, self.initial_y, self.initial_z')
        self.target_values_list = self.GateTargetValues(gate = Gate)#Target values are determined by the type of gate
        self.target_x = self.target_values_list["x"]
        self.target_y = self.target_values_list["y"]
        self.target_z= self.target_values_list["z"]
        self.objective_function = sym.Eq(self.G(self.t), sym.sympify(objective_function))


        #x_coord_equation is the equation for modeling x coordinate behavior in system_modeling_equation
        self.x_coord_equation = sym.Eq(self.x(self.t).diff(self.t), sym.sympify(x_crd_eq))
        self.y_coord_equation = sym.Eq(self.y(self.t).diff(self.t), sym.sympify(y_crd_eq))
        self.z_coord_equation = sym.Eq(self.z(self.t).diff(self.t), sym.sympify(z_crd_eq))
        self.system_modeling_equation = [self.x_coord_equation, self.y_coord_equation, self.z_coord_equation] #System of equations modeling a quantum system

    def GateTargetValues(self,gate = "H")->dict:#This is a method which return target value for choosing gate 
        target_value_list = {}
        if gate == "H":
            target_value_list["x"] = self.initial_x
            target_value_list["y"] = -self.initial_y
            target_value_list["z"] = -self.initial_z
        
        if gate == "S":
            target_value_list["x"] = self.initial_x
            target_value_list["y"] = -self.initial_z
            target_value_list["z"] = self.initial_y
        
        if gate == "Z":
            target_value_list["x"] = self.initial_x
            target_value_list["y"] = -self.initial_y
            target_value_list["z"] = -self.initial_z

        return target_value_list
    
    def dGdt(self): #This function returns the time derivative of the objective_function.
       dGdt = sym.Eq(sym.Derivative(self.objective_function.args[0], self.t), \
                     sym.Derivative(self.objective_function.args[1], self.t).doit())#We take the derivative with respect to time
       #We use the equations of the system to substitute the derivatives of coordinates with respect to time
       dGdt = sym.solve([dGdt] + self.system_modeling_equation, \
                     (self.G(self.t).diff(self.t), self.x(self.t).diff(self.t), self.y(self.t).diff(self.t) , self.z(self.t).diff(self.t)))
       dGdt = sym.Eq(list(dGdt.keys())[0], list(dGdt.values())[0])
       return dGdt
    
    def control_algorithm(self): #This function returns control algorithm u:
       dGdt = self.dGdt()
       control_algorithm = sym.simplify(sym.Eq(self.u(self.t), -self.GAMMA*sym.Derivative(dGdt.args[1], self.u(self.t)).doit()))
       return control_algorithm
    
    @staticmethod 
    def display_latex_forms(equation_list:list): # This function displays the system of equations in latex form
        print("The system of equations:")
        try:
            for i in equation_list:
                display(i)
        except TypeError:
            print("Equations must be submitted as a list. For examle, equation_list = [euation_1, equation_2...]")

if __name__ == "__main__":
    symb = GateContorlSymb(Gate="Z")
    l =symb.control_algorithm()
