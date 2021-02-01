import nidaqmx

with nidaqmx.Task() as task:
    #task.ai_channels.add_ai_voltage_chan("Dev3/ai0" "Dev1/ai0:Dev1/ai4")
    task.ai_channels.add_ai_voltage_chan("Dev3/ai0:Dev3/ai4")               # read 5 analog Channel
    i = 1
    while i < 5:
        result = task.read()
        i += 1    
        #result = task.read( number_of_samples_per_channel=10 )
        print(  result )


print(  result )

#print(round( result[9],3)) 
