import RPi.GPIO as GPIO
from values import values
from time import sleep
from octocontrol import OctoprintAPI

#L_ClickPort = 14
#rightClickPort = 15
controller = OctoprintAPI("localhost", 5000, "91DCA82B292642D58F5AB5A9CC8797A8")
controller.connect_to_printer()

stop = False
setUp = False
calibraited = False

#important printer coordinates and values:
leftX = 16
bottomY = 40
laserState = False
engraveSpeed = 220
operationalZ = 150
fastFeed = 800
slowFeed = 170
coordinates = values(leftX, bottomY, laserState, fastFeed)
#top right for both X and Y
rightCorner = 240
topCorner = 240
lowPower = 5

#gcode:
autoHome = ['G28']
setBottomLeft = ['G1 X' + str(leftX) + ' Y' + str(bottomY) + ' Z' + str(operationalZ)]
laserLowPower = ['M106 S' + str(lowPower)]
laserHighPower = ['M106']
laserOff = ['M107']
disableSteppers = ['M18']

def setXCommand():
        return ['G1 X' + str(coordinates.xPos) + " F" + str(coordinates.feedrate)]

def setYCommand():
        return ['G1 Y' + str(coordinates.yPos) + " F" + str(coordinates.feedrate)]

#messages:
welcome = "Welcome to the Etch-A-Sketch laser engraver control terminal. I will guide you through all calibration and control steps."
outOfBounds = "ERROR: OUT OF BOUNDS"
invalidCommandError = "ERROR: NOT A COMMAND, TRY AGAIN"
emergency = "Emergency noted, steppers disabled and firmware resetted"
#step one
stepOne = "Step one: home your engraver, and set to proper Z position. Please use the following checklist to determine if you are ready once firmware loads:"
checklist = """-laser is plugged in and engraver PSU.
-Medium is placed on bed in the bottom left corner.
-Workspace is clear.
-You are wearing glasses.
\nIs everything true? (Y/N)"""
rePrompt = "OK, try again:"
#step two
stepTwo = "I will now set X and Y boundaries so the laser will only stay on the medium. Refer to doccumentation to set top right corner position."
moveHead = "Enter a WASD command, STOP (in case of emergency), POSITION to view position, or DONE when laser is at the top right position:"
#step tree
stepThree = "Congrats! You are now calibraited and ready to go. Use FULL or LOW to change laser power, POSITION to view position, or STOP in case of emergency"
def reportCoordinates(x, y):
        print("Coordinates are X = " + str(x) + ", Y = " + str(y))


#Used in all steps
def sendCommand(command):
        controller.send_gcode(command)
        return("COMMAND SENT: " + str(command))

def emergencyStop():
        print(sendCommand(laserOff))
        print(sendCommand(disableSteppers))
        print(emergency)

def sendMovement(userInput):
        #example: W10

        travelDirection = userInput[0]
        #validates correct direction
        if (travelDirection != 'W' and travelDirection != 'A' and travelDirection != 'S' and travelDirection != 'D'):
                print(invalidCommandError + "\n")
                return False
        #confirms numbers are real
        travelMagnitudeString = userInput[1: ]
        try:
                float(travelMagnitudeString)
        except:
                print(invalidCommandError + "\n")
                return False
        #confirms new position is in the correct area
        travelMagnitude = abs(float(travelMagnitudeString))
        if travelDirection == "D" and coordinates.xPos + travelMagnitude <= rightCorner:
                coordinates.xPos += travelMagnitude
                print(sendCommand(setXCommand()))
        elif travelDirection == "A" and coordinates.xPos - travelMagnitude >= leftX:
                coordinates.xPos -= travelMagnitude
                print(sendCommand(setXCommand()))
        elif travelDirection == "W" and coordinates.yPos + travelMagnitude <= topCorner:
                coordinates.yPos += travelMagnitude
                print(sendCommand(setYCommand()))
        elif travelDirection == "S" and coordinates.yPos - travelMagnitude >= bottomY:
                coordinates.yPos -= travelMagnitude
                print(sendCommand(setYCommand()))
        else:
                print(outOfBounds + "\n")

#actual code here
while not stop:
        print(welcome + "\n")
        doAutoHome = False
        print(stepOne + "\n")
        if not setUp:
                sleep(10)
                setUp = True
        print(sendCommand(laserOff))
        while not doAutoHome:
                promptAutoHome = input(checklist).upper()
                if promptAutoHome == "Y":
                        doAutoHome = True
                else:
                        print("\n" + rePrompt + "\n")

        print(sendCommand(autoHome))
        print(sendCommand(setBottomLeft))
        #step two:
        print(stepTwo + "\n")
        print(sendCommand(laserLowPower))
        while not calibraited:
                userResponse = input(moveHead + "\n").upper()
                if (userResponse == "DONE"):
                        calibraited = True
                        print(sendCommand(laserOff))
                elif (userResponse == "STOP"):
                        emergencyStop()
                        calibraited = True
                        stop = True
                elif (userResponse == "POSITION"):
                        reportCoordinates(coordinates.xPos, coordinates.yPos)
                else:
                        sendMovement(userResponse)
        #step three-all ready to go!
        rightCorner = coordinates.xPos
        topCorner = coordinates.yPos
        reportCoordinates(coordinates.xPos, coordinates.yPos)
        print(stepThree)
        coordinates.feedrate = slowFeed

        R_clk = 17
        R_dt = 18

        L_clk = 22
        L_dt = 23
        L_sw = 15

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(R_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(R_dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(L_clk, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(L_dt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(L_sw, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        L_counter = 0
        L_clkLastState = GPIO.input(L_clk)
        L_SwLaserState = False
        L_SwLastState = 0

        R_counter = 0
        R_clkLastState = GPIO.input(R_clk)
        R_SwLaserState = False


        try:

                while True:
                        L_clkState = GPIO.input(L_clk)
                        L_dtState = GPIO.input(L_dt)
                        if L_clkState != L_clkLastState: #OR OTHER CLKSTATE OR SCANNER
                                if L_dtState != L_clkState:
                                        L_counter += 1
                                        sendMovement("D2")
                                else:
                                        L_counter -= 1
                                        sendMovement("A2")
                                print("LEFT" + str(L_counter))
                        L_clkLastState = L_clkState

                        #RIGHT STUFF:

                        R_clkState = GPIO.input(R_clk)
                        R_dtState = GPIO.input(R_dt)
                        if R_clkState != R_clkLastState: #OR OTHER CLKSTATE OR SCANNER
                                if R_dtState != R_clkState:
                                        R_counter += 1
                                        sendMovement("W2")
                                else:
                                        R_counter -= 1
                                        sendMovement("S2")
                                print("RIGHT" + str(R_counter))
                        R_clkLastState = R_clkState


                        #left button stuff
                        L_SwInputState = GPIO.input(L_sw)
                        if L_SwInputState == 0 and not L_SwInputState == L_SwLastState:
                            if coordinates.laserState:
                                print(sendCommand(['M106 S255']))
                                coordinates.feedrate = slowFeed
                            else:
                                print(sendCommand(['M106 S10']))
                                coordinates.feedrate = fastFeed
                            coordinates.laserState = not coordinates.laserState
                        sleep(0.0005)
                        L_SwLastState = L_SwInputState

        finally:
            GPIO.cleanup()
            sleep(0.0001)
