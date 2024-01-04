import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial

#initialize serial port
ser = serial.Serial()
ser.port = 'COM5' #Arduino serial port
ser.baudrate = 115200
ser.timeout = 10 #specify timeout when using readline()
ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
#xs = [] #store time
bs = [] #store braking power
ts = [] #for throttle power

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# This function is called periodically from FuncAnimation
def animate(i, bs, ts):
  #Aquire and parse data from serial port
  line = ser.readline()
  line_as_list = line.split(b',')
  brake_power = int(line_as_list[0])
  brake_power = map_range(brake_power, 0, 1023, 0, 100)

  throttle_value = line_as_list[1]
  throttle_as_list = throttle_value.split(b'\n')
  throttle_power = int(throttle_as_list[0])
  throttle_power = map_range(throttle_power, 0, 1023, 0, 100)
	

	# Add x and y to lists
  bs.append(brake_power)
  ts.append(throttle_power)

  bs = bs[-100:]
  ts = ts[-100:]

  # Draw x and y lists
  ax.clear()
  ax.plot(bs, label="Brake Power")
  ax.plot(ts, label="Throttle Power")

  # Format plot
  #plt.xticks(rotation=45, ha='right')
  #plt.subplots_adjust(bottom=0.1)
  plt.title('Sensor Data')
  plt.ylabel('Power')
  plt.legend(fontsize="x-large")
  #plt.axis([1, i, 0, 100]) #Use for arbitrary number of trials
  #i=i+1

# Set up plot to call animate() function periodically
#ani = animation.FuncAnimation(fig, animate, fargs=(xs, bs, ts), interval=20)
ani = animation.FuncAnimation(fig, animate, fargs=(bs, ts), interval=20)
plt.show()