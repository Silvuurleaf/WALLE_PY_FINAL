import time
class DefaultPOSDown(object):
    def __init__(self, Robot):
        # end effector down at 90 degrees
        #Robot.write(b"#0 P1530 T2000 #1 P1540 #2 P1440 #3 P750 #4 P750\r")

        Robot.write(b"#1 P1700 T2000\r")
        time.sleep(1.5)
        Robot.write(b"#2 P1400 T1500\r")
        time.sleep(1.5)

        Robot.write(b"#3 P750\r")
        Robot.write(b"#0 P1530 T1500\r")
        Robot.write(b"#4 P750\r")