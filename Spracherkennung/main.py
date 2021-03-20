

import sounddevice as sd
import numpy as np
import time
from math import pi

#print(sd.query_devices())
#print('Default Devise : ' + str(sd.default.device))

# https://python-sounddevice.readthedocs.io/en/0.4.1/examples.html#play-a-sine-signal



DefaultDevice = 28



SamplingFrequenz = 16000

SoundTime = 1


#
# Record sound
#

def getSound( frequenz):
    n = np.arange( 0, SoundTime, 1/SamplingFrequenz)
    sound = np.sin( 2 * pi * frequenz * n)
    return sound

'''
s1 = getSound(1000)
s2 = getSound(4123)
soundwave = s1 + s2
sd.play( soundwave, SamplingFrequenz)
sd.wait()

s1 = getSound(1000)
s2 = getSound(500)
soundwave = s1 + s2
sd.play( soundwave, SamplingFrequenz)
sd.wait()

s1 = getSound(1000)
s2 = getSound(4123)
soundwave = s1 + s2
sd.play( soundwave, SamplingFrequenz)
sd.wait()

FrequezList = [220, 233.082, 246.942, 261.6, 277.183, 311.127, 329.628, 349.228, 369.994, 391.995, 415.305, 440.0]
SoundTime = 0.5
for f in FrequezList: 
    sd.play( getSound( f ), SamplingFrequenz)
    sd.wait()
'''
SoundTime = 0.8
'''
for n in range(37, 49+1):
    frequenz = 1.0594630943593**(n-49) * 440# f(n) = (12SQR(2) ⁽n-49) *440 Hz
    print('Taste ' + str(n) +'  Frequenz : ' + str(frequenz))
    sd.play( getSound( frequenz ), SamplingFrequenz)
    sd.wait()

for n in range(25, 88+1):
    frequenz = 1.0594630943593**(n-49) * 440# f(n) = (12SQR(2) ⁽n-49) *440 Hz
    print('Taste ' + str(n) +'  Frequenz : ' + str(frequenz))
    sd.play( getSound( frequenz ), SamplingFrequenz)
    sd.wait()
'''

alle_meine_Endchen = [40, 41, 42, 43, 0, 44, 44, 0, 45,45,45,45,0 , 44, 43, 43, 43,43,0, 42,42,0, 44, 44, 44, 40]
SoundTime = 0.4

for n in alle_meine_Endchen:
    n= n-5
    frequenz = 1.0594630943593**(n-49) * 440# f(n) = (12SQR(2) ⁽n-49) *440 Hz
    print('Taste ' + str(n) +'  Frequenz : ' + str(frequenz))
    if n == 0:
        time.sleep(SoundTime/2)  
    else:
        sd.play( getSound( frequenz ), SamplingFrequenz)
        sd.wait()



#
# Record sound
#

print( 'Record Sound...')
fs = 48000
duration = 5

data = sd.rec(int(duration * fs), channels=2)
sd.wait()
print(data.shape)

print( 'Play Sound...')
sd.play( data, fs )





