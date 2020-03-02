from nitrous import *
from Gui import *
from Side_Functions import *
from Cea import *
import math

constants = {
    'delta_t': 0.01,
    'lag_time': 0.2,
    'liquid_end': 2.0,
    'Z_crit': 0.27377,
    'P_crit': 72.45000,
    'gamma': 1.3,
    'specific_gas_constant': 188.911611,
    'Z_guess_accuracy': 0.0001,
    'nitrous_molar_mass': 0.04401,
    'chamber_pressure_gas_only': 8


}
def string_modify(string):
    string = string.upper()
    tmp = ''
    for i in string:
        if i.isalpha():

            tmp = tmp + ' ' + i
            flag = 1

        else:
            if flag == 1:
                tmp = tmp + ' '
            tmp = tmp + i
            flag =0

    return tmp


def calc(cea):
    #cea = set_gui()
    P_Vessel = [float(cea['Vessel_Pressure'])]
    P_Chamber = [float(cea['Combustion_Pressure'])]
    vessel_volume = float(cea['Vessel_Volume'])
    oxid_mass = [float(cea['oxid_mass'])]
    K_loss = float(cea['K_loss'])
    inj_holes = float(cea['holes_num'])
    inj_diameter = float(cea['hole_diam'])
    radius = [float(cea['port_diam'])/2]
    a_ballistic = float(cea['a_ballistic'])
    n_ballistic = float(cea['n_ballistic'])
    length = float(cea['fuel_length'])
    fuel_dens = float(cea['fuel_dens'])
    throat_diam = float(cea['throat_diam'])
    exit_nozzle_diam = float(cea['nozzle_exit'])
    chuj_coeff = float(cea['chuj_coeff'])
    oxid_name = cea['oxid_name']
    fuel_name = cea['fuel_name']

    oxid_formula = cea['oxid_formula']



    fuel_formula = cea['fuel_formula']

    fuel_formula = string_modify(fuel_formula)
    oxid_formula = string_modify(oxid_formula)

    oxid_temp = cea['oxid_temp']
    fuel_temp = cea['fuel_temp']
    oxid_enthalpy = cea['oxid_enthalpy']
    fuel_enthalpy = cea['fuel_enthalpy']
    time = float(cea['time_max'])

    T = nox_on_press(P_Vessel[-1])
    l_dens = nox_Lrho(T)
    v_dens = nox_Vrho(T)

    liquid_mass = liquid_phase(vessel_volume/1000,P_Vessel[-1],oxid_mass[-1])
    vap_mass = oxid_mass[-1]-liquid_mass
    add_oxid(oxid_name,oxid_formula,oxid_temp,oxid_enthalpy)
    add_fuel(fuel_name,fuel_formula,fuel_temp,fuel_enthalpy)

    t=[0]
    reg=[0]
    Gox=[]
    reg=[]
    OF=[]
    Isp=[]
    Thrust=[]
    mf=[]
    liquid_flow=[]
    count=0
    c_star=[]
    i=0


    while t[-1]< time:


        liquid_flow.append(pow( 2 * l_dens * ( P_Vessel[-1] - P_Chamber[-1] )*100000 / D_loss( K_loss, inj_holes, inj_diameter ), 0.5 ))

        m_out = liquid_flow[-1] * constants['delta_t']
        m_evap = m_out / l_dens / (1 / v_dens - 1 / l_dens)
        liquid_mass = liquid_mass - m_out - m_evap
        vap_mass += m_evap
        MF,GOX,RADIUS,REG = fuel_flow(liquid_flow[-1],radius[-1],a_ballistic,n_ballistic,length,fuel_dens,constants['delta_t'])
        radius.append(RADIUS)
        mf.append(MF)
        Gox.append(GOX)
        reg.append(REG)
        OF.append(liquid_flow[-1]/mf[-1])
        Isp.append(get_Isp(oxid_name,fuel_name,P_Chamber[-1],OF[-1],pow(exit_nozzle_diam/throat_diam,2)))
        Thrust.append(Isp[-1] * (liquid_flow[-1]+mf[-1])*9.81*chuj_coeff)
        if liquid_mass <  2 * constants['liquid_end']  and liquid_mass > constants['liquid_end'] * 1.9 :
            tmp_time = t[-1]
            tmp_vessel = P_Vessel[-1]
            tmp_chamber = P_Chamber[-1]
            tmp_liquid_flow = liquid_flow[-1]
            tmp_fuel_flow = mf[-1]
            tmp_vap_dens = v_dens
            tmp_vap_mass = vap_mass
            tmp_l_dens = l_dens
            tmp_Isp = Isp[-1]
            tmp_thrust = Thrust[-1]
            tmp_OF = OF[-1]
            tmp_radius = radius[-1]
            tmp_mf = mf[-1]
            tmp_reg = reg[-1]
            #break
        if (liquid_mass < constants['liquid_end']):

            radius.pop() #radius jest rozjechany z czasem o 1 wartosc wiec bez tego wykres sie wydupcy
                         # (przydzieli ekstrapolowany czas starej wartosci)

            extrapolate_time = liquid_mass / liquid_flow[-1]
            tmp2_t = t[-1]
            t.append(extrapolate_time +t[-1])
            P_Vessel.append(LinearExtrapolate(t[-1], tmp_time, tmp_vessel, tmp2_t, P_Vessel[-1]))
            liquid_flow.append(LinearExtrapolate(t[-1], tmp_time, tmp_liquid_flow, tmp2_t, liquid_flow[-1]))
            vap_mass = LinearExtrapolate(t[-1], tmp_time, tmp_vap_mass, tmp2_t, vap_mass)

            v_dens = LinearExtrapolate(t[-1], tmp_time, tmp_vap_dens, tmp2_t, v_dens)
            P_Chamber.append(LinearExtrapolate(t[-1], tmp_time, tmp_chamber, tmp2_t, P_Chamber[-1]))

            l_dens = LinearExtrapolate(t[-1], tmp_time, tmp_l_dens, tmp2_t, l_dens)
            Thrust.append(LinearExtrapolate(t[-1], tmp_time, tmp_thrust, tmp2_t, Thrust[-1]))
            radius.append(LinearExtrapolate(t[-1], tmp_time, tmp_radius, tmp2_t, radius[-1]))
            Isp.append(LinearExtrapolate(t[-1], tmp_time, tmp_Isp, tmp2_t, Isp[-1]))
            OF.append(LinearExtrapolate(t[-1], tmp_time, tmp_OF, tmp2_t, OF[-1]))
            mf.append(LinearExtrapolate(t[-1], tmp_time, tmp_mf, tmp2_t, mf[-1]))
            reg.append(LinearExtrapolate(t[-1], tmp_time, tmp_reg, tmp2_t, reg[-1]))
            #print(Thrust[-1], " ", t[-1])
            #P_Chamber.append(constants['chamber_pressure_gas_only'])
            counter = 0
            liquid_flow.append(pow(2 * l_dens * (P_Vessel[-1] - P_Chamber[-1]) * 100000 / D_loss(K_loss, inj_holes, inj_diameter), 0.5))

            m1 = vap_mass
            T1 = T
            P1 = P_Vessel[-1]
            P2 = P_Vessel[-1]
            vap_dens = v_dens
            Z1 = compressibility_factor(P1,constants['P_crit'],constants['Z_crit'])

            while  t[-1] < time:
                if P_Vessel[-1] <= 3.5:
                    return OF,P_Chamber, P_Vessel, Thrust, Isp, mf, liquid_flow, t, radius
                m2 = m1 - liquid_flow[-1]*constants['delta_t']
                Z2 = Z1
                Z_p = 1.0
                T2 = 0.0

                while math.fabs(Z2-Z_p) >= constants['Z_guess_accuracy']:
                    T2 = T1 * pow(Z2 * m2 / Z1 / m1, 1 / (constants['gamma'] - 1))
                    P2 = pow((T2 / T1), ((constants['gamma']) / (constants['gamma'] - 1))) * P1
                    Z_p = compressibility_factor(P2, constants['P_crit'], constants['Z_crit'])
                    if math.fabs(Z2-Z_p) <= 0.0001:
                        break
                    if Z2 < Z_p:
                        Z2 += constants['Z_guess_accuracy']/10
                    if Z2 > Z_p:
                        Z2 -= constants['Z_guess_accuracy']/10

                P_Vessel.append(P2)
                if m2 <=0:
                    return OF,P_Chamber, P_Vessel, Thrust, Isp, mf, liquid_flow, t, radius
                P1 = P2
                T1 = T2
                vap_dens = nox_Vrho(T1)
                Z1 = Z2
                MF, GOX, RADIUS, REG = fuel_flow(liquid_flow[-1],radius[-1],a_ballistic,n_ballistic,length,fuel_dens,constants['delta_t'])
                mf.append(MF)
                Gox.append(GOX)
                radius.append(RADIUS)
                reg.append(REG)


                OF.append(liquid_flow[-1]/mf[-1])
                if counter > 0:

                    At = pow(throat_diam / 1000, 2) * 3.14 / 4
                    P_Chamber.append(c_star[-1]*(mf[-1]+liquid_flow[-1])/At/100000)
                    #if counter == 1:
                        #P_Chamber.pop()

                elif counter == 0:
                    P_Chamber.append(P_Chamber[-1])

                Isp.append(get_Isp(oxid_name, fuel_name, P_Chamber[-1], OF[-1], pow(exit_nozzle_diam / throat_diam, 2)))
                Thrust.append(Isp[-1] * (liquid_flow[-1] + mf[-1]) * 9.81 * chuj_coeff)

                if P_Chamber[-1] <= 1:
                    P_Chamber[-1]= 1
                    c_star.append(P_Chamber[-1] * 100000 * pow(throat_diam / 1000, 2) * 3.14 / 4 / (liquid_flow[-1] + mf[-1]))
                    t.append(t[-1] + constants['delta_t'])
                    liquid_flow.append(pow(2 * vap_dens * (P_Vessel[-1] - P_Chamber[-1]) * 100000 / D_loss(K_loss, inj_holes,inj_diameter), 0.5))
                    return OF, P_Chamber, P_Vessel, Thrust, Isp, mf, liquid_flow, t, radius

                c_star.append(P_Chamber[-1] * 100000 * pow(throat_diam / 1000, 2) * 3.14 / 4 / (liquid_flow[-1] + mf[-1]))
                t.append(t[-1]+constants['delta_t'])
                counter = counter+1
                liquid_flow.append(pow(2 * vap_dens * (P_Vessel[-1] - P_Chamber[-1]) * 100000 / D_loss(K_loss, inj_holes, inj_diameter),0.5))






            return OF,P_Chamber, P_Vessel, Thrust, Isp, mf, liquid_flow, t, radius
        if count > 0:
            #P_Chamber.append((liquid_flow[-1] + mf[-1]) * c_star[-1] / pow(throat_diam/1000,2)*3.14/4)
            At = pow(throat_diam/1000,2)*3.14/4
            P_Chamber.append(c_star[-1]*(mf[-1]+liquid_flow[-1])/At/100000)
        elif count == 0:
            P_Chamber.append(P_Chamber[-1])

        if P_Chamber <= 1:
            P_Chamber[-1]= 1
            return OF, P_Chamber, P_Vessel, Thrust, Isp, mf, liquid_flow, t, radius
        #c_star.append(P_Chamber[-1] * 3.14/4*pow((throat_diam/1000),2) / (liquid_flow[-1] + mf[-1]))
        c_star.append(P_Chamber[-1]*100000*pow(throat_diam/1000,2)*3.14/4/(liquid_flow[-1] + mf[-1]))
        #c_star.append(get_c_star(oxid_name,fuel_name,P_Chamber[-1],OF[-1]))

        count=count+1
        T=Temperature_Iteration(T,liquid_mass,m_evap)
        P_Vessel.append(nox_vp(T))
       # P_Vessel=nox_vp(T)
        l_dens=nox_Lrho(T)
        v_dens=nox_Vrho(T)
        #t=t+constants['delta_t']
        t.append(t[-1]+constants['delta_t'])


    #P_Chamber.pop()
    return OF, P_Chamber, P_Vessel, Thrust, Isp, mf, liquid_flow, t, radius