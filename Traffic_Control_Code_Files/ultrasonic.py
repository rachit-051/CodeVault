# This file contains the functions to read from the ultrasonic sensor 
# and return whether a vehicle is detected


# importing relevent files
import time
import matplotlib.pyplot as plt
import main_final as menu

#declare variables to store vehicle detections
value = [] #stores the distance from ultrasonic sensor (US)
carDetection = [] #stores whether a car was detected
numOfCars = [] #stores the number of cars detected
timeDetect = [] #stores the timestamps for the US readings
distance = [] #stores the distance from US
arrayLimit = 100 #limit of number of data points stored in the array

#declare variables to store button presses
numOfPed = []
timeDetectPed = []

#Callback function is called when an ultrasonic reading is done
#This function takes 1 parameter (data of ultrasonic reading) and returns nothing
def callback(data):
    currDistance = data[2]
    value.append(currDistance)
    while len(value) == 0: #if no reading was made, keep waiting until a reading is made
        pass

#This function stores the reading of the ultrasound into a list
#This function takes no parameters and returns nothing
def store_distance():
    distance.append(value[-1]) #appends to the end of the list
    while len(distance) > arrayLimit: #if list is too long, remove the oldest data
        distance.pop(0)

#This function stores whether or not a vehicle was detected at the time of reading into a list
#This function takes no parameters and returns nothing
def store_detection():
    if (value[-1] <= menu.threshold): #if distance to vehicle is less than threshold, add 1 to the list and increment vehicle counter
        carDetection.append(1)

        if len(numOfCars) == 0:
            numOfCars.append(1) #if the list is empty, add it as the initial value of the list
        else:    
            numOfCars.append(numOfCars[-1]+1) #if the list isn't empty, increment the latest value by one and append to the list

        timeDetect.append(time.time())

        if len(carDetection) > arrayLimit: #if list is too long, remove the oldest data
            carDetection.pop(0)
            numOfCars.pop(0)
            timeDetect.pop(0)

    elif (value[-1] > menu.threshold): #if distance of vehicle is greater than threshold, add 0 to the list, do nothing to vehicle counter
        carDetection.append(0)

        if len(numOfCars) == 0:
            numOfCars.append(0) #if the list is empty, add it as the initial value of the list
        else:    
            numOfCars.append(numOfCars[-1]) #if the list isn't empty, copy the latest value and append to the list

        timeDetect.append(time.time())

        if len(carDetection) > arrayLimit: #if list is too long, remove the oldest data
            carDetection.pop(0)
            numOfCars.pop(0)
            timeDetect.pop(0)

#This function is to get the ultrasonic sensor to read the distance
#This function takes 3 parameter (Arduino instance, trigger pin, and echo pin) and returns nothing
def sonar_setup(myBoard, triggerPin, echoPin):
    myBoard.set_pin_mode_sonar(triggerPin,echoPin,callback,timeout=200000)

#This function executes tthe sensor reading, storing and checking for vehicles
#This function takes in 3 parameters (Arduino instance, the trigger pin and echo pin of the sensor), it returns True or False depending on vehicle detection
def run_ultrasonic(myBoard, triggerPin, echoPin):
    sonar_setup(myBoard, triggerPin, echoPin)
    time.sleep(1)
    if len(value) == 0:
        return False

    store_distance()
    store_detection()

    if carDetection[-1] == 1: #if vehicle was detected in the most recent reading, return True
        return True
    elif carDetection[-1] == 0:  #if vehicle was not detected in the most recent reading, return False
        return False
        
#Graphs the number of vehicles since the last minute
#This function takes no parameters and returns nothing
def graph_vehicle():
    if len(numOfCars) == 0:
        print("No enough data collected")
        return

    i = len(timeDetect)-1 #checks from the end of the list until there's at least one minute's worth of data

    while timeDetect[-1] - timeDetect[i] < 60: #checks 
        if i == 0:
            break

        i -= 1 #move the index to the left by one element

    graphDataX = [timeDetect[index] for index in range(i, len(timeDetect))] #places the data to be plotted
    graphDataY = [numOfCars[index] for index in range(i, len(timeDetect))]
    
    for i in range(1,len(graphDataX)): #format the time to be starting from 0 instead of the program start time
        graphDataX[i] = graphDataX[i] - graphDataX[0]
    graphDataX[0] = 0

    plt.xlabel("Time in seconds (s)")
    plt.ylabel("Number of vehicles")
    plt.title("NUmber of vehicle VS Time")
    plt.plot(graphDataX, graphDataY, marker='o')
    plt.savefig("number_of_cars.png")
    plt.show()
    
#Graphs the number of pedestrian button presses since the last minute
#This function takes no parameters and returns nothing
def graph_ped():
    if len(numOfPed) == 0:
        print("No enough data collected")
        return

    i = len(timeDetectPed)-1

    while timeDetectPed[-1] - timeDetectPed[i] < 60:
        if i == 0:
            break

        i -= 1 #checks from the end of the list until there's at least one minute's worth of data

    graphDataX = [timeDetectPed[index] for index in range(i, len(timeDetectPed))] #places the data to be plotted
    graphDataY = [numOfPed[index] for index in range(i, len(timeDetectPed))]
    
    for i in range(1,len(graphDataX)): #format the time to be starting from 0 instead of the program start time
        graphDataX[i] = graphDataX[i] - graphDataX[0]
    graphDataX[0] = 0

    plt.xlabel("Time in seconds (s)")
    plt.ylabel("Number of pedestrians")
    plt.title("Number of Pedestrians VS Time")
    plt.plot(graphDataX, graphDataY, marker='o')
    plt.savefig("number_of_peds.png")
    plt.show()