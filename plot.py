
from main import main
import numpy as np
import matplotlib.pyplot as plt
import math
import Cea
import Side_Functions
import nitrous
import Gui
# if 0:
#      import UserList
#      import UserString
#      import UserDict
#      import itertools
#      import collections
#      import future.backports.misc
#      import commands
#      import base64
#      import __buildin__
#      import math
#      import reprlib
#      import functools
#      import re
#      import subprocess

OF,Pressure_Chamber,Pressure_Vessel,Thrust,Isp,Fuel_Flow,Oxid_Flow,Time, Radius = main()

def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier

def step(x):
    if x < 10:
        return 1
    if x >=10:
        return x//10

def filter(x):
    i =1
    while i < len(x):
        if x[i-1] < x[i]:
            x[i-1] = x[i]
        i=i+1

filter(Pressure_Chamber)
filter(Thrust)
filter(Oxid_Flow)
filter(OF)
filter(Isp)
filter(Fuel_Flow)


br = {'settings': np.arange(0,round_up(Time[-1]),step(Time[-1]))}

# for i in range(0,1000):
#     if Pressure_Chamber[i] < Pressure_Chamber[i+1]:
#         del Pressure_Chamber[i]

length = [len(OF), len(Pressure_Chamber), len(Pressure_Vessel), len(Thrust), len(Isp), len(Fuel_Flow),
          len(Oxid_Flow), len(Time), len(Radius)]


def min(tab):
    m=tab[0]
    for i in tab:
        if i<m:
            m=i
    return m

sample = min(length)
# fig = plt.figure()
# ax = fig.gca()
#plt1 = fig.add_subplot(221)
#plt1.grid()
# #Time, OF = create_plot('linear')
 #Time.append(15.1)
#plt1.plot(Time, Pressure_Vessel, color ='r')
# fig.plot(Time, Pressure_Vessel)
# ax.set_xticks(np.arange(0, 15, 1))
# plt1.set_title('$y_1 = x$')
# fig.subplots_adjust(hspace=.5,wspace=0.5)
#
# plt.show()
# for i in Pressure_Chamber:
#     print(i)

#x = np.arange(0, 1, 0.05)
#y = np.power(x, 2)
#Time.append(15.1)
#Pressure_Chamber.append(0)
#Time.pop()

# for i in Pressure_Chamber:
#     print(i)
#
#
#
# print(len(Time))
# print(len(Pressure_Chamber))

#Pressure_Chamber.append(0)
#Pressure_Chamber.append(0)
#x = Time[0:sample]
#y = Thrust[0:sample]

fig = plt.figure(figsize=(15,15))
#ax = fig.gca()
#ax.set_xticks(np.arange(0, 15, 1))
#ax.set_yticks(np.arange(0, 30, 2))

#plt.plot(x, y, linewidth=2.0)
#plt.scatter(x, y)
#plt.grid()


plt1 = fig.add_subplot(221)
plt1.plot(Time[0:sample], Pressure_Vessel[0:sample], color ='r')
plt1.grid()

plt1.set_yticks(np.arange(0,round_up(Pressure_Vessel[0])+Pressure_Vessel[0]//6,Pressure_Vessel[0]//6))
plt1.set_xticks(br['settings'])

plt1.set_axis_on()
plt1.set_title('Pressure Vessel')
plt1.set_xlabel('Time [s]')
plt1.set_ylabel('Pressure [bar]')


plt2 = fig.add_subplot(222)
plt2.plot(Time[0:sample],Pressure_Chamber[0:sample])
#plt2.scatter(Time[0:sample],Pressure_Chamber[0:sample])
plt2.grid()

plt2.set_yticks(np.arange(0,round_up(Pressure_Chamber[0])+Pressure_Chamber[0]//6,Pressure_Chamber[0]//6))
plt2.set_xticks(br['settings'])
plt2.set_axis_on()
plt2.set_title('Pressure Chamber')
plt2.set_xlabel('Time [s]')
plt2.set_ylabel('Pressure [bar]')

plt3 = fig.add_subplot(223)
plt3.plot(Time[0:sample],Thrust[0:sample])
plt3.grid()
plt3.set_yticks(np.arange(0,round_up(Thrust[0])+Thrust[0]//6,500))
plt3.set_xticks(br['settings'])
plt3.set_axis_on()
plt3.set_xlabel('Time [s]')
plt3.set_ylabel('Thrust [N]')
plt3.set_title('Thrust')

plt4 = fig.add_subplot(224)
plt4.plot(Time[0:sample],Isp[0:sample])
plt4.grid()
plt4.set_yticks(np.arange(0,round_up(Isp[0]),10))
plt4.set_xticks(br['settings'])
plt4.set_axis_on()
plt4.set_xlabel('Time [s]')
plt4.set_ylabel('Isp [s]')
plt4.set_title('Isp')

plt.savefig('line_plot.pdf')

fig1 = plt.figure(figsize=(15,15))
plt5 = fig1.add_subplot(221)
plt5.plot(Time[0:sample],OF[0:sample])
plt5.grid()
plt5.set_yticks(np.arange(0,math.ceil(OF[0])+1,1))
plt5.set_xticks(br['settings'])
plt5.set_axis_on()
plt5.set_xlabel('Time [s]')
plt5.set_ylabel('OF')
plt5.set_title('OF')

plt6 = fig1.add_subplot(222)
plt6.plot(Time[0:sample],Radius[0:sample])
#plt6.scatter(Time[0:sample],Radius[0:sample])
plt6.grid()
plt6.set_yticks(np.arange(math.floor(Radius[0]),math.ceil(Radius[-1]),1))
plt6.set_xticks(br['settings'])
plt6.set_axis_on()
plt6.set_xlabel('Time [s]')
plt6.set_ylabel('Radius [mm]')
plt6.set_title('Radius')

plt7 = fig1.add_subplot(223)
plt7.plot(Time[0:sample],Oxid_Flow[0:sample])

plt7.grid()
plt7.set_yticks(np.arange(0,math.ceil(Oxid_Flow[0]),0.1))
plt7.set_xticks(br['settings'])
plt7.set_axis_on()
plt7.set_xlabel('Time [s]')
plt7.set_ylabel('Oxidizer Flow [kg/s]')
plt7.set_title('Oxidizer Flow')

plt8 = fig1.add_subplot(224)
plt8.plot(Time[0:sample],Fuel_Flow[0:sample])

plt8.grid()
plt8.set_yticks(np.arange(0,math.ceil(Fuel_Flow[0]),0.1))
plt8.set_xticks(br['settings'])
plt8.set_axis_on()
plt8.set_xlabel('Time [s]')
plt8.set_ylabel('Fuel Flow [kg/s]')
plt8.set_title('Fuel Flow')




plt.savefig('plot2.pdf')



plt.show()


