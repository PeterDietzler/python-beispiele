#!/usr/bin/env python3

import minimalmodbus
import serial
import time
import struct
import binascii
import paho.mqtt.client as paho
from time import gmtime, strftime



def umwandeln_ieee(Wert):  #Umwandlung Array of int ( 4 byte) in float nach IEEE 754
    Wert2=str(hex(Wert))
    Wert2=Wert2.replace('0x', '')
    if Wert2=='0':
       Wert2='00000000'
    Wert3=struct.unpack('>f', binascii.unhexlify(Wert2))[0]
   #Wert3= round(Wert3,3)
    return (Wert3)

#Hilfvariable im bei Auslesefehler nicht zu senden
go=True

#mqtt  Config Daten hier Eintragen
mqtt_username=""
mqtt_password=""
mqtt_server="192.168.0.2"
mqtt_port=1885
mqtt_subscribe="/Zaehler"
 
 
#print(minimalmodbus._get_diagnostic_string()) 
 
def on_subscribe(client, userdata, mid, granted_qos):
   print("Gesendet!")

def on_message(client, userdata, msg):
   print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
'''
client = paho.Client(client_id="Zaehler", clean_session=True, userdata=None, protocol=paho.MQTTv31)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.username_pw_set(mqtt_username, mqtt_password)
client.connect(mqtt_server, mqtt_port,60)
client.subscribe(mqtt_subscribe, qos=1)
'''
#Adapter für Modbus Anlegen 
#smartmeter = minimalmodbus.Instrument('/dev/ttyUSB0', 1,) # port name, slave address (in decimal)
smartmeter = minimalmodbus.Instrument('com6', 1,) # port name, slave address (in decimal)
smartmeter.serial.baudrate = 9600         # Baud
smartmeter.serial.bytesize = 8
smartmeter.serial.parity   = serial.PARITY_EVEN # vendor default is EVEN
smartmeter.serial.stopbits = 1
smartmeter.serial.timeout  = 0.6          # seconds
smartmeter.mode = minimalmodbus.MODE_RTU   # rtu or ascii mode
smartmeter.clear_buffers_before_each_transaction = False

smartmeter.debug = False # set to "True" for debug mode

#Debug Werte für L1 ausgeben

werteausgeben= False
 

