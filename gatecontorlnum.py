import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

class GateControlNum:
    def __init__(self, initial_condition: dict, gate: str, gamma = 40):
        self.initial_condition = initial_condition
        self.gamma = gamma
        self.target_values_list = self.GateTargetValues(Gate = gate, initial_condition = self.initial_condition)#Target values are determined by the type of gate
        self.target_x_values = self.target_values_list["x"]
        self.target_y_values = self.target_values_list["y"]
        self.target_z_values = self.target_values_list["z"]
  

    def GateTargetValues(self, initial_condition, Gate = "H")->dict:#This is a method which return target value for choosing gate 
        target_value_list = {}
        if Gate == "H":
            target_value_list["x"] = initial_condition["x"]
            target_value_list["y"] = -initial_condition["y"]
            target_value_list["z"] = -initial_condition["z"]
        
        if Gate == "S":
            target_value_list["x"] = initial_condition["x"]
            target_value_list["y"] = -initial_condition["z"]
            target_value_list["z"] = initial_condition["y"]
        
        if Gate == "Z":
            target_value_list["x"] = initial_condition["x"]
            target_value_list["y"] = -initial_condition["y"]
            target_value_list["z"] = -initial_condition["z"]
        return target_value_list
    
    @property#Work with initial condition
    def initial_condition(self):
        return self._initial_condition
    
    @initial_condition.setter
    def initial_condition(self, value):
        if abs(1 - sum([x**2 for x in value.values()])) > 0.02 :
            raise ValueError("The sum of initial condition should be equal 1 in order the point stay at Bloch sphere") 
        self._initial_condition = value
    
    def system_equation_main(self, x:list, t):
        u = -self.gamma*x[2]*(x[0]- x[1]*self.target_x_values)#self.gamma*(x[2]*self.target_x_values - x[0]*self.target_z_values)
        dxdt = x[0]
        dydt = x[1]
        dzdt = x[2]
        dfdt = [dxdt, dydt, dzdt]
        return dfdt
    
    def system_solution(self, tstart = 0, tstop = 520): #This function solves the differential equation
        t = np.arange(tstart,tstop)
        solution = odeint(lambda x,t: self.system_equation_main(x,t), list(self.initial_condition.values()), t)
        return solution
    
    def objective_function(self, solution): #This function returns objective function values
        objective_function =  0.5*(solution[:,0] - self.target_x_values)**2 \
            + 0.5*(solution[:,1] - self.target_y_values)**2 + 0.5*(solution[:,2] - self.target_z_values)**2
        return objective_function
    
    def control_algorithm(self, solution): #This function returns control_algorithm values
        control_algorithm = self.gamma*(solution[:,2])
        return control_algorithm
    
    def sum_fuction(self, solution): #This function returns sum of all coords values during the solution
        sum_fuction = solution[:,0]**2 + solution[:,1]**2+ solution[:,2]**2
        return sum_fuction
    
    def dGdt(self, solution): #dg/dt values
        u_function = self.control_algorithm(solution)
        dGdt = (solution[:,0] - self.target_x_values)
        return dGdt
    
    def plot_solution(self, solution): #dg/dt values
        tstart = 0
        tstop = len(solution[:,0])
        t = np.arange(tstart,tstop)
        N = len(solution[:,0])
        asymptote_x = np.linspace(0, tstop, N, endpoint=True)
        asymptote_y = np.zeros(N)

        plt.plot(asymptote_x, asymptote_y + self.target_x_values, color = "green", linestyle = '--', linewidth = 2, label='x*')
        plt.plot(asymptote_x, asymptote_y + self.target_y_values, color = "black", linestyle = '--', linewidth = 2, label='y*')
        plt.plot(asymptote_x, asymptote_y + self.target_z_values, color = "red", linestyle = '--', linewidth = 2, label='z*')
        # main chart
        plt.plot(t, solution[:,0], linewidth = 2, color = "green", label='x')
        plt.plot(t, solution[:,1], linewidth = 2, color = "black", label='y')
        plt.plot(t, solution[:,2], linewidth = 2, color = "red", label='z')
        plt.legend(fontsize="20")
        plt.axis([tstart, tstop, -1, 1])
        plt.xticks(np.arange(0, tstop, step = tstop/10, dtype=None).tolist(), fontsize = 10)
        plt.xlabel("t", fontsize = 30)
        plt.ylabel("x, y, z", fontsize = 30)
        #plt.grid(color='r', linestyle='-', linewidth=2)
        #plt.yticks(np.arange(-1, 1, step = 0.1, dtype=None).tolist(),fontsize = 10)
        plt.show()


if __name__ == "__main__":
    gate_h = GateControlNum(gate = "S", initial_condition = {"x": -0.7, "y": 0.5, "z": -0.5,})
    solution = gate_h.system_solution()
    print(len(solution))
    gate_h.plot_solution(solution) 