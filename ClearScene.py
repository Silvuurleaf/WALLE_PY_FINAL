import time
class MoveFromFrame(object):
    def __init__(self, Robot):

        #code gets the arm away from the board so an unobstructed picture can be taken

        Robot.write(b"#0 P2250 T1000\r")
        time.sleep(1)
        Robot.write(b"#1 P1643 T1000\r")
        time.sleep(1)
        Robot.write(b"#3 P2250 T1000\r")
        time.sleep(1)
        Robot.write(b"#4 P750\r")