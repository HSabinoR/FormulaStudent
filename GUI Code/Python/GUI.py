import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import serial.tools.list_ports
import threading
import pandas as pd
import time
from matplotlib.widgets import Button, Slider, CheckButtons

# Checks each port's description
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'USB-SERIAL CH340' in p.description or 'Arduino' in p.description
]

if not arduino_ports:
    raise IOError("No Arduino found\n")
if len(arduino_ports) > 1:
    print('Multiple Arduinos found - using the first\n')

# Initialize serial port
ser = serial.Serial()
ser.port = arduino_ports[0] # Arduino serial port
ser.baudrate = 250000 # Specify baudrate
ser.timeout = 10 # Specify timeout when using readline()

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


def save_BT_graph(event):
    global brake, throttle
    try:
        with lock_brake_throttle:
            with lock_angle:
                df = pd.DataFrame({'Brake Power': brake[-BTx_axis_slider.val:], 'Throttle Power': throttle[-BTx_axis_slider.val:]})
                df.to_csv('manual_save_BT_' + time.strftime('%Y-%m-%d %H-%S') + '.csv', index=False)
    except Exception as e:
        print(f"Something went wrong with saving sensor data to CSV file: {e} \n")

def save_WA_graph(event):
    global angle
    try:
        with lock_brake_throttle:
            with lock_angle:
                df = pd.DataFrame({'Wheel Angle': angle[-WAx_axis_slider.val:]})
                df.to_csv('manual_save_WA_' + time.strftime('%Y-%m-%d %H-%S') + '.csv', index=False)
    except Exception as e:
        print(f"Something went wrong with saving sensor data to CSV file: {e} \n")


def animate(i, brake, throttle, angle): # This function is called periodically from FuncAnimation
    BTstatus = BTcheck.get_status()[0]
    WAstatus = WAcheck.get_status()[0]

    with lock_brake_throttle:
        if BTstatus == True:
            brake = brake
            throttle = throttle
        else:
            brake = brake[-BTx_axis_slider.val:]
            throttle = throttle[-BTx_axis_slider.val:]

    with lock_angle:
        if WAstatus == True:
            angle = angle[-1000000:]
        else:
            angle = angle[-WAx_axis_slider.val:]

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
    
    if BTstatus == True:
            ax.axis([0, len(brake), 0, 100])
    else:
        ax.axis([0, BTx_axis_slider.val, 0, 100])
    

    # Format wheel angle plot
    ax2.set(xlabel="Time", ylabel="Angle(°)")
    ax2.legend(fontsize="x-large", loc='upper left')

    if WAstatus == True:
        ax2.axis([0, len(angle), 0, 360])
    else:
        ax2.axis([0, WAx_axis_slider.val, 0, 360])

    # Calculate the time since the program started
    elapsed_time = time.time() - start_time

    #Update time text
    time_text.set_text('Program Runtime: ' + time.strftime("%H:%M:%S.{}".format(str(elapsed_time % 1)[2:])[:11], time.gmtime(elapsed_time))) # Prints into hours, minutes and seconds

def save_data_on_close(event): # Save sensor data when window is closed
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
            ser.close() # Closes serial port
            plt.close()
            run_time = time.time() - start_time
            print("Program Exited!!")
            print('Program Runtime: ' + time.strftime("%H:%M:%S.{}".format(str(run_time % 1)[2:])[:11], time.gmtime(run_time))) # Prints into hours, minutes and seconds
        
init_x = 2000

BTx_axis = fig.add_axes([0.15, 0.4, 0.3, 0.02])
BTx_axis_slider = Slider(
    ax=BTx_axis,
    label='Time Frame',
    valmin=500,
    valmax=10000,
    valstep=500,
    valinit=init_x,
)

WAx_axis = fig.add_axes([0.6, 0.4, 0.3, 0.02])
WAx_axis_slider = Slider(
    ax=WAx_axis,
    label='Time Frame',
    valmin=500,
    valmax=10000,
    valstep=500,
    valinit=init_x,
)

label = ["Start-Current Time Frame"]

rax = fig.add_axes([0.15, 0.35, 0.13, 0.04])
BTcheck = CheckButtons(
    ax=rax,
    labels=label,
    check_props={'facecolor': 'red'},
)

cax = fig.add_axes([0.6, 0.35, 0.13, 0.04])
WAcheck = CheckButtons(
    ax=cax,
    labels=label,
    check_props={'facecolor': 'red'},
)

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

# Sets up the time textb
time_text = fig.text(.43, 0.94, '', transform=fig.transFigure, verticalalignment='bottom', fontsize=12)

# Set window title
fig.canvas.manager.set_window_title('Sensor Data')

# Format button 1
b1_axes = plt.axes([0.42,0.89,0.056,0.025]) # left,bottom, width, height
save_Current_BT = Button(b1_axes, "Save Current Graph" )
save_Current_BT.label.set_fontsize(7)
save_Current_BT.on_clicked(save_BT_graph) # Checks if button is pressed

# Format button 2
b2_axes = plt.axes([0.843,0.89, 0.056, 0.025]) # left,bottom, width, height
save_Current_WA = Button(b2_axes, "Save Current Graph" )
save_Current_WA.label.set_fontsize(7)
save_Current_WA.on_clicked(save_WA_graph) # Checks if button is pressed

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(brake, throttle, angle), cache_frame_data=False, interval=0)
plt.show()

# Waits for the thread to finish before exiting
serial_Thread.join()