while True:
    #client.loop_start()

 #Werte Abfragen

    try:
        #Adresse = smartmeter.read_register(2, 0, 3, False)   2 Byte Lesen
        # registeraddress, number_of_decimals=0, functioncode=3, signed=False
        
        Frequenz= (smartmeter.read_register( 0x130, 2 , 3, False))  # 01 03 01 31 00 01 D4 39 
        Frequenztxt = "Frequenz ist: %.3f V" % Frequenz
        print (Frequenztxt)
 
        L1Spannung= (smartmeter.read_register( 0x131, 2 , 3, False))  
        L1Spannungtxt = "L1Spannung ist: %.1f V" % L1Spannung
        print (L1Spannungtxt)
 
        Current= (smartmeter.read_register( 0x139, 2 , 3, False))  
        Currenttxt = "Current ist: %.3f A" % Current
        print (Currenttxt)
 
        #Adresse = smartmeter.read_long(2, 3, False)         4 Byte Lesen
        # registeraddress,  functioncode=3, signed=False
        
        ActivePower= umwandeln_ieee(smartmeter.read_long(0x140, 3, True, 0))
        ActivePowertxt = "ActivePower ist: %.3f kW" % ActivePower
        print (ActivePowertxt)
        
        ReactivePower = umwandeln_ieee(smartmeter.read_long(0x148, 3, True, 0))
        ReactivePowertxt = "Blindleistung ist: %.3f kVAr" % ReactivePower
        print (ReactivePowertxt)
 
        ApparentPower = umwandeln_ieee(smartmeter.read_long(0x150, 3, True, 0))
        ApparentPowertxt = "Wirkleistung ist: %f kVA" % ApparentPower
        print (ApparentPowertxt)
        
        PowerFactorL1 = (smartmeter.read_register( 0x158, 3 , 3, True)) 
        PowerFactortxt = "PowerFactorL1 ist: %.3f " % PowerFactorL1
        print (PowerFactortxt)

        AktiveEnergie = umwandeln_ieee(smartmeter.read_long( 0xA000, 3, False))   
        AktiveEnergietxt = "AktiveEnergie ist: %.3f kWh" % AktiveEnergie
        print (AktiveEnergietxt)

        ReverseEnergie = umwandeln_ieee(smartmeter.read_long( 0xA01E, 3, False))  
        ReverseEnergietxt = "ReverseEnergie ist: %.3f kWh " % ReverseEnergie
        print (ReverseEnergietxt)

        print (" ")
 
        go=True;
    except:
        print ("\nEinlesen nicht geklappt, versuche es erneut in 15 Sekunden")
        go=False;

    if go:
     #Werte Ausgeben falls gewünscht
        if werteausgeben:
            print(strftime("\n%Y-%m-%d %H:%M:%S", gmtime()))
            print ("Aktuelle Werte:")
            #AdresseTxt = "Die Slave Adresse ist: %s" % Adresse
            #print (AdresseTxt)
            L1Spannungtxt = "L1Spannung ist: %f V" % L1Spannung
            print (L1Spannungtxt)
            L1Stromtxt = "L1Strom ist: %f A" % L1Strom
            print (L1Stromtxt)
            Frequencytxt = "Frequenz ist: %f hz" % Frequency
            print (Frequencytxt)
            L1Leistungtxt = "L1Leistung ist: %f KW/h" % L1Leistung
            print (L1Leistungtxt)
            L1PowerFactortxt = "L1Power Faktor ist: %f" % L1PowerFactor
            print (L1PowerFactortxt)
            Leistung_gesamttxt = "Leistung Gesamt ist: %f KW" % Leistung_gesamt
            print (Leistung_gesamttxt)

     # Werte Senden
        '''
        #client.publish("/Zaehler/Adresse",str(Adresse), qos=1)
        client.publish("/Zaehler/L1/L1Spannung",str(L1Spannung), qos=0)
        client.publish("/Zaehler/L2/L2Spannung",str(L2Spannung), qos=0)
        client.publish("/Zaehler/L3/L3Spannung",str(L3Spannung), qos=0)
        client.publish("/Zaehler/Gesamt/Frequency",str(Frequency), qos=0)
        client.publish("/Zaehler/L1/L1Strom",str(L1Strom), qos=0)
        client.publish("/Zaehler/L2/L2Strom",str(L2Strom), qos=0)
        client.publish("/Zaehler/L3/L3Strom",str(L3Strom), qos=0)
        client.publish("/Zaehler/Gesamt/Leistung_gesamt",str(Leistung_gesamt*1000), qos=0)
        client.publish("/Zaehler/L1/L1Leistung",str(L1Leistung*1000), qos=0)
        client.publish("/Zaehler/L2/L2Leistung",str(L2Leistung*1000), qos=0)
        client.publish("/Zaehler/L3/L3Leistung",str(L3Leistung*1000), qos=0)
        client.publish("/Zaehler/L1/L1PowerFactor",str(L1PowerFactor), qos=0)
        client.publish("/Zaehler/L2/L2PowerFactor",str(L2PowerFactor), qos=0)
        client.publish("/Zaehler/L3/L3PowerFactor",str(L3PowerFactor), qos=0)
        client.publish("/Zaehler/Gesamt/Verbrauch_gesamt",str(Verbrauch_gesamt), qos=0)
        client.publish("/Zaehler/Gesamt/Strom_gesamt",str(Strom_gesamt), qos=0)
        #client.publish("/Zaehler/L1/L1Verbrauch",str(L1Verbrauch), qos=1)
        #client.publish("/Zaehler/L2/L2Verbrauch",str(L2Verbrauch), qos=1)
        #client.publish("/Zaehler/L3/L3Verbrauch",str(L3Verbrauch), qos=1)
        '''
    time.sleep(15)
    