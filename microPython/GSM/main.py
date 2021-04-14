import machine

#
# https://techtotinker.blogspot.com/2020/10/014-esp32-micropython-sim800l-gsm.html
#

gsm = machine.UART(2, 115200)

#1. Check for the signal strength
gsm.write('AT+CSQ\r')

#2. Get the list of available network operators
gsm.write('AT+COPS=?\r')

#3. Determine the network operators the sim800l is currently registered
gsm.write('AT+COPS?\r')

#4. Determine if the sim800l is currently connected
gsm.write('AT+CREG?\r')

#5. Force it to connect
gsm.write('AT+CREG=1\r')

#6. Get the current battery level
gsm.write('AT+CBC\r')

#7. Turn off the echo of commands, 
# use ATE0 to turnoff and ATE1 to turnon.
gsm.write('ATE0\r')

