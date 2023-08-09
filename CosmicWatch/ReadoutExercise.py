import numpy as np
import pandas as pd
def read_cosmicwatch_output_PC(file_path):
    print(file_path)
    with open(file_path, 'r') as file:
        lines =  file.read().splitlines()
    
    # Remove header lines
    lines = lines[11:]
    
    # Extract data from each line
    comp_date = []
    event_numbers = []
    ardn_times = []
    adc_counts = []
    sipm_voltages = []
    deadtimes = []
    
    for line in lines:
        parts = line.strip().split(' ')
        
        timestamp = parts[1]
        event_number = int(parts[2])
        ardn_time = int(parts[3])
        adc_count = int(parts[4])
        sipm_voltage = float(parts[5])
        deadtime = int(parts[6])
        comp_date.append(timestamp)
        event_numbers.append(event_number)
        ardn_times.append(ardn_time)
        adc_counts.append(adc_count)
        sipm_voltages.append(sipm_voltage)
        deadtimes.append(deadtime)

    return timestamps, event_numbers, ardn_times, adc_counts, sipm_voltages, deadtimes

def read_cosmicwatch_output_SD(file_path):
    print(file_path)
    with open(file_path, 'r') as file:
        lines =  file.read().splitlines()
    
    # Remove header lines
    lines = lines[6:]
    
    # Extract data from each line
    timestamps = []
    event_numbers = []
    ardn_times = []
    adc_counts = []
    sipm_voltages = []
    deadtimes = []
    
    for line in lines:
        parts = line.strip().split(' ')
        
        event_number = int(parts[0])
        ardn_time = int(parts[1])
        adc_count = int(parts[2])
        sipm_voltage = float(parts[3])
        deadtime = int(parts[4])
        # timestamps.append(timestamp)
        event_numbers.append(event_number)
        ardn_times.append(ardn_time)
        adc_counts.append(adc_count)
        sipm_voltages.append(sipm_voltage)
        deadtimes.append(deadtime)

    return  event_numbers, ardn_times, adc_counts, sipm_voltages, deadtimes

# Get file path from user
file_path = ####input("Enter the path to the CosmicWatch output file: ")
file_from_computer=False###If using in OLED mode
file_from_SDCard=True###If using files from SD mode
# # Call the function to read the CosmicWatch output
# timestamps, event_numbers, ardn_times, adc_counts, sipm_voltages, deadtimes = read_cosmicwatch_output_PC(file_path)
# Call the function to read the CosmicWatch output
event_numbers, ardn_times, adc_counts, sipm_voltages, deadtimes = read_cosmicwatch_output_SD(file_path)
bin_size=30# in seconds
# Access the data
# print(f"First timestamp: {timestamps[0]}")
print(f"First event number: {event_numbers[0]}")
print(f"First Ardn time: {ardn_times[0]}")
print(f"First ADC count: {adc_counts[0]}")
print(f"First SiPM voltage: {sipm_voltages[0]}")
print(f"First Deadtime: {deadtimes[0]}")

# Simple check to see if the events are sequential
def sequential(l):
    l = np.asarray(l).astype(int)
    check = range(min(l),max(l)+1)

    if len(l)!=len(check):
        print('There is an event missing in the data.')
        return False

    counter = 0
    for i in range(len(l)):
        counter+=1
        if l[i]!=check[i]:
            print('Check event number: '+str(counter))
    return sum(check == l)==len(l)

if not sequential(event_numbers):
    print('Events in file are not sequential.')

if file_from_computer:
    time_stamp = []
    for i in range(len(comp_date)):
        year  = int(comp_date[i].split('-')[0])
        month = int(comp_date[i].split('-')[1])
        day   = int(comp_date[i].split('-')[2])
        hour  = int(comp_time[i].split(':')[0])
        mins  = int(comp_time[i].split(':')[1])
        sec   = int(np.floor(float(comp_time[i].split(':')[2])))
        try:  
            decimal = float('0.'+str(comp_time[i].split('.')[-1]))
        except:
            decimal = 0.0
        time_stamp.append(float(time.mktime((year, month, day, hour, mins, sec, 0, 0, 0)))+ decimal) 


    time_stamp_s     = np.asarray(time_stamp) -  min(np.asarray(time_stamp))       # The absolute time of an event in seconds
    time_stamp_ms    = np.asarray(time_stamp -  min(np.asarray(time_stamp)))*1000  # The absolute time of an event in miliseconds   
    total_time_s     = max(time_stamp) -  min(time_stamp)     # The absolute time of an event in seconds
    detector_name    = detName                                
    n_detector       = len(set(detName))
# Convert the cumulative deadtime to the deadtime between events
# The detector starts at time 0, so append a zero.
event_deadtime_ms = np.diff(np.append([0],deadtimes))

# The Arduino absolute time isn't great. Over the course of a few hours, it will be off by several seconds. 
# The computer will give you accurate time down to about 1ms. Reading from the serial port has ~ms scale uncertainty.
# The Arduino can give you a precise measurement (down to 1us), but the absolute time will drift. Expect it to be off by roughly 1min per day.
Ardn_time_ms      = np.asarray(ardn_times)
Ardn_time_s       = np.asarray(ardn_times)/1000.

Ardn_total_time_s = max(Ardn_time_s)
Ardn_total_time_ms= max(Ardn_time_s)*1000.

event_number     = np.asarray(event_numbers)  # an arrray of the event numbers
total_counts     = max(event_number.astype(int)) - min(event_number.astype(int))
adc      = adc_counts # an array of the measured event ADC value
sipm     = sipm_voltages# an array of the measured event SiPM value

event_deadtime_s   = event_deadtime_ms/1000.      # an array of the measured event deadtime in seconds
event_deadtime_ms  = event_deadtime_ms    # an array of the measured event deadtime in miliseconds
total_deadtime_ms  = max(event_deadtime_ms)       # an array of the measured event deadtime in miliseconds
total_deadtime_s   = max(event_deadtime_ms)/1000. # The total deadtime in seconds
print('Total Deadtime(s):',total_deadtime_s)

# The time between events is well described by the Arduino timestamp. 
# The 'diff' command takes the difference between each element in the array.

Ardn_event_livetime_s = np.diff(np.append([0],Ardn_time_s)) - event_deadtime_s
print('Event livetime(s):',Ardn_event_livetime_s)
print('NEvents:',len(Ardn_event_livetime_s))
print('Total Event livetime(s):',np.sum(Ardn_event_livetime_s))



#Time to Calculate!!
if file_from_computer:
    live_time= ##the livetime is defined as Ardn_total_time-total_deadtime
    weights  = ##weights=1/livetime
    count_rate       = ##counts/live_time 
    count_rate_err   = # what is the error on a counting measurement?

    

elif file_from_SDCard:
    live_time= ##the livetime is defined as Ardn_total_time-total_deadtime
    weights  = ##weights=1/livetime
    count_rate       = ##counts/live_time 
    count_rate_err   = # what is the error on a counting measurement?

    
else:
    print('Error')

# print('Count rate: '+str(np.round(count_rate,4)) +' +/- '+ str(np.round(count_rate_err,4)))
