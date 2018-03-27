#inherent code files
import time
import serial

#Code to control arm movement
import ClearScene
import DefaultPOS
import InverseKinematics
import SetAngles
import GrabAndDrag

#Computer Vision Port
import Webcam

#Old Code Files not used
import SetAngles_V2
import IK_V3
import EnterScene


class robot(object):
    def __init__(self):

        # configure the serial connections (the parameters differs on the device you are connecting to)
        self.WALLE = serial.Serial(
            port='com4',
            baudrate=115200,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        print("Initialize empty list that will store angle values")
        self.AngleList = [0]*4

        self.Time = 2000 #default time for allmovement is 2 seconds


        self.Commands() #instructions to run arm

        """
        Code Appendix
        
            self.WALLE.write(b'hello')  # write a string in binary to arm
            self.WALLE.close()          # close port
        
        """

    def Commands(self):
        print("CLEARING AREA. PREPARING FOR PHOTOSHOOT")

        ClearScene.MoveFromFrame(self.WALLE) #moves arm out of the way so webcam can snap a picture
        time.sleep(2)

        CameraMan = Webcam.Webcam() #create object CameraMan  that accesses and uses webcam
        CameraMan.MissonApproved()  #gives the go ahead to run computer vision image proccessing

        x = CameraMan.GOTOX #list of x-values for located objects
        y = CameraMan.GOTOY #list of y-values for located objects

        color = CameraMan.color #color value user wanted to look for


        print("Beginning movement... Running Inverse Kinematics")

        for i in range(len(x)): #counter runs through all coordinates provided

            DefaultPOS.DefaultPOSDown(self.WALLE) #moves arm to a set default positon
            time.sleep(3.5)

            print("Moving to coordinates ({}, {})".format(x[i],y[i]))

            self.Angles = InverseKinematics.IK(self.WALLE, x[i],y[i],5) #z-distance is provided so arm hovers above the block
            self.AngleList = self.Angles.AngleValues()

            print("LIST OF ANGLE VALUES AFTER INVERSE KINEMATICS..........{}".format(self.AngleList))

            # Once angles are calculated they are forwarded to arm and are converted to P values for each motor
            SetAngles.Move(Robot=self.WALLE, Angles=self.AngleList, time=2000)

            time.sleep(4)

            # z-value of zero drops the arm down to grab the block
            self.Angles =InverseKinematics.IK(self.WALLE, x[i],y[i],0)
            self.AngleList = self.Angles.AngleValues()
            SetAngles.Move(Robot=self.WALLE, Angles=self.AngleList, time=2000)

            time.sleep(3)
            currentPos = (x[i],y[i],0) #passes current location of arm

            # GrabAndDrag will pick up the object, check its color, and dump it at a corresponding locale
            GrabAndDrag.MovingObject(self.WALLE, currentPos, locale=color)

        self.WALLE.close()

Startup = robot()










