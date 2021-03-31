# ************************
# https://techtotinker.blogspot.com/2020/11/016-esp32-micropython-web-server-esp32.html?m=1
#
import machine
import time
led = machine.Pin(2,machine.Pin.OUT)
led.off()


# ************************
# Configure the ESP32 wifi
# as Access Point mode.
import network
myssid = 'ESP32-AP-WebServer'
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
    if led.value()==1:
        led_state = 'ON'
        print('led is ON')
        R1= '2810'
        R2= '2820'
        R3= '2830'
        R4= '2840'
        R5= '2850'
        R6= '2860'
        R7= '2870'
        R8= '2880'

    elif led.value()==0:
        led_state = 'OFF'
        print('led is OFF')
        R1= '2801'
        R2= '2802'
        R3= '2803'
        R4= '2804'
        R5= '2805'
        R6= '2806'
        R7= '2807'
        R8= '2808'
    
        
    html_page = """<!DOCTYPE HTML>  
        <html>  
        <head>  
          <meta name="viewport" content="width=device-width, initial-scale=1">  
        </head>  
        <body>  
           <center><h2>ESP32 Web Server in MicroPython </h2></center>  
           <center>  
             <form>  
               <button type='submit' name="LED" value='1'> LED ON </button>  
               <button type='submit' name="LED" value='0'> LED OFF </button>  
               <button type='submit' name="measure" value='1'> Measure </button>  
             </form>  
           </center>  
           <center><p>LED is now <strong>""" + led_state + """</strong>.</p></center>  
           <center><p>R1 = <strong>""" + R1 + """</strong>.</p></center>  
           <center><p>R2 = <strong>""" + R2 + """</strong>.</p></center>  
           <center><p>R3 = <strong>""" + R3 + """</strong>.</p></center>  
           <center><p>R4 = <strong>""" + R4 + """</strong>.</p></center>  
           <center><p>R5 = <strong>""" + R5 + """</strong>.</p></center>  
           <center><p>R6 = <strong>""" + R6 + """</strong>.</p></center>  
           <center><p>R7 = <strong>""" + R7 + """</strong>.</p></center>  
           <center><p>R8 = <strong>""" + R8 + """</strong>.</p></center>
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
    led_on =  request.find('/?LED=1')
    led_off = request.find('/?LED=0')
    measure_on = request.find('/?measure=1')
    if led_on == 6:
        print('LED ON')
        print(str(led_on))
        led.value(1)
    elif led_off == 6:
        print('LED OFF')
        print(str(led_off))
        led.value(0)
    elif measure_on == 6:
        print('measure_on')
        measure_state =1
    response = web_page()
    measure_state = 0
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    
    # Socket close()
    conn.close()
    
    