import requests

class iobroker:
    def __init__(self, user='', password=''):
        #print('init shelly()')
        self.data = 0
        self.user = user
        self.password= password
        #ip = 'http://' + self.ip + '/status'
        #print('ip=', ip)

    def get_raw(self, http):
        try:
            r = requests.get(http) # Daten abfragen
            return float( r.content)
        except:
            return 0
    
    
    
    
    
    