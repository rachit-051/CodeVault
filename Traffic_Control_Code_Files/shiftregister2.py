# This module adds the ability to display static and scrolling text 
# on an seven-segment display at the users' speed with a 74HC595 shift-register

#imports the required modules
import time

charLookup = {
        "0" : int("11111100",2), #1111 - on 0000 - off
        "1" : int("01100000",2),
        "2" : int("11011010",2),
        "3" : int("11110010",2),
        "4" : int("01100110",2),
        "5" : int("10110110",2),
        "6" : int("10111110",2),
        "7" : int("11100000",2),
        "8" : int("11111110",2),
        "9" : int("11110110",2),
        "A" : int("11101110",2),
        "B" : int("00111110",2),
        "C" : int("00011010",2),
        "D" : int("01111010",2),
        "E" : int("10011110",2),
        "F" : int("10001110",2),
        "G" : int("11110110",2),
        "H" : int("00101110",2),
        "I" : int("01100000",2),
        "J" : int("01110000",2),
        "K" : int("00000000",2),
        "L" : int("00011100",2),
        "M" : int("00101010",2),
        "N" : int("00101010",2),
        "O" : int("11111100",2),
        "P" : int("11001110",2),
        "Q" : int("11100110",2),
        "R" : int("00001010",2),
        "S" : int("10110110",2),
        "T" : int("00011110",2),
        "U" : int("01111100",2),
        "V" : int("00111000",2),
        "W" : int("00111000",2),
        "X" : int("00000000",2),
        "Y" : int("01110110",2),
        "Z" : int("11011010",2),
        " " : int("00000000",2),
        "." : int("00000001",2)
}   

#Writes a character to a digits
#Takes in 5 parameters (Arduino Instance, the pins of the shift register, the segments, and a pin mask), it returns nothing
def write_to_7_seg_series(myArduino, digits, pins, segCode, pinMask):

    myArduino.digital_write(pins[2],1) #OE set to HIGH
    myArduino.digital_write(pins[4],0) #SRCLR set to LOW, starts resetting shift register
    myArduino.digital_write(pins[4],1) #SRCLR set to HIGH, stops resetting shift register

    #write value into register
    for i in range(8):
        if (digits) & (int("00000001", 2) << i):
            myArduino.digital_write(pins[0],0)
        else:
            myArduino.digital_write(pins[0],1)
        #clock handling:
        #setup
        myArduino.digital_write(pins[1],1) #turns SRCLK on
        #hold
        myArduino.digital_write(pins[1],0) #turns SRCLK off

    for i in range(8):
        if (charLookup[segCode]) & (pinMask << i):
            myArduino.digital_write(pins[0],1)
        else:
            myArduino.digital_write(pins[0],0)
        #clock handling:
        #setup
        myArduino.digital_write(pins[1],1) #turns SRCLK on
        #hold
        myArduino.digital_write(pins[1],0) #turns SRCLK off

    myArduino.digital_write(pins[3],1) #turns RCLK on
    myArduino.digital_write(pins[3],0) #turns RCLK off

    #enable output
    myArduino.digital_write(pins[2],0) #OE set to LOW, turns on display
    time.sleep(1e-3)
    myArduino.digital_write(pins[2],1) #OE set to HIGH, turns off display

#This function receives a 4 character string and turns on the appropriate digit and executes the write_to_7_seg_series function
#Takes in 3 parameters (Arduino Instance, the digit pins, the pins of the shift register, and the message), it returns nothing
def write_to_4_digits_serial(myArduino, pins, message):
    digits = 0b10000000 #this holds the binary for which 7 segment display digit to turn on
    pinMask = 0b00000001 #this holds the binary to read each character code bit by bit

    #iterate and draw
    for j in range(len(message)):
        write_to_7_seg_series(myArduino, digits, pins, message[j], pinMask)
        digits = digits >> 1

#This function converts all characters to Upper case and replaces the characters "W" and "M" with
#"NN" and "VV" respectively
#Takes in 1 parameter (string to be checked), it returns the corrected message
def msg_check(message):
    message = message.upper() #change to uppcase
    message = message.replace("M","NN")
    message = message.replace("W","VV")
    return message

#This function displays a scrolling text on the seven-segment display
#Takes in 4 parameters (Arduino instance, the pins of the digits, the pins of the shift register,  
#the string to be displayed, and the speed of the scrolling text), it returns nothing
def display_scroll(myArduino, pins, message, spd):
    message = msg_check(message)

    for msgIndex in range(len(message)-3):
        dispMsg = message[msgIndex:(msgIndex+4)]
        display_static(myArduino, pins, dispMsg, spd)
    return

#This function displays a static text on the seven-segment display
#Takes in 4 parameters (Arduino instance, the pins of the digits, the pins of the shift register, 
#and the string to be displayed), it returns nothing
def display_static(myArduino, pins, message, dur):
    message = msg_check(message)
    startTime = time.time()
    while (time.time() - startTime) < dur:
        write_to_4_digits_serial(myArduino, pins, message)
        time.sleep(0.05) #delay for some reason helps with the timing of the display
    return