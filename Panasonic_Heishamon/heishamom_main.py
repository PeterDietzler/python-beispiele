Keine ausgewählt 

Direkt zum Inhalt
Gmail mit Screenreadern verwenden
in:sent 
Konversationen
47,84 GB von 100 GB belegt
Abo kündigen
Nutzungsbedingungen · Datenschutz · Programmrichtlinien
Letzte Kontoaktivität vor 1 Stunde
Details
import time
from shelly import shelly
import json
import requests
import os
import math

from datetime import datetime
global shelly1_ip
global shelly2_ip


shelly1_ip = "192.168.188.36"
shelly2_ip  ="192.168.188.177"

shelly_hk_ip  ="192.168.188.34"



def read_heishamon(IP):
    url = f"http://{IP}/"
    
    try:
        json_str = requests.get(url + 'json', timeout=( 3, 15) )
        data = json_str.json() 
        
        if json_str.status_code == 200:
            #data = json.loads(json_str.text).json()
            #print(data)
            return data, 0
        else:
            print("Not Working")
            return -1

    except requests.exceptions.InvalidURL or requests.exceptions.ConnectionError as err:
        print(err)
    except requests.exceptions.Timeout:
        print("The request timed out")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e )
    return 0, -1
 
 
 
 
def set_heishamon(IP, Name, Value): 
    url = "http://" + IP + "/command?" + Name + "=" + str(Value)
    #print("url = ", url)
    res = requests.get(url)
    if res.status_code == 200:
        print("url = ", url)
        print("answer = ", res.text)
        #data = json.loads(res.text)
        #print(data)
    else:
        print("Not Working")



    


def check_Heatpump( IP1, IP2):
    
    print("check_Heatpump(" + IP1 + ", " + IP2 )
    STATE_START_DEFROST =0
    STATE_START_PUMP_FLOW =0
    Defrost_State_IP1 =0
    Pump_Flow_IP1 =0
    
    data, res = read_heishamon(IP1)
    if res==0:
        Defrost_State_IP1 = data["heatpump"][26]["Value"]


    if Defrost_State_IP1 == 1:
        print( IP1 +" Enteisung Startet ")
        print( IP2 +" Ausschalten")
        set_heishamon( IP2, "SetHeatpump", 0)
        STATE_START_DEFROST=1

        while (STATE_START_DEFROST) :
            time.sleep(30)
            print("START_DEFROST:time.sleep(30)")
            data, res = read_heishamon(IP1)
            if res==0:
                Pump_Flow_IP1 = data["heatpump"][2]["Value"]
            
            if( Pump_Flow_IP1 >=25):
                STATE_START_PUMP_FLOW = 1
                STATE_START_DEFROST =0
                print( IP1 +" Pumpe startet")
                
            
        while(STATE_START_PUMP_FLOW):
            # Warten bis Volumenstrom kleine 20 l/min
            time.sleep(30)
            print("START_PUMP_FLOW: time.sleep(30)")
            data, res = read_heishamon(IP1)
            if res==0:
                Pump_Flow_IP1 = data["heatpump"][2]["Value"]
            if( Pump_Flow_IP1 < 20):
                STATE_START_PUMP_FLOW = 0
                print( IP1 +" Pumpe endet")
    
        print( IP2 +" Einschalten")
        set_heishamon(IP2, "SetHeatpump", 1)
        
        data = read_heishamon(IP1)
        if res==0:          
            Defrost_State_IP1 = data["heatpump"][26]["Value"]
        
        if Defrost_State_IP1 == 0:
            STATE_START_DEFROST = 0
            print( IP1 +" Enteisung Endet ")
    #print("check_Heatpump()")
                
    # http://192.168.188.25/command?SetZ1HeatRequestTemperature=1
    
    





