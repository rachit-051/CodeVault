# This file controls the timing for the traffic lights and their sequences based
# sensor inputs from ultrasonic and pushbutton

# importing relevent files
import time
from pymata4 import pymata4
import ultrasonic as ultra
import shiftregister2 as seg
import main_final as menu
import heartBeat

#declare arduino instance
myBoard = pymata4.Pymata4()

#declare input and output pins of traffic system
pedPin = [10, 11, 15]

trafPin = [8, 14]

buttonPin = 9

#declare pins for ultrasonic sensor
triggerPin = 13
echoPin = 12


#declare pins for shift register
SRCLR = 4 #SRCLR bar (this means not SRCLR) is the serial register clear. It can either be set as high or connected to the microcontroller. In this diagram it is connected to the microcontroller.

SRCLK = 3 #SRCLK is the shift register clock. It should be connected to the microcontroller.

RCLK = 5 #RCLK is the register clock. It should be connected to the microcontroller, possibly to the same pin as SRCLK.

OE = 6 #OE bar (this means not OE) is the output enable. It can either be set to high (always on) or connected to the microcontroller. In this diagram it is connected to the microcontroller.

SER = 2 #SER is the serial input. It should be connected to the microcontroller.

pins = [SER, SRCLK, OE, RCLK, SRCLR]

# declaring relevant variables for the reset timer
heartbeat = 16 # pin that send heartbeat to reset timer
resetPin = 3 # receiver of the output of the 556 timer
basePin = 18 # pin that determine reset timer duration by switching on/off the transistor

# set input/output pins 
myBoard.set_pin_mode_digital_output(heartbeat)
myBoard.set_pin_mode_analog_input(resetPin)
myBoard.set_pin_mode_digital_output(basePin)

for i in pedPin:
    myBoard.set_pin_mode_digital_output(i)

for i in trafPin:
    myBoard.set_pin_mode_digital_output(i)

for i in pins:
    myBoard.set_pin_mode_digital_output(i)

myBoard.set_pin_mode_digital_input_pullup(buttonPin)
myBoard.set_pin_mode_digital_input(triggerPin)
myBoard.set_pin_mode_digital_input(echoPin)

#This function controls the ped LED
#This function takes in 4 parameters (ped pins and the ped values), returns nothing
def ped_control(pedPin, r, g, f):
    myBoard.digital_pin_write(pedPin[0], r)
    myBoard.digital_pin_write(pedPin[1], g)
    myBoard.digital_pin_write(pedPin[2], f)
    return

#This function controls the LEDs of the trafic light
#This function takes in 2 parameters (traffic light pins and the color to turn on), returns nothing
def traf_light_control(trafPin, color):
    myBoard.digital_pin_write(trafPin[0], 0) #turn off all LEDs beforehand
    myBoard.digital_pin_write(trafPin[1], 0)

    if color == 'r':
        myBoard.digital_pin_write(trafPin[0], 1)
    elif color == 'y':
        myBoard.digital_pin_write(trafPin[0], 1) #yellow colour requires both red and green LED to be on
        myBoard.digital_pin_write(trafPin[1], 1)
    elif color == 'g':
        myBoard.digital_pin_write(trafPin[1], 1)
    return

#This function sets the lights to the initial state
#This function takes in nothing and returns nothing
def initial():
    print("\nInitial State")
    print("Traffic Light Red")
    traf_light_control(trafPin, 'r')
    print("Ped Light Green")
    ped_control(pedPin, 0, 1, 0)
    heartBeat.timer_duration(myBoard, basePin, menu.preset) #sets the preset for the heartbeat 556 timer
    heartBeat.start_timer(myBoard, heartbeat) #starts the heartbeat 556 timer
    return

#This function executes certain lighting sequences in the event a vehicle is detected
#This function takes in nothing and returns nothing
def vehicle_detected():

    print("Vehicle Detected")
    #Delay for 1s then keep flashing red on the pedestrian light for redPedDelay then turn red.
    seg.display_static(myBoard, pins, " GO ", 1)
    print("Ped Light Flash Red")
    ped_control(pedPin, 1, 0, 1)
    seg.display_static(myBoard, pins, "GO 3", menu.redPedDelay/3)
    seg.display_static(myBoard, pins, "GO 2", menu.redPedDelay/3)
    seg.display_static(myBoard, pins, "GO 1", menu.redPedDelay/3)
    print("Ped Light Red")
    ped_control(pedPin, 1, 0, 0)
    seg.display_static(myBoard, pins, "STOP", menu.redPedDelay)

    #Delay for 1s then Traffic light turns green.
    seg.display_static(myBoard, pins, "STOP", 1)
    print("Traffic Light Green")
    traf_light_control(trafPin, 'g')

    #Delay for greenTrafDelay then turn Traffic light yellow.
    startTime = time.time()
    while (time.time() - startTime) < menu.greenTrafDelay:
        seg.display_static(myBoard, pins, "STOP", 1)
        if myBoard.digital_read(buttonPin)[0] == 0:
            ped_detected()
            return

        print(" ") #why print empty string???

    print("Traffic Light Yellow")
    traf_light_control(trafPin, 'y')

    #Delay for 3s then turn Traffic light red.
    seg.display_static(myBoard, pins, "STOP", 3)
    traf_light_control(trafPin, 'r')
    #Delay for redTrafDelay then return to initial state.
    seg.display_static(myBoard, pins, "STOP", menu.redTrafDelay)
    #initial()
    return

