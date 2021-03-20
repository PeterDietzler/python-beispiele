

import speech_recognition as sr



file_name = "MaxAufstehen.wav"
#file_name = input(" Get Filename:")


speech = sr.Recognizer()


def from_file( fileName ):
    with sr.AudioFile(file_name) as f:
        data =speech.record(f)
        text = speech.recognize_google( data, language= "de-DE")
        return text
        
        
def fromMicrophone():
    with sr.Microphone() as micro:
        print("Recording...  ")
        audio =speech.record( micro, duration=10)
        print("Translate...")

        text = speech.recognize_google( audio, language= "de-DE")
        return text

print( from_file( file_name )) 
    
#print( fromMicrophone() )








