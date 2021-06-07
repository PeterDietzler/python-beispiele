from shelly import shelly
from iobroker import iobroker
import time
import os
import json
import string



def myPrint( text, level):
    local_time = time.localtime() # get struct_time
    time_string = time.strftime("%Y.%m.%d %H:%M:%S", local_time)

    FileTime = time.strftime("%Y.%m.%d", local_time)
    
    myString = time_string + ' | '+  str(level) +' | ' + text + '\n'
    f = open("log/" + FileTime + "_WW_Speicher.log", "a")
    f.write( myString)  
    f.close()

def logTemperatur( temp, intervall):
    local_time = time.localtime() # get struct_time
    time_string = time.strftime("%Y.%m.%d %H:%M:%S", local_time)

    myString = time_string + '\t' +str(temp) + '\n'
    f = open("log/Temperatur.log", "a")
    f.write( myString)  
    f.close()
    pass
                   

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)
    
def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate    
    
# EVU_Netz_export ==>> positiv(+) für Netzeinspeisung Netzbezug, negativ(-) für  Netzbezug
#
def set_BW_Heizleistung( EVU_Netz_export ): # aktuell freie leistung 
    global Current_State
    global Power_State
    global _Leistung
    ip_1KW = "192.168.188.60" # Shelly 1PM Heizung 1kW
    ip_2KW = "192.168.188.52" # Shelly 1PM Heizung 2kW
    
    Heizstab_1000W = shelly(ip_1KW)
    Heizstab_2000W = shelly(ip_2KW)

    
    akt_Power = Heizstab_1000W.get_power(0) + Heizstab_2000W.get_power(0)
    
    
    #if EVU_Netz_export - akt_Power <=10:
        #return akt_Power
    
    '''
    else:
        Schalt_Leistung = akt_Power + EVU_Netz_export
    '''
    Schalt_Leistung = EVU_Netz_export
    
    if Schalt_Leistung < 1:   # Alles auschalten
        myPrint('Heizstab aus', 0)
        Heizstab_1000W.set_relay(0)
        time.sleep(1)
        Heizstab_2000W.set_relay(0)
        return 0
    
    elif Schalt_Leistung < 1000:   # Alles auschalten
        myPrint('Heizstab aus', 0)
        Heizstab_1000W.set_relay(0)
        time.sleep(1)
        Heizstab_2000W.set_relay(0)
        return 0
    
    elif Schalt_Leistung < 2000: # 1000W schalten
        myPrint('Heizstab 1000W', 0)
        Heizstab_2000W.set_relay(0)
        time.sleep(1)
        Heizstab_1000W.set_relay(1)
        return 1000

    elif Schalt_Leistung < 3100: # 2000W schalten
        myPrint('Heizstab 2000W', 0)
        Heizstab_1000W.set_relay(0)
        time.sleep(1)
        Heizstab_2000W.set_relay(1)
        return 2000
    
    elif Schalt_Leistung < 4000: # 3000W schalten
        myPrint('Heizstab 3000W', 0)
        Heizstab_1000W.set_relay(1)
        time.sleep(1)
        Heizstab_2000W.set_relay(1)
        return 3000
    else:
        print('Maximal Leisrung 3000W')
        return -1
    
def set_Soco_Charger( power):
    myPrint('Soco_Charger() ', 0)
    pass


def my_map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)




def reset_log_files():
    f = open("log/" + "PV_Energie_Wh.log", "w")
    f.write( str(0.000) )  
    f.close()
  
  
    f = open("log/" + "HausEnergie_Export_Wh.log", "w")
    f.write( str(0.000) )  
    f.close()
  
    f = open("log/" + "HausEnergie_Verbrauch_Wh.log", "w")
    f.write( str(0.000) )  
    f.close()
  
    f = open("log/" + "HausEnergie_Import_Wh.log", "w")
    f.write( str(0.0001) )  
    f.close()
  
    f = open("log/" + "WW_Speicher_Energie_Wh.log", "w")
    f.write( str(0.0001) )  
    f.close()



