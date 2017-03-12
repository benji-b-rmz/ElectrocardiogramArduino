#Benjamin Ramirez
#passively plotting inputs from some sensors
#using 

# Benjamin Ramirez
# 11/20/2016
# liveplotting input data from arduino using serial port

import sys
import matplotlib.pyplot as plt
import serial
import math
from datetime import datetime
from random import randint

BPM_RANGE = 50
GSR_RANGE = 500
CARDIO_RANGE = 500
DELTA_RANGE = 20

#REPLOT_RATE = 20 #higher slower, will break if too low

def main():
    #initializing the serial objects:
    print "trying to connect"
    ser = serial.Serial('/dev/tty.usbmodem1411', 115200)
    print ser.name
    bpm_file = open('BPMlog.txt', 'w')
    delta_file = open('Delta.txt', 'w')
    gsr_file = open('GSRlog.txt', 'w')
    cardio_file = open('CARDIOlog.txt', 'w')

    bpm_list = [0 for i in range(0,BPM_RANGE)]
    bpm_xaxis = [i for i in range(0,BPM_RANGE)]


    delta_list = [0 for i in range(0,DELTA_RANGE)]
    delta_xaxis = [i for i in range(0,DELTA_RANGE)]

    gsr_list = [0 for i in range(0,GSR_RANGE)]
    gsr_xaxis = [i for i in range(0, GSR_RANGE)]

    cardio_list = [0 for i in range(0,CARDIO_RANGE)]
    cardio_xaxis = [i for i in range(0, CARDIO_RANGE)]

    #iterations = 0L

    def replot():

        BPMplot.clear()
        GSRplot.clear()
        CARDIOplot.clear()

        BPMplot.plot(bpm_xaxis, bpm_list)
        GSRplot.plot(gsr_xaxis, gsr_list)
        CARDIOplot.plot(cardio_xaxis, cardio_list)

        plt.draw()
        plt.pause(0.00001)

    def process_data(data, data_list, data_file):
        try:
            data_point = data.strip()
            data_point = data_point[1:len(data_point)] #getting rid of the prefix character
            store_data(data_file, data_point)
            data_list = add_entry(data_list, data_point)
        except:
            print "bad data point processing"
            print data_point

    # setting the databuffer that will be used for plotting values
    # other points will be put into a file
    f, (BPMplot, CARDIOplot, GSRplot) = plt.subplots(3, 1, sharex=False, sharey=False)
    plt.ion()  # allows for interactive plotting "real-time"


    plt.draw()
    plt.pause(0.01)

    while True:
        # grabbing the inputs from serial port
        try:
            data = ser.readline()
            if len(data) > 0:
                print data
                #we found data, now process it
                if data[0] == 'G':
                    print "got a GSR reading"
                    process_data(data, gsr_list, gsr_file)
                    #iterations += 1

                elif data[0] == 'S':
                    print "got a CARDIO reading"
                    process_data(data, cardio_list, cardio_file)

                elif data[0] == 'B':
                    print "got a bpm reading"
                    process_data(data, bpm_list, bpm_file)
                    replot()

                elif data[0] == 'Q':
                    print "got a delta reading"
                    process_data(data, delta_list, delta_file)

            # if iterations%REPLOT_RATE == 0:
            #    replot()

        except KeyboardInterrupt:
        	#Throw a keyboard Interrupt by holding ctrl + C
            print "serial loop terminated"
            break

    ser.close()
    gsr_file.close()
    bpm_file.close()
    delta_file.close()
    cardio_file.close()

    print "done"

def add_entry(array, entry):
    for i in range(len(array) - 1):
        array[i] = array[i + 1]
    try:
        array[len(array) - 1] = int(entry)
    except:
        "bad data point"
    return array

def store_data(file_object, data):
    file_object.write(str(datetime.now()) + "\t" + str(data) + "\n")

main()
