# ************************
# https://techtotinker.blogspot.com/2020/11/016-esp32-micropython-web-server-esp32.html?m=1
#
import machine
import time
import esp32

led = machine.Pin(2,machine.Pin.OUT)
led.off()


# ************************
# Configure the ESP32 wifi
# as Access Point mode.
import network
myssid = 'ESP32-AP-WebServer-001F1F08C4CB' # 00:1F:1F:08:C4:CB'
mypassword ='12345678'


ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=myssid, password=mypassword)
while not ap.active():
    pass
print('network config:', ap.ifconfig())


# ************************
# Configure the socket connection
# over TCP/IP
import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

# ************************
# Function for creating the
# web page to be displayed
def web_page():
    espHall = esp32.hall_sensor()     # read the internal hall sensor
    #espTemperatur = esp32.raw_temperature() # read the internal temperature of the MCU, in Farenheit
    espTemperatur = (esp32.raw_temperature() - 32) * 5/9
    
    
    if led.value()==1:
        led_state = 'ON'
        print('led is ON')
        R1= 28010
        R2= 28020
        R3= 28030
        R4= 28040
        R5= 28050
        R6= 28060
        R7= 28070
        R8= 28080
 
    elif led.value()==0:
        led_state = 'OFF'
        print('led is OFF')
        R1= 2801
        R2= 2802
        R3= 2803
        R4= 2804
        R5= 2805
        R6= 2806
        R7= 2807
        R8= 2808
    
    
    html_page = """<!DOCTYPE HTML>  
        <html>  
        <head>  
          <meta name="viewport" content="width=device-width, initial-scale=1">  
        </head>  
        <body>  
           <center><h2> """ + myssid +     """ </h2></center>  
           <center><p>Projekt: python-beispiele/microPython/HalloWelt </p></center> 
           <center><p>Hall       : """ + str(espHall) +     """ mT </p></center> 
           <center><p>Temperatur : """ + str(espTemperatur) + """ °C</p></center> 
           <center>  
             <form>  
               <button type='submit' name="LED" value='1'> LED ON </button>  
               <button type='submit' name="LED" value='0'> LED OFF </button>  
             </form>  
           </center>  
           <center><p> <strong> Sinus </strong></p></center>  
           <center><p>R1 = <strong>""" + str(R1) + """</strong> R3 = <strong>""" + str(R3) + """</strong></p></center>  
           <center><p>R2 = <strong>""" + str(R2) + """</strong> R4 = <strong>""" + str(R4) + """</strong></p></center>  
           <center><p> <strong> Cosinus </strong></p></center>  
           <center><p>R5 = <strong>""" + str(R5) + """</strong> R7 = <strong>""" + str(R7) + """</strong></p></center>  
           <center><p>R6 = <strong>""" + str(R6) + """</strong> R8 = <strong>""" + str(R8) + """</strong></p></center>  
        </body>  
        </html>"""  
    return html_page


while True:
    # Socket accept() 
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))
    
    # Socket receive()
    request=conn.recv(1024)
    print("")
    print("")
    print("Content %s" % str(request))

    # Socket send()
    request = str(request)
    led_on = request.find('/?LED=1')
    led_off = request.find('/?LED=0')
    if led_on == 6:
        print('LED ON')
        print(str(led_on))
        led.value(1)
    elif led_off == 6:
        print('LED OFF')
        print(str(led_off))
        led.value(0)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    
    # Socket close()
    conn.close()
    
    