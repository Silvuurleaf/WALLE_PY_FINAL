import time
class EnterFrame(object):
    def __init__(self, Robot):

        #code gets the arm away from the board so an unobstructed picture can be taken
        Robot.write(b"T1000 #0 P1500\r")
        time.sleep(1)
        Robot.write(b"T1000 #1 P1500\r")
        time.sleep(1)
        Robot.write(b"T1000 #3 P1500\r")
        time.sleep(1)
        Robot.write(b"#4 P750\r")