def ueberschuss_laden():

    evu_Total_Power   ='http://iobroker01:8087/getPlainValue/node-red.0.EVU.TotalPower'
    evu_energie       ='http://iobroker01:8087/getPlainValue/node-red.0.Haus.TotalEnergie'
    evu_ret_energie   ='http://iobroker01:8087/getPlainValue/node-red.0.EVU.EnergieReturned'
    pv_power          ='http://iobroker01:8087/getPlainValue/node-red.0.PV.Power'
    pv_energie        ='http://iobroker01:8087/getPlainValue/node-red.0.PV.TotalEnergie'
    bwPumpe           ='http://iobroker01:8087/getPlainValue/node-red.0.Heizung.BrauchwasserPumpe'
    ip_pcWohnzimmer = "192.168.188.35"
    ip_Heitzung     = "192.168.188.36" # Heizung tempeaturen
    ip_Brauchwasser = "192.168.188.37" # Heizung tempeaturen

    heitzung    = shelly(ip_Heitzung)
    bw_speicher = shelly(ip_Brauchwasser)
    pc_wohnzimmer= shelly(ip_pcWohnzimmer)
    BW_Speicher_Heizung = 0
    Aktueller_Eigenverbarauch = 0
    PV_Leistung = 0

    evu = iobroker()

    EVU_Netz_exp = 0
    EVU_Netz_exp_alt = 0
    PV_Leistung_alt=0
    PV_Leistung_filter=0
    Loop_Time = 5 # Sekunden
    Speicher_Lade_Leistung =0
    os.environ['TERM'] = 'xterm'
    
    #reset_log_files()

  

    
    HausEnergie_Export_Wh = 0
    HausEnergie_Import_Wh = 0
    HausEnergie_Verbrauch_Wh = 0
    WW_Speicher_Energie_Wh = 0.0
    EVU_Netz_Bezug =0
    EVU_Netz_exp_alt =0
    seconds_alt =time.time()
    EVU_Zähler=0
    myexit = False
    PV_Energie_Wh =0
    while (myexit == False):

        
        clearConsole()
        local_time = time.localtime() # get struct_time
        _std = time.strftime("%H", local_time)
        _min = time.strftime("%M", local_time)
        _sec = time.strftime("%S", local_time)
        _day = time.strftime("%d", local_time)
        _month = time.strftime("%m", local_time)
        _jahr = time.strftime("%Y", local_time)
        _date = time.strftime("%Y%m%d", local_time)
        # Monatlich in s yearly Verzeichnis
   
        # TODO
   
        # Täglich daten wegschreiben
        if _std == '23' and _min == '59' and _sec > '50' and _sec < '59':
            print(" reset_log_files():",_std, _min,_sec)
            
            # Schriebe die Daten in Datei            
            f = open("log/logging/monthly/" + _jahr + _month +".csv", "a+")
            output =[ EVU_Zähler, HausEnergie_Verbrauch_Wh, PV_Energie_Wh, HausEnergie_Export_Wh, HausEnergie_Import_Wh, WW_Speicher_Energie_Wh] 
            f.write( _date  )  
            for value in output:
                f.write( ", %d" % (value) )  
            f.write( "\n" )  
            f.close()

            reset_log_files()
            HausEnergie_Export_Wh = 0.0
            HausEnergie_Import_Wh = 0.0 
            time.sleep(5)
            
        # alle 5 Minuten daten schreiben
        if  ((int(_min) % 5) == 0) and _sec > '00' and _sec < '09':
            # Schriebe die Daten in Datei            
            f = open("log/logging/dayly/" + _date +".csv", "a+")
            output =[ EVU_Zähler, HausEnergie_Verbrauch_Wh, PV_Energie_Wh, HausEnergie_Export_Wh, HausEnergie_Import_Wh, WW_Speicher_Energie_Wh] 
            f.write( _std + _min  )  
            for value in output:
                f.write( ", %d"% (value) )  
            f.write( "\n" )  
            f.close()
            time.sleep(5)
        # write_dayly_csv_file( path_file, var_list)    
        # write_5min_csv_file( path_file, var_list)    

        get_value_start = time.time()

        Aussen_temperatur      = heitzung.get_temperature( 0)
        Kessel_temperatur      = heitzung.get_temperature( 1)
        WarmwasserSpeicher_temperatur  = heitzung.get_temperature( 2)
        PV_Leistung     = evu.get_raw( pv_power)*-1 
        BW_Speicher_soc = my_map( WarmwasserSpeicher_temperatur, 40, 68, 0, 100)
        EVU_Netz_Bezug  = evu.get_raw( evu_Total_Power)  # positiv(+) für Netzbezug, negativ(-) für Netzeinspeisung 
       
        get_value_time = time.time() - get_value_start
                                        

        #get_value_start = time.time()

        EVU_Netz_Export = EVU_Netz_Bezug * -1.0
        
        #EVU_Netz_exp ist der gdämpte export( Filter 1er Ordnung) 
        EVU_Netz_exp =  EVU_Netz_exp_alt *0.9 + EVU_Netz_Export*0.1     
        EVU_Netz_exp_alt= EVU_Netz_exp
        
        PV_Leistung_filter =PV_Leistung_alt *0.9 + PV_Leistung*0.1
        PV_Leistung_alt = PV_Leistung_filter
        
        if EVU_Netz_exp > 0:
            Ueberschuss_Leistung = (EVU_Netz_exp) +Speicher_Lade_Leistung
        else:
            Ueberschuss_Leistung =0;
        
        
        #Ueberschuss_Leistung = PV_Leistung_filter
        
        
        
        if (Aussen_temperatur > 21.0):
            soc_max = 88
        else:
            soc_max = 98
        
        if (WarmwasserSpeicher_temperatur < 63.0):
            #if temp <= 65.6 or Kessel_temperatur < 55:              
            if Ueberschuss_Leistung < 900 or Ueberschuss_Leistung < 0:
                Speicher_Lade_Leistung = set_BW_Heizleistung( 0)
                
            elif (Ueberschuss_Leistung > 1100) and (Ueberschuss_Leistung < 1950):
                Speicher_Lade_Leistung = set_BW_Heizleistung( 1000)
                
            elif (Ueberschuss_Leistung > 2200) and (Ueberschuss_Leistung < 2900):
                Speicher_Lade_Leistung = set_BW_Heizleistung( 2000)
                
            elif Ueberschuss_Leistung > 3000:
                    Speicher_Lade_Leistung = set_BW_Heizleistung( 3000)
        
        elif (WarmwasserSpeicher_temperatur > 65.0):
            Speicher_Lade_Leistung = set_BW_Heizleistung( 0 )
        
        f = open("log/" + "PV_Energie_Wh.log", "r")
        PV_Energie_Wh_alt = f.readline()  
        f.close()
        PV_Energie_Wh = float(PV_Energie_Wh_alt) + (PV_Leistung*1.0 * Loop_Time*1.0) / 3600
        f = open("log/" + "PV_Energie_Wh.log", "w")
        f.write( str(PV_Energie_Wh) )  
        f.close()
        

        if EVU_Netz_Bezug > 0.000:
            f = open("log/" + "HausEnergie_Import_Wh.log", "r")
            HausEnergie_Import_Wh_alt = f.readline()  
            f.close()
            HausEnergie_Import_Wh = float(HausEnergie_Import_Wh_alt) + (EVU_Netz_Bezug*1.0 * Loop_Time*1.0) / 3600
            f = open("log/" + "HausEnergie_Import_Wh.log", "w")
            f.write( str(HausEnergie_Import_Wh) )  
            f.close()
        else:
            f = open("log/" + "HausEnergie_Export_Wh.log", "r")
            HausEnergie_Export_Wh_alt = f.readline()  
            f.close()
            HausEnergie_Export_Wh = float(HausEnergie_Export_Wh_alt) + (EVU_Netz_Bezug*-1.0 * Loop_Time*1.0) / 3600
            f = open("log/" + "HausEnergie_Export_Wh.log", "w")
            f.write( str(HausEnergie_Export_Wh) )  
            f.close()


        f = open("log/" + "HausEnergie_Verbrauch_Wh.log", "r")
        HausEnergie_Verbrauch_Wh_alt = f.readline()  
        f.close()
        HausEnergie_Verbrauch_Wh = float(HausEnergie_Verbrauch_Wh_alt) + (PV_Leistung + EVU_Netz_Bezug) * Loop_Time / 3600.0
        f = open("log/" + "HausEnergie_Verbrauch_Wh.log", "w")
        f.write( str(HausEnergie_Verbrauch_Wh) )  
        f.close()
        
       
       
       
        f = open("log/" + "WW_Speicher_Energie_Wh.log", "r")
        WW_Speicher_Energie_Wh_alt = f.readline()
        f.close()
        #print("WW_Speicher_Energie_Wh_alt :", WW_Speicher_Energie_Wh_alt)
        WW_Speicher_Energie_Wh = float(WW_Speicher_Energie_Wh_alt) + Speicher_Lade_Leistung * Loop_Time / 3600.0
        #f = open("log/" + "WW_Speicher_Energie_Wh.log", "w")
        f = open("log/" + "WW_Speicher_Energie_Wh.log", "w")
        f.write( str(WW_Speicher_Energie_Wh) )  
        f.close()
        
        f = open("log/" + "EVU_Zähler.log", "r")
        EVU_Zähler_alt = f.readline()
        f.close()
        EVU_Zähler = float(EVU_Zähler_alt) + EVU_Netz_Bezug * Loop_Time /3600.0
        f = open("log/" + "EVU_Zähler.log", "w")
        f.write( str(EVU_Zähler) )  
        f.close()
        
        #get_value_time = time.time() - get_value_start
        
        
        # seconds passed since epoch
        seconds = time.time()
        Loop_Time = Loop_delay = seconds - seconds_alt
        print("Loop_delay:", Loop_delay)    
        print("get_value_time:", get_value_time)
        seconds_alt =seconds
        
        
        local_time = time.ctime(seconds)
        print('Warm-Wasser-Speicher PV-Überschuß Ladereglung ' )    
        print(local_time)    
        print('---------------------------------------------------------------------' )
        print("|     PV ges.   : %4.0dW (%4.3fkWh)     |    PV_filter.   : %4.0fW" % (PV_Leistung, (PV_Energie_Wh/1000.0),PV_Leistung_filter ))
        print('---------------------------------------------------------------------' )
        print("|     Haus      : %4.0dW (imp. %4.3fkWh | exp. %4.3fkWh)" % ((EVU_Netz_Bezug), (HausEnergie_Import_Wh/1000.0), (HausEnergie_Export_Wh/1000.0)))
        print('---------------------------------------------------------------------' )
        print("|     Haus verb.: %4.0dW ( %4.3fkWh)    | EVU-Zähler( %4.3fkWh))" % ((PV_Leistung + EVU_Netz_Bezug), (HausEnergie_Verbrauch_Wh/1000.0),EVU_Zähler/1000.0 ) )
        print('---------------------------------------------------------------------' )
        print("|     WW Power  : %4.0dW ( %4.3fkWh)    |    Ueberschuß %4.0fW" % (Speicher_Lade_Leistung, WW_Speicher_Energie_Wh/1000.0, Ueberschuss_Leistung))
        print('---------------------------------------------------------------------' )
        print("|     WW SoC    : %2.0d%%               |    WW Temp     : %2.2f°C" % (BW_Speicher_soc, WarmwasserSpeicher_temperatur))
        print('---------------------------------------------------------------------' )
        print('' )
        
        time.sleep(5)

