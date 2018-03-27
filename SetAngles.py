
class Move(object):
    def __init__(self, Robot, Angles, time):

        #Runs through list of angles and sends information as bytes via serial connection to move arm
        #Offset position - degree/pvalue conversion for motor
        ch0 = (1500 - 10.72 * Angles[0])
        ch1 = (1480 + 8.33 * Angles[1])
        ch2 = (1470 - 8.33 * Angles[2])
        ch3 = (1500 + 8.96296 * Angles[3])


        out = ("#0 P{} T{} #1 P{} T{} #2 P{} #3 P{}\r".format(ch0, time, ch1, time, ch2, ch3))

        Robot.write(bytes(out, 'utf8')) #utf8 encodes string so it can be read by serial connection


        """
            #PAST SETTINGS (Iteratively solved for ideal positions)
            
            Most Recent changes
            #CH0: #was 14550 -> 1500 -> 1570 works well idk wth is wrong with this thing
                    #1570 and 1540 work back and forth
                    
            #CH1:#was 1450
            #CH2: #1440
            #Ch3: #was 1550
            
            #ch0 = (1570 - 10.72 * Angles[0])
            #ch1 = (1450 + 8.33 * Angles[1]) #was 1450
            #ch2 = (1500 - 9.2 * Angles[2]) #1450 8.33
            #ch3 = (1550 + 7 * Angles[3]) #was 1550 8.9629

            # 8.21 #1470
            # 8.18
            # ch0 1530, 1540,1440, 1500

            # current settings that work well 1500, 1500, 1440, 1500
            # MORE current settings 1540, 1470, 1440, 1500, N =5.625
        """
