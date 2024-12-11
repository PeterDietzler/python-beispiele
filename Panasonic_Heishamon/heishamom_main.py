import time

import json
import requests
import os

from datetime import datetime

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
    
    





def check_Main_Target_Temp(IP1, IP2):
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
    
    
    data1, res = read_heishamon(IP1)
    if res==0:
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
  
  
    data2, res = read_heishamon(IP2)
    if res==0:
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
        


    print("\n" + str(datetime.now()))

    print("Outside_Temp           = "+" ("+  str(Outside_Temp1) + ", " + str(Outside_Temp2) + ") [°C]" )
    print("Z1_Heat_Request_Temp   = "+" ("+  str(Z1_Heat_Request_Temp1) + ", " + str(Z1_Heat_Request_Temp2) + ") [°C]" )
    print("Main_Target_Temp       = "+" ("+  str(Main_Target_Temp1) + ", " + str(Main_Target_Temp2) + ") [°C]" )
    print("Main_Outlet_Temp       = "+" ("+  str(Main_Outlet_Temp1) + ", " + str(Main_Outlet_Temp2) + ") [°C]" )
    print("Main_Inlet_Temp        = "+" ("+  str(Main_Inlet_Temp1)  + ", " + str(Main_Inlet_Temp2)  + ") [°C]" )
    
    Main_Delta_Temp1 = float(Main_Outlet_Temp1) - float(Main_Inlet_Temp1)
    Main_Delta_Temp2 = float(Main_Outlet_Temp2) - float(Main_Inlet_Temp2)
    
    print("Main_Delta_Temp        = "+" ("+  str(Main_Delta_Temp1)  + ", " + str(Main_Delta_Temp2)  + ") [°C]" )
    
    
    print("\nHeatpump_State         = "+" ("+  str(Heatpump_State1) + ", " + str(Heatpump_State2) + ") [1=on, 0=off]" )
    print("Defrosting_State       = "+" ("+  str(Defrosting_State1) + ", " + str(Defrosting_State2) + ") [1=on, 0=off]" )
    print("Error                  = "+" ("+  str(Error1) + ", " + str(str(Error2)) + ") [Hxx]" )
    
    
    print("Heating_Off_Out_Temp   = "+" ("+  str(Heating_Off_Outdoor_Temp1) + ", " + str(Heating_Off_Outdoor_Temp2) + ") [°C]" )

    print("\nCompressor_Freq        = "+" ("+  str(Compressor_Freq1) + ", " + str(Compressor_Freq2) + ") [Hz]" )
    print("Outside_Pipe_Temp      = "+" ("+  str(Outside_Pipe_Temp1) + ", " + str(Outside_Pipe_Temp2) + ") [°C]" )

    print("Main_Hex_Outlet_Temp   = "+" ("+  str(Main_Hex_Outlet_Temp1) + ", " + str(Main_Hex_Outlet_Temp2) + ") [°C]" )
    print("Inside_Pipe_Temp       = "+" ("+  str(Inside_Pipe_Temp1) + ", " + str(Inside_Pipe_Temp2) + ") [°C]" )


    print("High_Pressure          = "+" ("+  str(High_Pressure1) + ", " + str(High_Pressure2) + ") [Kgf/cm2 ~ Bar]" )
    print("Pump_Flow              = " +" ("+  str(Pump_Flow1) + ", " + str(Pump_Flow2) + ") [l/min]" )
    print("Pump_Speed             = "+" ("+  str(Pump_Speed1) + ", " + str(Pump_Speed2) + ") [r/min]" )
    print("Fan1_Motor_Speed       = " +" ("+  str(Fan1_Motor_Speed1) + ", " + str(Fan1_Motor_Speed2) + ") [r/min]" )


    Heat_Power_Production = int(Heat_Power_Production1) + int(Heat_Power_Production2)
    print("\nHeat_Power_Production  = ",  Heat_Power_Production, end='')
    print(" ("+  str(Heat_Power_Production1) + ", " + str(Heat_Power_Production2) + ") [Watt]" )
  
    Heat_Power_Consumption =int(Heat_Power_Consumption1) + int(Heat_Power_Consumption2)     
 
    print("Heat_Power_Consumption = ",  Heat_Power_Consumption, end='')
    print(" ("+  str(Heat_Power_Consumption1) + ", " + str(Heat_Power_Consumption2) + ") [Watt]" )

    print("Operations_Hours       = "+" ("+  str(Operations_Hours1) + ", " + str(Operations_Hours2) + ") [h]" )
    print("Operations_Counter     = "+" ("+  str(Operations_Counter1) + ", " + str(Operations_Counter2) + ") [ ]" )


'''
    delta = int(Main_Target_Temp1) - int(Main_Target_Temp2)
    print("Main_Target_Temp = " , Main_Target_Temp1)
    print("Main_Target_Temp2 = " , Main_Target_Temp2)

    if( delta != 0):
        set_heishamon(IP2, "SetZ1HeatRequestTemperature", delta)
'''











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
        check_Main_Target_Temp(IP1, IP2)
        for i in range(0, 10):
            time.sleep(1)
            print('.', end="")

if __name__ == "__main__":
    main()
    
# http://192.168.188.25/command?SetZ1HeatRequestTemperature=2    
# http://192.168.188.173/command?SetZ1HeatRequestTemperature=2
 # http://192.168.188.25/command?SetHeatpump=1
# http://192.168.188.173/command?SetHeatpump=1

    
    