import math
import numpy as np
import cv2
import time

class Boundary(object):
    def __init__(self, image):
        print("Finding boundary...")

        self.frame = image      #frame is image taken from the webcam
        self.DefineBounds()     #Will find the boundaries of workspace and coordinate conversions from pixels to cm


    def DefineBounds(self):

        """
            Gist: The webcam picture is blurred and converted to gray scale. Once this is done it should be easier to identify
            our working space which was a piece of white paper with a blackoutline so the OpenCV could readily identify and create a contour
            around the work area. 
            
            Once we have our workspace we find the top left most point in our contour. This will serve as our zero, zero coordinate all objects
            will be measured relative to this position. 
            
            Since we know that the paper's actual diemensions we can find the corresponding image length(pixels) of our contour and get
            a conversion value between pixels and cms for our image. This once we have a distance from an object in pixel from our image we
            can find a equivalent distance in CMs.
        """

        # convert the image to grayscale, blur it, and detect edges

        print("Creating grayscale image...Blurring image")
        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(gray, 35, 125)

        # find the contours in the edged image and keep the largest one (The largest contour will be our piece of paper)
        th, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        c = max(contours, key=cv2.contourArea)
        print("Contours have been found")

        # compute the bounding box of the of the paper region and return it
        print("Drawing Contour")
        cv2.drawContours(self.frame, c, -1, (0, 0, 0), 3)
        cv2.imshow("B and W", edged)
        cv2.imshow("capture", self.frame)
        cv2.waitKey(0)

        # minAreaRect returns (center (x,y), (width, height), angle of rotation )

        """
            Error occured where the length and height values would flip flop in the indexes of cv2.minAreaRect
            this would throw off the unit conversion because the paper has a different length and height.
            
            Check: the pixel conversions should be close to each other for length and height.
        """

        BboxWidth = cv2.minAreaRect(c)[1][0]    #should grabt the length of the contour
        BboxHeight = cv2.minAreaRect(c)[1][1]   #should grabt the height of the contour

        print("BOUNDING BOX WIDTH IS {}".format(BboxWidth))
        print("BOUNDING BOX HEIGHT IS {}".format(BboxHeight))

        self.Px2CmWidth = BboxWidth / 21.5 # 1cm = x many pixels     #21.5cm wide
        self.Px2CmHeight = BboxHeight / 18  # 1cm = x many pixels   #18 cm long

        print("CHECKING WIDTH AND HEIGHT CONVERSIONS")
        print(BboxWidth, BboxHeight)
        print("Conversion values Px2Cm width {}, Px2Cm height {}".format(self.Px2CmWidth, self.Px2CmHeight))

        #Round the conversion values up and if they don't match that means that minAreaRect command flipped the length with height
        #so the conversions are run again dividing by the appropriate amount.
        if math.ceil(self.Px2CmWidth) != math.ceil(self.Px2CmHeight):
            print("Rounding occuring")
            self.Px2CmWidth = (cv2.minAreaRect(c)[1][1])/21.5
            self.Px2CmHeight = (cv2.minAreaRect(c)[1][0])/18
        else:
            pass

        print(" ")
        print("final conversions")
        print("Bbox diemensions {}  x  {}".format(BboxWidth, BboxHeight))
        print("Conversion values Px2Cm width {}, Px2Cm height {}".format(self.Px2CmWidth, self.Px2CmHeight))

        #Finding the top and left most coordinate

        self.extLeft = tuple(c[c[:, :, 0].argmin()][0]) #Most left coordinate position
        self.topmost = tuple(c[c[:, :, 1].argmin()][0]) #Top most coordinate position

        #Other coordinates used to analyze contour. They were unused for this project.
        self.extTop = tuple(c[c[:, :, 1].argmin()][0])
        self.extRight = tuple(c[c[:, :, 1].argmax()][0])
        self.extBottom = tuple(c[c[:, :, 1].argmax()][0])

        self.UpperLeftMaybe = (self.extLeft[0], self.topmost[1])
        print("Top left coordinate")
        print(self.UpperLeftMaybe)
        print(self.extLeft[0], self.topmost[1])

        #draws white boxes to show the top and left most coordinate in contours list
        cv2.rectangle(self.frame, (self.extLeft), (self.extLeft[0]+10, self.extLeft[1]+10), (255, 255, 255), 2)
        cv2.rectangle(self.frame, (self.topmost), (self.topmost[0] + 10, self.topmost[1] + 10), (255, 255, 255), 2)


        #cv2.rectangle(self.frame, (self.extRight), (self.extRight[0], self.extRight[1]+100), (255, 255, 0), 2)

        print("Black Box represents 0,0 coordinate")
        cv2.rectangle(self.frame, (self.UpperLeftMaybe), (self.UpperLeftMaybe[0] - 10, self.UpperLeftMaybe[1] - 10), (0, 0, 0), 2)

        cv2.imshow("BOX",self.frame)
        cv2.waitKey(0)

