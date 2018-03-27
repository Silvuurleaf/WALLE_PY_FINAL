import InverseKinematics
import SetAngles
import time
import DefaultPOS

class MovingObject(object):
    def __init__(self, Robot, CurrentPos, locale):
        print("grabbing and placing object")


        #closes gripper to grab box
        Robot.write(b" #4 P2250\r")
        time.sleep(1)

        Angles = InverseKinematics.IK(Robot, CurrentPos[0], CurrentPos[1], CurrentPos[2] + 8)
        SetAngles.Move(Robot=Robot, Angles=Angles.AngleValues(), time=1200)

        time.sleep(5)

        if locale == "blue":
            print("moving")
            x = 15
            y = 20
            z = 1
        elif locale == 'red':
            x = 15
            y = 15
            z = 1
        elif locale == 'green':
            x = 15
            y = 12
            z = 1
        elif locale == 'yellow':
            x =15
            y = 22
            z = 1
        else:
            print("uhmmm what?")

        # Blue Drop Off

        Angles = InverseKinematics.IK(Robot, x, y, CurrentPos[2]+8)
        # AngleList = Angles.AngleValues()
        SetAngles.Move(Robot=Robot, Angles=Angles.AngleValues(), time=1200)

        time.sleep(3)
        # let go of block

        Angles = InverseKinematics.IK(Robot, x, y, z+2)
        SetAngles.Move(Robot=Robot, Angles=Angles.AngleValues(), time=1200)
        time.sleep(3)
        Robot.write(b" #4 P750\r")

        time.sleep(1.8)

        DefaultPOS.DefaultPOSDown(Robot)