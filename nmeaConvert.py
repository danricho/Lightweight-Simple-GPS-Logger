# pip install git+https://github.com/bsdz/micropyGPS.git

import sys
import time
from micropyGPS import MicropyGPS

inputFile = sys.argv[1] # eg: LOG00001.TXT
outputCSV = inputFile.split(".")[0]+'.csv' # eg: LOG00001.csv
print("Input: " + inputFile)
print("Output: " + outputCSV)

fix_type_decode = ["","NO FIX","2D FIX","3D FIX"]

my_gps = MicropyGPS()
lastTime = 0

print("Processing...")    

with open(outputCSV, 'w') as out_file:

  # -- writing CSV header row -- 
  out_file.write('DATE,TIME,SECS,LAT,LONG,"ALT\n(metres)",')
  out_file.write('"COURSE\n(deg, True)","GND SPEED\n(km/hr)",')
  # remove following line if using standard library...
  out_file.write('"LOCAL MAG VARIATION (deg, True)",')
  out_file.write('NUMBER SATS,FIX TYPE,HOR DOP,VERT DOP,POS DOP\n')
  
  # -- process the log file line by line --
  with open(inputFile) as fp:
    for line in fp:
      
      for x in line:
      
        # -- update the GPS object with the NMEA data --
        my_gps.update(x) 
        
        # -- writing to CSV if required --
        isNew = (lastTime != my_gps.timestamp)
        haveFix = (fix_type_decode[my_gps.fix_type] != "NO FIX")
        
        if isNew and haveFix:

          # -- saving a line to CSV. --
          out_file.write(my_gps.date_string('s_dmy') + ",")
          out_file.write(str(my_gps.timestamp[0]) + ":")
          out_file.write(str(my_gps.timestamp[1]) + ",")
          out_file.write(str(my_gps.timestamp[2]) + ",")
          out_file.write(my_gps.latitude_string() + ",")
          out_file.write(my_gps.longitude_string() + ",")
          out_file.write(str(my_gps.altitude) + ",")
          out_file.write(str(my_gps.course) + ",")
          out_file.write(str(my_gps.speed[2]) + ",")
          # remove following line if using standard library...
          out_file.write(str(my_gps.mag_variation) + ",")
          out_file.write(str(my_gps.satellites_in_use) + ",")
          out_file.write(fix_type_decode[my_gps.fix_type] + ",")
          out_file.write(str(my_gps.hdop) + ",")
          out_file.write(str(my_gps.vdop) + ",")
          out_file.write(str(my_gps.pdop) + "\n")
        
        lastTime = my_gps.timestamp

print("Done!")      