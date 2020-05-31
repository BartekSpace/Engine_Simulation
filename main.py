from Gui import set_gui
from calc import calc
from plot import *


cea, flag = set_gui()


OF, Pressure_Chamber, Pressure_Vessel, Thrust, Isp, Fuel_Flow, Oxid_Flow, Time, Radius = calc(cea)

plot(OF, Pressure_Chamber, Pressure_Vessel, Thrust, Isp, Fuel_Flow, Oxid_Flow, Time, Radius)

if flag == True:
   make_txt(Pressure_Chamber,Pressure_Vessel,Thrust,Time,Fuel_Flow)


