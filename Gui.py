import sys
if sys.version_info[0] >= 3:
    import PySimpleGUI as sg
else:
    import PySimpleGUI27 as sg

def set_gui ():
    bl = {'size': (25,1)}
    br = {'size': (30,1), 'justification':('right')}

    tab1_layout =  [
        [sg.T('This is inside tab 1')],
        [sg.Checkbox('Simulation time',default=True,key='check')],[ sg.Text("Time [s]"),sg.InputText( key='time_max',disabled=False,default_text='15')],
        [sg.Text('_'*120)],


        [sg.Text('Engine',size=(25,1),font=16,text_color='red'), sg.Text('Vessel', size=(40,1), font=16,justification='right',text_color='red')],
        [sg.Text('Combustion Pressure [bar]',**bl ), sg.InputText(key='Combustion_Pressure', default_text='30'),sg.Text('Pressure [bar]', **br), sg.InputText(key='Vessel_Pressure',default_text='60')],
        [sg.Text('Injector hole diameter [mm]', **bl), sg.InputText(key='hole_diam',default_text='1.5'),sg.Text('Volume [dm3]',**br), sg.InputText(key='Vessel_Volume', default_text='15')],
        [sg.Text('Holes number',**bl ), sg.InputText(key='holes_num',default_text='36'),sg.Text('Oxidizer Mass [kg]',**br),sg.InputText(key='oxid_mass')],
        [sg.Text('Throat Diameter [mm]',**bl), sg.InputText(key='throat_diam',default_text='32.8')],
        [sg.Text('Exit Nozzle Diameter [mm]', **bl), sg.InputText(key='nozzle_exit', default_text='70')],
        [sg.Text('K Loss', **bl),sg.InputText(key='K_loss',default_text='7.3')],
        [sg.Text('Real coeff',**bl),sg.InputText(key='chuj_coeff',default_text='0.8')],
        [sg.Text('_'*120)],
        [sg.Text('Fuel',size=(25,1),font=16,text_color='red')],
        [sg.Text('Length [mm]',**bl),sg.InputText(key='fuel_length',default_text='1000')],
        [sg.Text('Port Diameter [mm]',**bl),sg.InputText(key='port_diam',default_text='60')],
        [sg.Text('Density [kg/m3]',**bl),sg.InputText(key='fuel_dens',default_text='1130')],
        [sg.Text('a ballistic',**bl),sg.InputText(key='a_ballistic',default_text='0.00772597539149796')],
        [sg.Text('n ballistic',**bl),sg.InputText(key='n_ballistic',default_text='0.777265794840152')],
                    ]

    tab2_layout = [[sg.T('This is inside tab 2')],

                    [sg.Text('Oxidizer',size=(25,1),font=16,text_color='red'), sg.Text('Fuel', size=(40,1), font=16,justification='right',text_color='red')],
                   [sg.Text('Name', **bl), sg.InputText(key='oxid_name',default_text='Nitrous'), sg.Text('Name', **br),sg.InputText(key='fuel_name', default_text='Nylon')],
                   [sg.Text('Formula', **bl), sg.InputText(key='oxid_formula',default_text='N 2.0 O 1.0'), sg.Text('Formula', **br),sg.InputText(key='fuel_formula',default_text='C 6.0   H 11.0   O 1.0  N 1.0')],
                   [sg.Text('Temperature [K]', **bl), sg.InputText(key='oxid_temp',default_text='298.15'), sg.Text('Temperature [K]', **br),sg.InputText(key='fuel_temp',default_text='298.15')],
                   [sg.Text('Enthalpy [kJ/mol]', **bl), sg.InputText(key='oxid_enthalpy',default_text='75.24'), sg.Text('Enthalpy [kJ/mol]', **br),sg.InputText(key='fuel_enthalpy',default_text='67.69')],
                   ]



                   # [sg.In(key='in')]]

    layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout, tooltip='tip'), sg.Tab('Tab 2', tab2_layout)]], tooltip='TIP2')],
              [sg.Button('Subbmit',key='button'),sg.Button('Generate Txt',key='txt'),sg.Button('Quit',key='quit')] ]

    window = sg.Window('My window with tabs', default_element_size=(25,1)).Layout(layout).Finalize()

    #event,values = window.Read()
    #sg.Popup(event,values)





    while True:

       #
        # if window.Element('check'):
        #     window.Element('maslo').Update(disabled=False)
        #
        # if not window.Element('check'):
        #     window.Element('maslo').Update(disabled=True)
        # if event == 'check':
        #     if values[0] == True:
        #         window.Element('maslo').Update(disabled=False)
        #     if values[0] == False:
        #         window.Element('maslo').Update(disabled=True)

        # if values[0] == True:
        #       window.FindElement('maslo').Update(disabled=False)
        # if values[0] == False:
        #       window.FindElement('maslo').Update(disabled=True)
        #event, values = window.Read()
        event, values = window.read()
        flag = False
       # print (values)

        if event is None:  # always,  always give a way out!
             quit()
             break
        if event is 'quit':
            quit()

        if event is 'button':
            return values, flag
            #print(event, values)
            quit()
            #print ('dupa')
        if event is 'txt':
            flag = True
            return values, flag
            quit()


    # while True:
    #     event, values = window.read()
    #     print(event,values)
    #     if event is None:           # always,  always give a way out!
    #         break