# WW-Speicher als Energie vernichter
# kondstant auf 67 °C halten
#
def maximal_laden():
     
    myPrint('Starte Programm maximal_laden()', 0)
    # 1. Temperaturen  ermitteln
    ip_Heitzung     = "192.168.188.36" # Heizung tempeaturen
    heitzung    = shelly(ip_Heitzung)
    
 
    # 3. Heitzstab einbinden      
    ip_1KW = "192.168.188.60" # Shelly 1PM Heizung 1kW
    ip_2KW = "192.168.188.52" # Shelly 1PM Heizung 2kW
    
    Heizstab_1000W = shelly(ip_1KW)
    Heizstab_2000W = shelly(ip_2KW)

    ip_WW_PumpenPower ='http://iobroker01:8087/getPlainValue/node-red.0.Heizung.BrauchwasserPumpe'
    iob = iobroker()
    
    WW_Power_counter = 0
     
    os.environ['TERM'] = 'xterm'
    while True:
        clearConsole()

        Aussen_temperatur      = heitzung.get_temperature( 0)
        Kessel_temperatur      = heitzung.get_temperature( 1)
        WW_Speicher_temperatur = heitzung.get_temperature( 2)
        
        logTemperatur( WW_Speicher_temperatur, 0)

        WW_Speicher_soc = my_map( WW_Speicher_temperatur, 40, 67, 0, 100)

        WW_PumpenPower = iob.get_raw(ip_WW_PumpenPower)
        if WW_PumpenPower > 10:
            if WW_Power_counter ==0:
                myPrint('WW_PumpenPower ein,  Temp= %2.1f°C' % (WW_Speicher_temperatur), 0)
            WW_Power_counter += 5
        else:
            if WW_Power_counter >0:
                myPrint('WW_PumpenPower aus, Temp= %2.1f°C' % (WW_Speicher_temperatur), 0)
            WW_Power_counter = 0
    
        
        

        akt_Power = Heizstab_1000W.get_power(0) + Heizstab_2000W.get_power(0)
        if akt_Power > 1:
            if WW_Speicher_temperatur >= 67.3 or WW_Power_counter > (60*5):
                myPrint('Heizstab aus, Temp= %2.1f°C' % (WW_Speicher_temperatur), 0)
                Heizstab_1000W.set_relay(0)
                time.sleep(1)
                Heizstab_2000W.set_relay(0)
        else: # power = 0
            if WW_Speicher_temperatur <= 65.6 and WW_PumpenPower <10:
                '''
                if Aussen_temperatur > 20: # Nur Brauchwasser erwärmung
                    # PV-Überschuss in Brauchwasser Speicher verheitzen
                    if WW_Speicher_temperatur <= 60.0:
                        myPrint('Heizstab(3KW) ein, Temp= %2.1f°C' % (WW_Speicher_temperatur), 0)
                        Heizstab_1000W.set_relay(1)
                        time.sleep(1)
                        Heizstab_2000W.set_relay(1)
                     
                    if WW_Speicher_temperatur >= 65.0:
                        myPrint('Heizstab aus, Temp= %2.1f°C' % (WW_Speicher_temperatur), 0)
                        Heizstab_1000W.set_relay(0)
                        time.sleep(1)
                        Heizstab_2000W.set_relay(0)

                elif Aussen_temperatur > 19.5:
                    myPrint('Heizstab(1KW) ein, Temp= %2.1f°C' % (WW_Speicher_temperatur), 0)
                    Heizstab_1000W.set_relay(1)
                    pass    
                elif Aussen_temperatur > 19:
                    myPrint('Heizstab(2KW) ein, Temp= %2.1f°C' % (WW_Speicher_temperatur), 0)
                    Heizstab_2000W.set_relay(1)
                else:
                    myPrint('Heizstab(3KW) ein, Temp= %2.1f°C' % (WW_Speicher_temperatur), 0)
                    Heizstab_1000W.set_relay(1)
                    time.sleep(1)
                    Heizstab_2000W.set_relay(1)
                '''
                if Kessel_temperatur < 55:
                    myPrint('Heizstab(3KW) ein, Temp= %2.1f°C' % (WW_Speicher_temperatur), 0)
                    Heizstab_1000W.set_relay(1)
                    time.sleep(1)
                    Heizstab_2000W.set_relay(1)
                
                
                
        local_time = time.localtime() # get struct_time
        time_string = time.strftime("%Y.%m.%d %H:%M:%S", local_time)
        
        print('Warm-Wasser-Speicher Maximale Heitzleistung' )    
        print(time_string)    
        print('-------------------------------------------------------------' )
        print("|     Kessel T  : %2.1f°C      |    Aussen T    : %4.1f°C" % (Kessel_temperatur, Aussen_temperatur ))
        print('-------------------------------------------------------------' )
        print("|     WW Power  : %4.0dW       |    WW_Pumpe    : %4.0fW (%d)" % (akt_Power, WW_PumpenPower, WW_Power_counter))
        print('-------------------------------------------------------------' )
        print("|     WW SoC    : %2.0d%%        |    WW Temp     : 65.6°C < %2.1f°C < 67.3°C" % (WW_Speicher_soc, WW_Speicher_temperatur))
        print('-------------------------------------------------------------' )
        print('' )
        '''
        print(" 0 speicher:%2.1f Kessel:%2.1f Aussen: %2.1f 80" % ( WW_Speicher_temperatur, Kessel_temperatur, Aussen_temperatur ))
        '''
        
 

        time.sleep(5)
    


ueberschuss_laden()
#maximal_laden()


def main():
    
    # Lade SystemHardware.json
     
    
    EVU_Zaehlerstand_2020 = 30248.0 # KWH 16 Juni 2020
    EVU_Zaehlerstand_2021 = 32088.0 # KWH  1 Juni 2121
    
    
    
    while True:
        
        
        mySTATE = 'SommerBetrieb'
 
 
        # TODO
        # 1. Was ist Billiger? WW mit Heizung oder elektrisch
        #    - 1 KWh EVU-Bezug kosten 30 Cent == 30 Minuten Gas Kessel
        #    -  
        # 2. Hat WW-Speicher immer vorrang?
        
        
        if mySTATE == 'SommerBetrieb':
            # WW-Speicher mit Strom aus PV-Überschuss und der rest mit EVU Bezug.
            # Die Heizung soll nicht anspringen
            pass
        
        if mySTATE == 'SommerBetrieb_Überschuss':
            # WW-Speicher nur mit Strom aus PV-Überschuss.
            # Wenn es nicht reicht geht die Heizung an.
            pass
 
        
        elif mySTATE == 'StromHeizen':
            # 3. Heizen mit Elektrisch.
            pass

        


