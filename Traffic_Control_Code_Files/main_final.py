# Tests the functionality of a console menu, allowing the user to change parameters, view graphs, and has a login feature

#import required modules
import time
import ultrasonic as ultra

#timeout for the menu
timeoutLimit = 20

# This function checks if there has been an admin access timeout 
# This function is called after every input request to check for timeout
# The function doesn't take any parameter and returns nothing
def timeout_check():
    
    global startTime    #using the global variable

    #if the current time exceeds the set timeout limit, user is locked. Otherwise, startTime is reset.
    if (time.time() - startTime) > timeoutLimit:
        print ("\nError! User timed out.")
        print ("User Locked.\n")
        exit ()
        
    else:
        startTime = time.time()

# This function verifies admin through entered password
# The function doesn't take any parameter and returns nothing
def password_security_check():
    
    #stored password
    storedPin = "pwd123"

    #counter to check number of failed attempts
    counter = 0

    #loop to request for the password until correct password is entered
    while True:
       
        #resetting global current time variable
        global startTime
        startTime = time.time()

        inputPin = input("\nPlease enter the passcode: ")
        timeout_check()
        
        #checking if input pin is the same as stored pin
        if inputPin == storedPin:
            print ("\nSuccess!\nWelcome Admin!")
            parameter_list()
            break
        
        else:
            counter += 1    #incrementing counter by one after every failed attempt
            print (f"\nIncorrect pin. Please try again. {3-counter} attempt(s) left")
        
            #if 3 failed attempts at getting the right password have been made, the user does not respond for 2 minutes
            if counter == 3:
                print ("\nUser locked! No more attempts allowed for 2 minutes")
                time.sleep(120)
                counter = 0


#pre-defined values of all parameters:
redTrafDelay = 3       #red traf light delay
greenTrafDelay = 10    #green traf light delay
redPedDelay = 3        #red ped light delay
greenPedDelay = 10     #green ped light delay
threshold = 15         #minimum threshold detection distance from ultrasonic sensor
preset = 2             #declare the heartbeat 555 timer timing preset toggle for the heartbeat signal

