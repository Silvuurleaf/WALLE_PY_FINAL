import math
import numpy as np

class IK(object):
    def __init__(self, Robot,x,y,z):

        #all measurements are done from center of motors (where the joints are screwed together)

        do = 7.5        #displacement off board from motor housing (shoulder)
        L = 14.5        #length of link a1 (bicep)
        M = 18.5        #length of link a2 (forearm)
        N = 8.5725      #length of end effector (wrist)
        """
            Notes: Old values for joints
            previous M value: 19.4275
            previous N value: 5.625 Higher N distance means it gets farther away from board
        """

        #refer to link for further description of links
        #Link: https://github.com/EricGoldsmith/AL5D-BotBoarduino-PS2/blob/master/Robot_Arm_IK.pdf

        R = math.sqrt(x ** 2 + y ** 2)

        #s = R - N  NOT NEEDED BECUASE END EFFECTOR IS DEFAULTED AS BEING DOWN

        Q = math.sqrt((z - do + N) ** 2 + (R) ** 2)

        angleF = np.degrees(np.arctan2(z - do + N, R))

        angleG = np.degrees(np.arccos((L ** 2 + Q ** 2 - M ** 2) / (2 * L * Q)))

        angleA = angleF + angleG

        angleB = np.degrees(np.arccos(((M ** 2 + L ** 2 - Q ** 2) / (2 * L * M))))

        angleC = -angleB - angleA + 2 * math.pi

        #all joints +/- 90 with respect from orgin at which inverse kinematics was calulated from.
        self.theta1 = (np.degrees(np.arctan2(y, x))) - 90
        self.theta2 = (angleA) - 90
        self.theta3 = (angleB) - 90

        # end effector can't swing back fully and so has an additional offset of 19.75 degrees
        self.theta4 = (-self.theta2 - self.theta3) - 90 -19.75

        print('theta 1 is {}'.format(self.theta1))
        print('theta 2 is {}'.format(self.theta2))
        print('theta 3 is {}'.format(self.theta3))
        print('theta 4 is {}'.format(self.theta4))

    def AngleValues(self):

        return(self.theta1, self.theta2, self.theta3, self.theta4)