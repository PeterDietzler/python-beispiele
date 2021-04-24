from shelly import shelly
from iobroker import iobroker
import time



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
def set_BW_Heizleistung(Leistung): # aktuell freie leistung 
    global Current_State
    global Power_State
    global _Leistung
    ip_1KW = "192.168.188.37" # Heizung tempeaturen
    ip_2KW = "192.168.188.43" # Heizung tempeaturen
    Heizstab_1000W = shelly(ip_1KW)
    Heizstab_2000W = shelly(ip_2KW)
    current_Power_1000W    =  Heizstab_1000W.get_power(0)
    #current_Power_2000W    =  Heizstab_2000W.get_power(0)
    
    total_Power = current_Power_1000W #  + current_Power_2000W  
    if total_Power < 500:
        Power_State = 0
    
    if Leistung > 0:
        _Leistung = total_Power + Leistung
        
        print('BW_Leistung_calc    =', _Leistung,'W')
        if _Leistung > 1000:
            _Leistung =1000
    else:
        _Leistung = 0
        pass
    
    if _Leistung < 1000:
        # Alles auschalten
        Heizstab_1000W.set_relay(0)
        #Heizstab_2000W.set_relay(0)
        print('BW_Leistung         = 0 W')
        return 0
    elif _Leistung < 2000:
        # 1000W schalten
        Heizstab_1000W.set_relay(1)
        #Heizstab_2000W.set_relay(0)
        Power_State = 1
        print('BW_Leistung         = 1000 W')
        return 0
    elif _Leistung < 3000:
        # 2000W schalten
        Heizstab_1000W.set_relay(1)
        #Heizstab_2000W.set_relay(1)
        Power_State = 2
        print('BW_Leistung         = 3000 W')
        return 0
    elif _Leistung < 3001:
        # 3000W schalten
        Heizstab_1000W.set_relay(1)
        #Heizstab_2000W.set_relay(1)
        Power_State = 3
        print('BW_Leistung         = 3000 W')
    else:
        print('Maximal Leisrung 3000W')
    


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

BW_Heitzleistung = 0
BW_Heitzleistung_alt = 0

while True:
    temp            = heitzung.get_temperature( 2)
    PV_Leistung     = evu.get_raw( pv_power)*-1 
    BW_Speicher_soc = my_map( temp, 35, 70, 0, 100)
    EVU_Netz_Bezug = evu.get_raw( evu_power)
    
    if EVU_Netz_Bezug < 0:
        EVU_Netz_Export = EVU_Netz_Bezug* -1.0
    else:
        EVU_Netz_Export = 0
        
    BW_Heitzleistung =  BW_Heitzleistung_alt *0.7 + EVU_Netz_Export*0.3    
    BW_Heitzleistung_alt= BW_Heitzleistung
    
    if (BW_Speicher_soc < 98):
        set_BW_Heizleistung( BW_Heitzleistung )
    
    if (BW_Speicher_soc >= 100) :
        set_BW_Heizleistung( 0 )
  
    print('------------------------------' )
    #print('aussen_Temperatur   = ', heitzung.get_temperature( 0), '°C' )
    #print('kessel_Temperatur   = ', heitzung.get_temperature( 1), '°C' )

    print('BW_Speicher_soc     =', BW_Speicher_soc, '%' )
    #print('BW_Heitzstab        = ', BW_Heitzstab, 'W' )
    print('BW_Temperatur       =', temp, '°C' )
    #print('BW_Speicher_Heizung = ', BW_Speicher_Heizung)

    print('PV Leistung         =', PV_Leistung , 'W')
    print('EVU_Export_Leistung =', EVU_Netz_Export, 'W')   
    print('BW_Heitzleistung    =', BW_Heitzleistung, 'W')   
    #print('EVU_Netz_Bezug      = ', EVU_Netz_Bezug , 'W')
    
 
    time.sleep(10)




