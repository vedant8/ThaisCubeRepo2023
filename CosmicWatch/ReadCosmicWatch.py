import numpy as np
import pandas as pd
def read_cosmicwatch_output(file_path):
    print(file_path)
    with open(file_path, 'r') as file:
        lines =  file.read().splitlines()
    
    # Remove header lines
    lines = lines[11:]
    
    # Extract data from each line
    timestamps = []
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
        timestamps.append(timestamp)
        event_numbers.append(event_number)
        ardn_times.append(ardn_time)
        adc_counts.append(adc_count)
        sipm_voltages.append(sipm_voltage)
        deadtimes.append(deadtime)

    return timestamps, event_numbers, ardn_times, adc_counts, sipm_voltages, deadtimes

# Get file path from user
file_path = 'CW_data.txt'#input("Enter the path to the CosmicWatch output file: ")

# Call the function to read the CosmicWatch output
timestamps, event_numbers, ardn_times, adc_counts, sipm_voltages, deadtimes = read_cosmicwatch_output(file_path)

# Access the data
print(f"First timestamp: {timestamps[0]}")
print(f"First event number: {event_numbers[0]}")
print(f"First Ardn time: {ardn_times[0]}")
print(f"First ADC count: {adc_counts[0]}")
print(f"First SiPM voltage: {sipm_voltages[0]}")
print(f"First Deadtime: {deadtimes[0]}")
