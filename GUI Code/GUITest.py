import tkinter
from tkdial import *
import serial

sPort = serial.Serial('/dev/ttyACM0', 9600)

screen = tkinter.Tk()

meter = Meter(screen, start_angle=180, end_angle=-180, start=180, end=-180, fg="black", text_color="white", scale_color="red", major_divisions=180, minor_divisions=0)
meter.grid()

while True:
    try:
        data = sPort.readline().decode().strip()
        data = data.split(',')
        degrees, value2 = map(int, data)

        meter.set(degrees)
        screen.update()
    except KeyboardInterrupt:
        sPort.close()
        break