from mido import MidiFile

midi_file ='Alle_Meine_Entchen.mid'

mid = MidiFile(midi_file, clip=True)
print(mid)

for track in mid.tracks:
    print(track)

for msg in mid.tracks[0]:
    print(msg)
    
    
print(' '  )
print('open MIDI File: ' + str(midi_file) )
 
cv1 = MidiFile(midi_file, clip=True)

message_numbers = []
duplicates = []

for track in cv1.tracks:
    print(track)
    if len(track) in message_numbers:
        print('duplicates.append')
        duplicates.append(track)
    else:
        print('message_numbers.append : ' + str(len(track)))
        message_numbers.append(len(track))



print('track in duplicates')

for track in duplicates:
    print(track)
    cv1.tracks.remove(track)




print('Save MIDI File: ' )
cv1.save('new_song.mid')   