from shelly import shelly
from iobroker import iobroker
import time
import os

'''
def getHostname(ip):
    return socket.gethostbyaddr(ip)

def getHostnameRange(ip):
    res = ""
    for i in range(1, 256):
        
        host_to_check = ip + str(i)
        try:
            host_check = socket.gethostbyaddr(host_to_check)
            print( str(i) + " -> " + str(host_check))
        except socket.herror:
            #print 'Kein Dns-Eintrag für {}'.format(host_to_check)
            pass
        except socket.gaierror:
            #print 'Fehlerhafte Eingabe bei den Netzwerkadressen!'
            break

#print(getHostname("192.168.188.27" ))

#getHostnameRange("192.168.188.")

IP_Heitzung = "http://192.168.188.36/status" # Heizung tempeaturen
ip_Brauchwasser = "http://192.168.188.37/status" # Heizung tempeaturen

r = requests.get(IP_Heitzung) # Daten abfragen

data    = json.loads(r.content)    
print('Data ==: ',str(data))
print(" ")

ssid  = data['wifi_sta']['ssid'] 
ip    = data['wifi_sta']['ip'] 
mac   = data['mac'] 

'''



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
    
    
@static_vars(counter1=0)    
def set_BW_Heizleistung(Leistung): # aktuell freie leistung 
    global Current_State
    global Power_State
    global _Leistung
    set_BW_Heizleistung.counter1 +=1
    
       
    if not hasattr(set_BW_Heizleistung,"counter3"):
        set_BW_Heizleistung.counter3=0
    
    set_BW_Heizleistung.counter3 += 1 
    
    
    
    print('counter1', set_BW_Heizleistung.counter1)
    print('counter3', set_BW_Heizleistung.counter3)

    ip_1KW = "192.168.188.60" # Heizung tempeaturen
    ip_2KW = "192.168.188.52" # Heizung tempeaturen
    
    Heizstab_1000W = shelly(ip_1KW)
    Heizstab_2000W = shelly(ip_2KW)

    akt_Power_1KW  =  Heizstab_1000W.get_power(0)
    akt_Power_2KW  =  Heizstab_2000W.get_power(0)
    
    
    Schalt_Leistung = akt_Power_1KW + akt_Power_1KW + Leistung
        
    
    if Schalt_Leistung < 1000:   # Alles auschalten
        Heizstab_1000W.set_relay(0)
        Heizstab_2000W.set_relay(0)
        Power_State = 0
        return 0
    elif Schalt_Leistung < 2000: # 1000W schalten
        Heizstab_1000W.set_relay(1)
        Heizstab_2000W.set_relay(0)
        Power_State = 1
        return 1000
    elif Schalt_Leistung < 3000: # 2000W schalten
        Heizstab_1000W.set_relay(0)
        Heizstab_2000W.set_relay(1)
        Power_State = 2
        return 2000
    elif Schalt_Leistung < 10000: # 3000W schalten
        Heizstab_1000W.set_relay(1)
        Heizstab_2000W.set_relay(1)
        Power_State = 3
        return 3000
    else:
        print('Maximal Leisrung 3000W')
        return -1
    


def my_map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

evu_power         ='http://iobroker01:8087/getPlainValue/node-red.0.EVU.TotalPower'
evu_energie       ='http://iobroker01:8087/getPlainValue/node-red.0.Haus.TotalEnergie'
evu_ret_energie   ='http://iobroker01:8087/getPlainValue/node-red.0.EVU.EnergieReturned'
pv_power          ='http://iobroker01:8087/getPlainValue/node-red.0.PV.Power'
pv_energie        ='http://iobroker01:8087/getPlainValue/node-red.0.PV.TotalEnergie'

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
Loop_Counter = 0
os.environ['TERM'] = 'xterm'
while True:
    
    clearConsole()
    
    Loop_Counter += 1

    temp            = heitzung.get_temperature( 2)
    PV_Leistung     = evu.get_raw( pv_power)*-1 
    BW_Speicher_soc = my_map( temp, 40, 70, 0, 100)
    EVU_Netz_Bezug = evu.get_raw( evu_power)
    
    if EVU_Netz_Bezug < 0:
        EVU_Netz_Export = EVU_Netz_Bezug* -1.0
    else:
        EVU_Netz_Export = 0
        
    EVU_Netz_exp =  EVU_Netz_exp_alt *0.7 + EVU_Netz_Export*0.3    
    EVU_Netz_exp_alt= EVU_Netz_exp
    
    if (BW_Speicher_soc < 100):
        Speicher_Lade_Leistung = set_BW_Heizleistung( EVU_Netz_exp )
    
    if (BW_Speicher_soc >= 100) :
        Speicher_Lade_Leistung = set_BW_Heizleistung( 0 )
  
    #print('aussen_Temperatur   = ', heitzung.get_temperature( 0), '°C' )
    #print('kessel_Temperatur   = ', heitzung.get_temperature( 1), '°C' )
    import time

    # seconds passed since epoch
    seconds = time.time()
    local_time = time.ctime(seconds)
    print('Brauchwasser-Speicher PV-Überschuß Ladereglung ' )    
    print(local_time, '(loop=%d)' % Loop_Counter)    
    print('-------------------------------------------------------------' )
    print("|     PV: %4.0dW              |    Netz_exp.: %4.0f W" % (PV_Leistung, EVU_Netz_Export ))
    print('-------------------------------------------------------------' )
    print("|     SoC: %2.0d %%              |    Temperatur: %2.2f °C" % (BW_Speicher_soc, temp))
    print('-------------------------------------------------------------' )
    print("|     akt. Power: %4.0dW      |    Filter(Netz_exp): %4.0f W" % (Speicher_Lade_Leistung, EVU_Netz_exp))
    print('-------------------------------------------------------------' )
    print('' )

    time.sleep(10)