def check_Main_Target_Temp(Restart, IP1, IP2):
    #print ("check_Main_Target_Temp()")
    data1=0
    data2=0
    Heat_Power_Production =0
    Heat_Power_Production1 =0
    Heat_Power_Production2 =0
    Main_Target_Temp1 = 0
    Main_Target_Temp2 = 0
    Main_Delta_Temp1 = 0
    Main_Delta_Temp2 = 0
    
    shelly1= shelly(shelly1_ip)
    shelly2= shelly(shelly2_ip)
    shelly_hk = shelly( shelly_hk_ip)
    
    
    
    
    data1, res1 = read_heishamon(IP1)
    if res1==0:
        Heatpump_State1         = data1["heatpump"][0]["Value"]
        Pump_Flow1              = data1["heatpump"][1]["Value"]
        Main_Inlet_Temp1        = data1["heatpump"][5]["Value"]
        Main_Outlet_Temp1       = data1["heatpump"][6]["Value"]
        Main_Target_Temp1       = data1["heatpump"][7]["Value"]
        Compressor_Freq1        = data1["heatpump"][8]["Value"] 
        Operations_Hours1       = data1["heatpump"][11]["Value"]
        Operations_Counter1     = data1["heatpump"][12]["Value"]
        Outside_Temp1           = data1["heatpump"][14]["Value"]
        Heat_Power_Production1  = data1["heatpump"][15]["Value"]
        Heat_Power_Consumption1 = data1["heatpump"][16]["Value"]
        Outside_Pipe_Temp1      = data1["heatpump"][21]["Value"]
        Defrosting_State1       = data1["heatpump"][26]["Value"]
        Z1_Heat_Request_Temp1   = data1["heatpump"][27]["Value"]
        Error1                  = data1["heatpump"][44]["Value"]
        Main_Hex_Outlet_Temp1   = data1["heatpump"][49]["Value"]
        Inside_Pipe_Temp1       = data1["heatpump"][51]["Value"]

        Fan1_Motor_Speed1       = data1["heatpump"][62]["Value"]
        High_Pressure1          = data1["heatpump"][64]["Value"]
        Pump_Speed1             = data1["heatpump"][65]["Value"]
        Heating_Off_Outdoor_Temp1 = data1["heatpump"][77]["Value"]
  
  
    data2, res2 = read_heishamon(IP2)
    if res2==0:
        Heatpump_State2         = data2["heatpump"][0]["Value"]
        Pump_Flow2              = data2["heatpump"][1]["Value"]
        Main_Inlet_Temp2        = data2["heatpump"][5]["Value"]
        Main_Outlet_Temp2       = data2["heatpump"][6]["Value"]
        Main_Target_Temp2       = data2["heatpump"][7]["Value"]
        Compressor_Freq2        = data2["heatpump"][8]["Value"] 
        Operations_Hours2       = data2["heatpump"][11]["Value"]
        Operations_Counter2     = data2["heatpump"][12]["Value"]
        Outside_Temp2           = data2["heatpump"][14]["Value"]
        Heat_Power_Production2  = data2["heatpump"][15]["Value"]
        Heat_Power_Consumption2 = data2["heatpump"][16]["Value"]
        Outside_Pipe_Temp2      = data2["heatpump"][21]["Value"]
        Defrosting_State2       = data2["heatpump"][26]["Value"]
        Z1_Heat_Request_Temp2   = data2["heatpump"][27]["Value"] 
        Error2                  = data2["heatpump"][44]["Value"]

        Main_Hex_Outlet_Temp2   = data2["heatpump"][49]["Value"]
        Inside_Pipe_Temp2       = data2["heatpump"][51]["Value"]

        Fan1_Motor_Speed2       = data2["heatpump"][62]["Value"]
        High_Pressure2          = data2["heatpump"][64]["Value"]
        Pump_Speed2             = data2["heatpump"][65]["Value"]
        Heating_Off_Outdoor_Temp2 = data2["heatpump"][77]["Value"]
        
    if res1==0 and res2==0:

        print("\n" + str(datetime.now()))
        print_str("Heischamon", "188.173", "188.25", "IP", "" )
        print_str("Outside_Temp",         Outside_Temp1, Outside_Temp2, "°C", "" )
        print_str("Z1_Heat_Request_Temp", Z1_Heat_Request_Temp1, Z1_Heat_Request_Temp2, "°C", "" )
        
        print_str("Main_Target_Temp",     Main_Target_Temp1, Main_Target_Temp2, "°C", "" )
        hk_vorlauf = shelly_hk.get_temperature(0)
        hk_rücklauf = shelly_hk.get_temperature(1)
        
        print_str("Main_Outlet_Temp",     Main_Outlet_Temp1, Main_Outlet_Temp2, "°C", "HK_vl = {:3.1f}".format(hk_vorlauf) )
        print_str("Main_Inlet_Temp",      Main_Inlet_Temp1, Main_Inlet_Temp2, "°C", "Hk_rl = {:3.1f}".format(hk_rücklauf) )

        Main_Delta_Temp1 = float(Main_Outlet_Temp1) - float(Main_Inlet_Temp1)
        Main_Delta_Temp2 = float(Main_Outlet_Temp2) - float(Main_Inlet_Temp2)
        print_str("Main_Delta_Temp", "{:3.1f}".format(Main_Delta_Temp1), "{:3.1f}".format(Main_Delta_Temp2), "°C", "Outlet-Inlet" )

        Target_Delta_Temp1 = float(Main_Target_Temp1) - float(Main_Inlet_Temp1)
        Target_Delta_Temp2 = float(Main_Target_Temp2) - float(Main_Inlet_Temp2)
        print_str("Target_Delta_Temp", "{:3.1f}".format(Target_Delta_Temp1), "{:3.1f}".format(Target_Delta_Temp2), "°C", "Target-Inlet" )

        print("")
        print_str("Heatpump_State",      Heatpump_State1, Heatpump_State2, "State", "1=on, 0=off" )
        print_str("Defrosting_State",      Defrosting_State1, Defrosting_State2, "State", "1=on, 0=off" )
        print_str("Error",      Error1, Error2, "", "" )

        Error1_Reset_done = 0
        Error2_Reset_done = 0
        
        if Restart ==1:
            if str(Error1) == "H62":
                Error1_Reset_done=1
                # Starte Shelly neu
                print("shelly1 Aussschalten")
                shelly1.set_relay(0)
                print("Warte 10 Sekunden")
                time.sleep(10)
                print("shelly1 Einschalten")
                shelly1.set_relay(1)
                print("Warte 40 Sekunden")
                time.sleep(40)
                
            if str(Error2) == "H62":
                Error2_Reset_done=1
                # Starte Shelly neu
                print("shelly2 Aussschalten")
                shelly2.set_relay(0)
                print("Warte 10 Sekunden")
                time.sleep(10)
                print("shelly2 Einschalten")
                shelly2.set_relay(1)
                print("Warte 40 Sekunden")
                time.sleep(40)


            if str(Error1) == "No error" and str(Error1) == "No error":
                if str(Heatpump_State1) == "0" and Error1_Reset_done ==1:
                    Error2_Reset_done = 0
                    set_heishamon(IP1, "SetHeatpump", 1)
                    print("Warte 40 Sekunden")
                    time.sleep(40)

                if str(Heatpump_State2) == "0" and Error2_Reset_done ==1:
                    Error2_Reset_done = 0
                    set_heishamon(IP2, "SetHeatpump", 1)
                    print("Warte 40 Sekunden")
                    time.sleep(40)
                
        
        
        print_str("Heating_Off_Out_Temp",      Heating_Off_Outdoor_Temp1, Heating_Off_Outdoor_Temp2, "°C", "" )

        print_str("Compressor_Freq",           Compressor_Freq1, Compressor_Freq2, "Hz", "" )
        print_str("Outside_Pipe_Temp",         Outside_Pipe_Temp1, Outside_Pipe_Temp2, "°C", "" )
        #print_str("Main_Hex_Outlet_Temp",      Main_Hex_Outlet_Temp1, Main_Hex_Outlet_Temp2, "°C", "" )
        #print_str("Inside_Pipe_Temp",          Inside_Pipe_Temp1, Inside_Pipe_Temp2, "°C", "" )

        print_str("High_Pressure",             High_Pressure1, High_Pressure2, "~ Bar", "Kgf/cm2 " )
        print_str("Pump_Flow",                 Pump_Flow1, Pump_Flow2, "l/min", "" )
        #print_str("Pump_Speed",                Pump_Speed1, Pump_Speed2, "r/min", "" )
        #print_str("Fan1_Motor_Speed",          Fan1_Motor_Speed1, Fan1_Motor_Speed2, "r/min", "" )
     
        Real_Power_Production1 = int(1.16* float(Pump_Flow1)*60.0* Main_Delta_Temp1)
     
        Real_Power_Production2 = int(1.16* float(Pump_Flow2)*60.0* Main_Delta_Temp2)
        Real_Power_Production = Real_Power_Production1 +Real_Power_Production2
     
        print_str("Real_Power_Production", str(Real_Power_Production1), str(Real_Power_Production2), "Watt", str(Real_Power_Production) )

      
        Heat_Power_Consumption1 = shelly1.get_power(0)
        Heat_Power_Consumption2 = shelly2.get_power(0)
        Heat_Power_Consumption =int(Heat_Power_Consumption1) + int(Heat_Power_Consumption2)     
     
        print_str("Real_Power_Consumption", "{:5.0f}".format(Heat_Power_Consumption1), "{:5.0f}".format(Heat_Power_Consumption2), "Watt", str(Heat_Power_Consumption) )

 
        if math.fabs(Heat_Power_Consumption1) >= 0.0001: 
            COP1 = float(Real_Power_Production1 / Heat_Power_Consumption1)
        else:
            COP1 = 0.0

        if math.fabs(Heat_Power_Consumption2) >= 0.00001: 
            COP2 = float(Real_Power_Production2 / Heat_Power_Consumption2)
        else:
            COP2 = 0.0
            
        COP = Real_Power_Production / (Heat_Power_Consumption + 0.0000001)
        
        print_str("COP", "{:3.1f}".format(COP1)  , "{:3.1f}".format(COP2), "Out/In", "{:3.1f}".format(COP) )



        print("Temp/COP@35°C (7°C/5.08) (2°C/3.57) (-7°C/2.78)")
        print("Temp/COP@55°C (7°C/3.10) (2°C/2.27) (-7°C/1.85)")
        #print_str("Operations_Hours", Operations_Hours1, Operations_Hours2, "h", 0 )
        #print_str("Operations_Counter", Operations_Counter1, Operations_Counter2, "count", 0 )

    else:
        print("keine gültigen Daten :-]") 