# function to provide the list of all parameters to the admin upon successful verification
# takes in no parameters and returns nothing
def parameter_list():
    
    global redTrafDelay
    global greenTrafDelay
    global redPedDelay
    global greenPedDelay
    global threshold
    global preset
    
    #loop to gain input from the admin to view/change the parameter chosen 
    while True:
        
        #printing the list of all parameters
        print (f"\nList of Parameters:\n\n  1. Red Traffic Light Delay: {redTrafDelay} s\n  2. Green Traffic Light Delay: {greenTrafDelay} s\n  3. Red Pedestrian Light Delay: {redPedDelay} s\n  4. Green Pedestrian Light Delay: {greenPedDelay} s\n  5. Vehicle Threshold Distance: {threshold} cm\n  6. Heartbeat Signal Timout: Preset no. {preset} \n  7. Graphing Menu\n  0. Exit Console\n")
        
        #resetting global current time variable
        global startTime
        startTime = time.time ()

        #requesting user input
        userEdit = input ("Please enter the list number of the parameter you wish to edit: ")
        timeout_check()
       
        #checking if user input is within the range of paramater list i.e. 0-6
        if (int(userEdit) < 0 or int(userEdit) > 6):
            print("Error! Please enter a number between 0-6")
       
        try: 
            if int(userEdit) == 1:
                print (f"\nCurrent value of Red Traffic Light Delay: {redTrafDelay} s")
                redTrafDelay = int (input("Please enter the new value of Red Traffic Light Delay: "))
                print (f"\nNew value of Red Traffic Light Delay: {redTrafDelay} s")
                time.sleep(0.5)
        
            elif int(userEdit) == 2:
                print (f"\nCurrent value of Green Traffic Light Delay: {greenTrafDelay} s")
                greenTrafDelay = int (input("Please enter the new value of Green Traffic Light Delay: "))
                print (f"\nNew value of Green Traffic Light Delay: {greenTrafDelay} s")
                time.sleep(0.5)
                    
            elif int(userEdit) == 3:
                print (f"\nCurrent value of Red Traffic Pedestrian Light Delay: {redPedDelay} s")
                redPedDelay = int (input("Please enter the new value of Red Pedestrian Light Delay: "))
                print (f"\nNew value of Red Traffic Pedestrian Light Delay: {redPedDelay} s")
                time.sleep(0.5)
                                
            elif int(userEdit) == 4:
                print (f"\nCurrent value of Green Traffic Pedestrian Light Delay: {greenPedDelay} s")
                greenPedDelay = int (input("Please enter the new value of Green Pedestrian Light Delay: "))
                print (f"\nNew value of Green Traffic Pedestrian Light Delay: {greenPedDelay} s")
                time.sleep(0.5)

            elif int(userEdit) == 5:
                print (f"\nVehicle Threshold Distance: {threshold} cm")
                threshold = int (input("Please enter the new value of Vehicle Threshold Distance: "))
                print (f"\nNew value of Vehicle Threshold Distance: {threshold} cm")
                time.sleep(0.5)

            elif int(userEdit) == 6:
                if preset == 1:
                    print (f"\nCurrent Timing is 55s")
                elif preset == 2:
                    print (f"\nCurrent Timing is 45s")
                preset = int (input("Please choose a preset, enter 1 for 55s and 2 for 45s: "))
                print (f"\nNew preset for heartbeat timeout is: Preset no. {preset}")
                time.sleep(0.5)

            elif int(userEdit) == 7:
                print (f"\n\nGRAPING MENU: \n")
                graphing_menu_selector() #function to display appropriate graph types
            
            elif int(userEdit) == 0:
                print ("\nThank you! User Locked.")
                return
                #exit()
            else:
                print ("Please enter a number from 0-6") 

        except ValueError:
            userEdit = input ("Incorrect input. Please try again: ")
        

# This function requests for user input to check if any addtional paramters are to be edited
# The function doesn't take any parameter and returns the user input string of "YES" or "NO"
def additional_input_requests():
    
    #resetting global current time variable
    global startTime
    startTime = time.time()

    additionalValueChange = input("\nWould you like to edit any other parameter? YES/NO: ")
    timeout_check()    

    #checking the type of input obtained from user
    if additionalValueChange == "NO" or additionalValueChange == "YES":
        return additionalValueChange

    #looping is performed until correct input is obtained from user
    while (additionalValueChange != "YES" and additionalValueChange != "NO"):
        
        additionalValueChange = input("Unsupported input! \nWould you like to edit any other parameter? YES/NO: ")
        timeout_check()

        if additionalValueChange == "NO" or additionalValueChange == "YES":
            return additionalValueChange


# This function displays appropriate graph types based on user's choice (input)
# The function doesn't take any parameter and returns nothing
def graphing_menu_selector():

    #listing down all the possible types of graphs 
    print("Which of the following graphs would you like to see?\n")
    print ("  1. Number of Vehicle from Traffic Light vs Time\n  2. Number of Pushbutton Signals vs Time\n")

    #resetting global current time variable
    global startTime
    startTime = time.time()

    #requesting type of graph to be plotted from user
    graphSelector = input ("Please enter the list number of the graph you would like to view: ")

    while True: 
        try:
            if int(graphSelector) == 1:
                print ("\nNumber of Vehicle from Traffic Light vs Time graph plotted for the last 1 minute")
                print ("Please close the graph before proceeding")

                ultra.graph_vehicle() #graph for number of vehicle detected in the last 1 minute will be plotted
                break

            elif int(graphSelector) == 2:
                print ("\nNumber of Pushbutton Signals vs Time graph plotted for the last 1 minute")
                print ("Please close the graph before proceeding")

                ultra.graph_ped() #graphs the number of pedestrian button presses in the last minute
                break

        except ValueError:
            graphSelector = input ("Incorrect input. Please try again: ")     


#password_security_check()