#This function executes certain lighting sequences in the event a pedestrian is detected
#This function takes in nothing and returns nothing 
def ped_detected():
    if len(ultra.numOfPed) == 0: #if list is empty, create the first element in the list to start counter
        ultra.numOfPed.append(1)
        ultra.timeDetectPed.append(time.time())
    else: #if list is not empty, increment from the previous value and add it to the list
        ultra.numOfPed.append(ultra.numOfPed[-1] + 1) #adds the previous element + 1 into the list
        ultra.timeDetectPed.append(time.time()) #adds the time when the button was pressed into the list

    if len(ultra.numOfPed) > ultra.arrayLimit: #if the list is longer than the limit, remove the oldest one
        ultra.numOfPed.pop(0) #remove the oldest element
        ultra.timeDetectPed.pop(0) #remove the oldest element

    #Delay for 1s, change traffic light to yellow.
    print("Pedestrian Detected")
    seg.display_static(myBoard, pins, "STOP", 1)
    print("Traffic Light Yellow")
    traf_light_control(trafPin, 'y')

    #Delay for 3s, change traffic light to red.
    seg.display_static(myBoard, pins, "STOP", 3)
    print("Traffic Light Red")
    traf_light_control(trafPin, 'r')

    #Delay for 3s, return to initial state.
    seg.display_static(myBoard, pins, "STOP", menu.redTrafDelay)
    #initial()
    return

#This function executes certain lighting sequences in the event a no vehicle is detected for 1 minute
#This function takes in nothing and returns nothing
def no_vehicle_detected():

    print("No Vehicle Detected")
    #Flash pedestrian light red at 1-2Hz.
    print("Ped Light Flash Red")
    ped_control(pedPin, 1, 0, 1)
    seg.display_static(myBoard, pins, "GO 3", menu.redPedDelay/3) #counts down to 1 for the pedestrian to see when to stop crossing
    seg.display_static(myBoard, pins, "GO 2", menu.redPedDelay/3)
    seg.display_static(myBoard, pins, "GO 1", menu.redPedDelay/3)
    #Wait for 3s then turn the pedestrian light red.
    print("Ped Light Red")
    ped_control(pedPin, 1, 0, 0)

    #Wait for 3s then the traffic light turns green.
    seg.display_static(myBoard, pins, "STOP", menu.redPedDelay)
    print("Traffic Light Green")
    traf_light_control(trafPin, 'g')

    #Wait for 10s then turn the traffic light yellow.
    seg.display_static(myBoard, pins, "STOP", menu.greenTrafDelay)
    print("Traffic Light Yellow")
    traf_light_control(trafPin, 'y')
    
    #Wait for 3s then turn the traffic light red.
    seg.display_static(myBoard, pins, "STOP", 3)
    print("Traffic Light Red")
    traf_light_control(trafPin, 'r')
    initial()
    return

time.sleep(0.1)
while True: #checks whether signal has been sent by 556 timer each cycle, if a signal is detected then break out of while loop
    try:
        initial() #puts traffic light to initial state
        startTime = time.time() #stores startTime for time-keeping purposes for when no vehicle is detected for 1 minute
        while ultra.run_ultrasonic(myBoard, triggerPin, echoPin) == False: #reads ultrasonic sensor for vehicles, if it detects a vehicle, it breaks out of the while loop
            heartBeat.heartbeat_signal(myBoard, heartbeat) #sends heartbeat signal to 556 timer each cycle
            seg.display_static(myBoard, pins, " GO ", 0.2) #displays message to pedestrians
            if time.time() - startTime > 60: #if no vehicle is detected within 1 minute then run this sequence of lights
                no_vehicle_detected()
                startTime = time.time() #reset startTime
            if heartBeat.check_reset(myBoard, resetPin)==True:
                raise Exception("Resetting")
            pass
        vehicle_detected()
        
    except Exception:
        print("Arduino resetting")
        seg.display_scroll(myBoard, pins, "    BYE    ", 0.5) #prints scrolling message saying "BYE" to pedestrians
        myBoard.send_reset() #resets the Arduino
        myBoard.shutdown()

    except KeyboardInterrupt: #if user presses Ctrl+C, it opens the admin menu
        menu.password_security_check() #checks for user password
        pass