'''
    delta = int(Main_Target_Temp1) - int(Main_Target_Temp2)
    print("Main_Target_Temp = " , Main_Target_Temp1)
    print("Main_Target_Temp2 = " , Main_Target_Temp2)

    if( delta != 0):
        set_heishamon(IP2, "SetZ1HeatRequestTemperature", delta)
'''





#def print_int(name, wp1, wp2, unit, wp12 ):
#        print("%-20.20s = %6.0d | %6.0d | %6.6s | %6.1d |" % ( name, wp1, wp2, unit, wp12))

#def print_float(name, wp1, wp2, unit, wp12 ):
#        print("%-20.20s = %6.1f | %6.1f | %6.6s | %6.1f |" % ( name, wp1, wp2, unit, wp12))

def print_str(name, wp1, wp2, unit, wp12 ):
        print("%-25s = %8s | %8s | %6s | %15s |" % ( name, wp1, wp2, unit, wp12))



def main():

    IP1 ='192.168.188.173'
    IP2 ='192.168.188.25'
    
    
    #set_heishamon(IP2, "SetHeatpump", 1) 
    loop=0
    while True:
        loop = loop+1
        # Current date time in local system

        #check_Heatpump( IP1, IP2)
        #check_Heatpump( IP2, IP1)
        restart_wp = 1
        check_Main_Target_Temp( restart_wp, IP1, IP2)
        
        
        
        
        for i in range(0, 10):
            time.sleep(1)
            print('.', end="")

if __name__ == "__main__":
    main()
    
# http://192.168.188.25/command?SetZ1HeatRequestTemperature=2    
# http://192.168.188.173/command?SetZ1HeatRequestTemperature=2
 # http://192.168.188.25/command?SetHeatpump=1
# http://192.168.188.173/command?SetHeatpump=1

    
    
heishamom_main.py
heishamom_main.py wird angezeigt.