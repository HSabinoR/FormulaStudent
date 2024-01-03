import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import serial
import threading
import queue
import time

# Function to read data from the serial port
def read_serial_data(serial_port, data_queue):
    while True:
        try:
            line = serial_port.readline().decode().strip()
            data_queue.put(line)
        except UnicodeDecodeError:
            pass

# Function to update the graphs
def update_graphs(start_time):
    while True:
        try:
            data = data_queue.get(timeout=1)

            # Calculate the time since the program started
            current_time = time.time() - start_time

            # Update the graphs with the new data and time
            x_data.append(current_time)
            y_data.append(float(data))

            ax1.clear()
            ax1.plot(x_data, y_data, label='Sensor Data 1')
            ax1.set_xlabel('Time (seconds)')
            ax1.set_ylabel('Sensor Data 1')
            ax1.legend()

            canvas.draw()

        except queue.Empty:
            pass
        except Exception as e:
            print(f"Error in update_graphs: {e}")

# GUI setup
root = tk.Tk()
root.title("Sensor Data Graphs")

# Serial port setup
ser = serial.Serial("COM5", baudrate=115200)

# Data queue for inter-thread communication
data_queue = queue.Queue()

# Create and start a thread to read data from the serial port
serial_thread = threading.Thread(target=read_serial_data, args=(ser, data_queue), daemon=True)
serial_thread.start()

# Create multiple graphs
fig, ax1 = plt.subplots()
x_data, y_data = [], []  # Lists to store data and corresponding time

# Create Tkinter canvas for embedding Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Get the start time
start_time = time.time()

# Schedule the update_graphs function to run every 100 milliseconds
root.after(100, update_graphs, start_time)

# Start the Tkinter main loop
root.mainloop()