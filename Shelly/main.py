#import requests
#import json
#import socket
from shelly import shelly
from iobroker import iobroker




"""
{

"wifi_sta":{"connected":true,"ssid":"FRITZ!Box 7590 GM","ip":"192.168.188.27","rssi":-68},
"cloud":{"enabled":true,"connected":true},
"mqtt":{"connected":false},
"time":"12:11",
"unixtime":1610885482,
"serial":382,
"has_update":false,
"mac":"68C63AFB3138",
"cfg_changed_cnt":1,

"actions_stats":{"skipped":0},
"relays":[{"ison":false,"has_timer":false,"timer_started":0,"timer_duration":0,"timer_remaining":0,"overpower":false,"is_valid":true,"source":"input"}],
"emeters":[
{"power":172.56,"pf":0.96,"current":0.79,"voltage":227.50,"is_valid":true,"total":229643.1,"total_returned":47791.2},
{"power":183.93,"pf":0.65,"current":1.26,"voltage":226.81,"is_valid":true,"total":496613.5,"total_returned":141988.1},
{"power":-21.53,"pf":-0.11,"current":0.88,"voltage":226.74,"is_valid":true,"total":102768.8,"total_returned":8590.9}
],
"fs_mounted":true,

"update":{"status":"idle","has_update":false,"new_version":"20201124-092854/v1.9.0@57ac4ad8","old_version":"20201124-092854/v1.9.0@57ac4ad8"},
"ram_total":49296,
"ram_free":29152,
"fs_size":233681,
"fs_free":150851,
"uptime":725}
 
 """
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

def my_map(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


ip_pcWohnzimmer = "192.168.188.35"
ip_Heitzung     = "192.168.188.36" # Heizung tempeaturen
ip_Brauchwasser = "192.168.188.37" # Heizung tempeaturen


heitzung    = shelly(ip_Heitzung)
bw_speicher = shelly(ip_Brauchwasser)
pc_wohnzimmer= shelly(ip_pcWohnzimmer)


print('aussen_Temperatur   = ', heitzung.get_temperature( 0), '°C' )
print('kessel_Temperatur   = ', heitzung.get_temperature( 1), '°C' )
temp = heitzung.get_temperature( 2)
print('speicher_Temperatur = ', temp, '°C' )

soc = my_map( temp, 35, 65, 0, 100)

print('soc speicher        = ', soc, '%' )
print('')
print('ip_pcWohnzummer     = ', pc_wohnzimmer.get_power(0), 'W' )
print('bw_speicher         = ', bw_speicher.get_power(0), 'W' )

#bw_speicher.set_relay('toggel')


evu_power         ='http://iobroker01:8087/getPlainValue/node-red.0.EVU.TotalPower'
evu_energie       ='http://iobroker01:8087/getPlainValue/node-red.0.Haus.TotalEnergie'
evu_ret_energie   ='http://iobroker01:8087/getPlainValue/node-red.0.EVU.EnergieReturned'
pv_power          ='http://iobroker01:8087/getPlainValue/node-red.0.PV.Power'
pv_energie        ='http://iobroker01:8087/getPlainValue/node-red.0.PV.TotalEnergie'

evu = iobroker()
print('')
print('EVU Bezug leistung = ', evu.get_raw( evu_power) , 'W')
print('EVU Bezug Energie  = ', evu.get_raw( evu_energie) , 'kWh')
print('EVU Export         = ', evu.get_raw( evu_ret_energie) , 'W')

print('PV Leistung        = ', evu.get_raw( pv_power) , 'W')
print('PV Energie Total   = ',  evu.get_raw( pv_energie) , 'kWh')





