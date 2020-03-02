from Gui import set_gui
from calc import calc
from plot import plot

OF,Pressure_Chamber,Pressure_Vessel,Thrust,Isp,Fuel_Flow,Oxid_Flow,Time, Radius = calc(set_gui())
plot(OF,Pressure_Chamber,Pressure_Vessel,Thrust,Isp,Fuel_Flow,Oxid_Flow,Time, Radius)


