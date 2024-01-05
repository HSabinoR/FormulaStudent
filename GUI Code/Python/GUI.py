import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import threading
import pandas as pd
import time

#initialize serial port
ser = serial.Serial()
ser.port = 'COM5' #Arduino serial port
ser.baudrate = 115200
ser.timeout = 10 #specify timeout when using readline()
try:
    ser.open()
    if ser.is_open:
        print("\nAll right, serial port now open. Configuration:\n")
        print(ser, "\n")  # print serial parameters
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit()

# Create figure for plotting
fig = plt.figure()

# Graph for braking and throttle power
ax = fig.add_subplot(2, 2, 1)
brake = [] #store braking power
throttle = [] #store throttle power
lock_brake_throttle = threading.Lock()

# Graph for wheel angle
ax2 = fig.add_subplot(2, 2, 2)
angle = [] # store wheel angle
lock_angle = threading.Lock()

running = True


def map_range(x, in_min, in_max, out_min, out_max): # Similar to Arduino's map function
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min


def read_ser(): # Serial reading to run in independant thread
    global brake, throttle, running, angle
    try:
        while running:
            # Acquire and parse data from serial port
            line = ser.readline()
            if not line:
                continue  # Skip empty lines

            line_as_list = line.split(b',')
            if len(line_as_list) < 3:
                continue  # Skip incomplete lines

            brake_power = int(line_as_list[0])
            brake_power = map_range(brake_power, 0, 1023, 0, 100)

            throttle_power = int(line_as_list[1])
            throttle_power = map_range(throttle_power, 0, 1023, 0, 100)

            wheel_angle_value = line_as_list[2]
            angle_as_list = wheel_angle_value.split(b'\n')
            if len(angle_as_list) < 1:
                continue  # Skip incomplete lines

            wheel_angle = int(angle_as_list[0])
            wheel_angle = map_range(wheel_angle, 0, 1023, 0, 360)

            # Add x and y to list brake and throttle
            with lock_brake_throttle:
                brake.append(brake_power)
                throttle.append(throttle_power)

            with lock_angle:
                angle.append(wheel_angle)
        print("Threading Stopped\n")
    except Exception as e:
        print(f"An error occurred in the serial reading thread: {e}")
        running = False



def animate(i, brake, throttle, angle): # This function is called periodically from FuncAnimation
    with lock_brake_throttle:
        brake = brake[-100:]
        throttle = throttle[-100:]

    with lock_angle:
        angle = angle[-100:]

    # Draw braking and throttle graph
    ax.clear()
    ax.plot(brake, label="Brake Power", color="red")
    ax.plot(throttle, label="Throttle Power", color="green")
    
    # Draw wheel angle graph
    ax2.clear()
    ax2.plot(angle, label="Wheel Angle")

    # Format figure
    plt.xticks(rotation=90, ha='right')
    plt.suptitle('Sensor Data')
    
    # Format braking and throttle power plot
    ax.set(xlabel="Time", ylabel="Power(%)")
    ax.legend(fontsize="x-large", loc='upper left')
    ax.axis([0, 100, 0, 100])

    # Format wheel angle plot
    ax2.set(xlabel="Time", ylabel="Angle(°)")
    ax2.legend(fontsize="x-large", loc='upper left')
    ax2.axis([0, 100, 0, 360])

    # Calculate the time since the program started
    elapsed_time = time.time() - start_time

    #Update time text
    #plt.text(1.25, 1.2, 'Time(Secs): {:.2f}'.format(float(elapsed_time)), transform=ax.transAxes, horizontalalignment='right',verticalalignment='top', fontsize=22) # Prints Only in seconds
    plt.text(-30,400, 'Program Runtime: ' + time.strftime("%H:%M:%S.{}".format(str(elapsed_time % 1)[2:])[:11], time.gmtime(elapsed_time))) # Prints into hours, minutes and seconds

def save_data_on_close(event):
    global running
    if event.name == 'close_event':
        running = False
        try:
            with lock_brake_throttle:
                with lock_angle:
                    df = pd.DataFrame({'Brake Power': brake, 'Throttle Power': throttle, 'Angle': angle})
                    df.to_csv('sensor_data.csv', index=False)
        except Exception as e:
            print(f"Something went wrong with saving sensor data to sensor_data.csv: {e} \n")
        finally:
            ser.close()
            plt.close()
            run_time = time.time() - start_time
            #print("Program ran for {:.2f} seconds".format(run_time)) # Prints Only in seconds
            print("Program Exited!!")
            print('Program Runtime: ' + time.strftime("%H:%M:%S.{}".format(str(run_time % 1)[2:])[:11], time.gmtime(run_time))) # Prints into hours, minutes and seconds
        

# Connect the function to the close event
plt.gcf().canvas.mpl_connect('close_event', save_data_on_close)

start_time = time.time()

serial_Thread = threading.Thread(target=read_ser)
try:
    serial_Thread.start()
    print("Threading Started\n")
except Exception as e:
    print(f"Error ocurred: {e}\n")

# Maximize window
plt.get_current_fig_manager().window.state('zoomed')

fig.canvas.manager.set_window_title('Sensor Data')

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(brake, throttle, angle), cache_frame_data=False, interval=0)
plt.show()

# Waits for the thread to finish before exiting
serial_Thread.join()