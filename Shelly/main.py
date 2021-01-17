import requests
import json
import socket

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





print(getHostname("192.168.188.27" ))

getHostnameRange("192.168.188.")





home = "http://192.168.188.27/status"
r = requests.get(home) # Daten abfragen

data    = json.loads(r.content)    
print(str(data))
print(" ")

ssid  = data['wifi_sta']['ssid'] 
ip    = data['wifi_sta']['ip'] 

mac   = data['mac'] 



print(home + ": " + ssid + ": " + ip + ": " + mac)








