import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time


import FindBounds

class Webcam(object):
    def __init__(self):

        print("Webcam intitialized")

    def MissonApproved(self):
        print("Mission Approved Camera turning on")
        camera = cv2.VideoCapture(2)
        time.sleep(3)
        retval, frame = camera.read()

        self.image = frame

        """
        TO DO
        Add a subplot to display all OG image and proccessed images step by step

        """

        print("Running the boundary analysis. Defining Workspace as contour outlines")
        # Here the bounds of the working space and coordinates are defined
        self.BoundaryObject = FindBounds.Boundary(self.image)
        #self.ZeroZeroCoords = self.BoundaryObject.extLeft
        self.ZeroZeroCoords = self.BoundaryObject.UpperLeftMaybe


        print(" ")
        print("BACK IN WEBCAM CODE")
        print("Zero, Zero Coordinate positions")
        print(self.ZeroZeroCoords)


        print("RUNNING OBJECT ANALYSIS. Identifying color and object location")
        self.ObjectAnalysis()
        print("Object location found")
        self.YellowPages = self.OutlineDic

        n = len(self.YellowPages)
        # object positions
        x = [0] * n
        y = [0] * n

        for i in self.YellowPages:
            print(i)
            print(self.YellowPages[i])
            x[i] = self.YellowPages[i][0] - self.ZeroZeroCoords[0]
            y[i] = self.YellowPages[i][1] - self.ZeroZeroCoords[1]
        print("modified x and y coordinaetes accunting for zero position of workspace")
        print(x, y)

        """
            X,Y coordinates take into account the relative coordinate system used for our ALD5 arm. The board has a width of around 21.5cm
            and all measurements of distance in x-axis is from -10.5,10.5 where 0 on the x-axis corresponds to the center of base of the ALD5
            
            Additionally the y-coordinate system has an offset of 5cm. The base of ch1 motor is measured to be 5cm away from the board. 
            The additional +2 was correction value needed to move the arm to the intended position. This was possibly due to an error in the IK
        """
        # converting pixels to cm
        for i in range(len(x)):
            x[i] = ((x[i] / self.BoundaryObject.Px2CmWidth) - 10.25 )*-1 #Offset for robot coordinate system
            y[i] = (y[i] / self.BoundaryObject.Px2CmHeight) + 7 #changed from 6 because keeps grabbing block at edge closest to arm

        print("Image coordinates converted to cms")
        print(x, y)

        self.GOTOX = x
        self.GOTOY = y

        print("RAN THROUGH EVERYTHING WITH THE WEBCAM")


    def ObjectAnalysis(self):
        print(" ")
        print(" ")

        print("OBJECT ANALYSIS: Color being picked")
        print(" ")
        self.color = input("What color should Walle search for: ")

        print("Color selected was  " + str(self.color))
        print(" ")

        self.ColorRecog(self.color) #recognize color

        #once color recognition has been run pass the median image, created by color recognition, and the color we looked for
        self.ObjectRecog(self.median, self.color)

    def ColorRecog(self, color):
        print("color recognition")

        #image = cv2.imread("shapes_and_colors.jpg")
        image = self.image

        #creates image as hue to locate colors easier
        #HSV = hue saturateion value
        print("HUE filtering...")

        hsv =cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        """
        Run a case by case basis to see what color the user wants and proccess the image accodingly
        """
        if color == 'red':
            print("color registered as red")
            lowerBound = np.array([150,150,15])
            UpperBound = np.array([180,255,255])
        elif color == 'blue':
            print("color registered as blue")
            lowerBound = np.array([90, 50, 50])
            UpperBound = np.array([150, 255, 255])
        elif color == 'green':
            print("color registered as green")
            lowerBound = np.array([25, 50 ,20])
            UpperBound = np.array([60, 255, 160])

        elif color == 'yellow':
            lowerBound = np.array([20, 100, 100])
            UpperBound = np.array([30, 255, 255])
        else:
            lowerBound = np.array([0,0,0])
            UpperBound = np.array([255,255,255])


        # creates a mask from everything within range
        self.mask = cv2.inRange(hsv, lowerBound, UpperBound)

        #creates boolean value for mask to test if mask is within specified range or not
        result = cv2.bitwise_and(image, image, mask=self.mask)

        #take an area of 15x15 pixels from our image and averages the values (divide by 255 colors)
        self.median = cv2.medianBlur(result, 15)

        print("Original Image, masked image, and blurred image being generated")
        #display image results
        cv2.imshow("Orginal image", image)
        cv2.imshow("Masked Image", self.mask)
        cv2.imshow("blur", self.median)

        cv2.waitKey(0)

    def ObjectRecog(self, image, color):


        """
        This section deals with finding the centers of objects and outlines (contours)
        """

        #median blurred image being sent

        #THRESHOLDING FILTRATION
        print("Image proccessing being performed on median image")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # converts gray scale
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # smooths with 5x5 kernal
        ret, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        print("finding contours of block(s)")
        # th = original image, contours = contours of the image, heirarchy of the contours
        th, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        # draws Contours on original image
        # DrawContours args(image, contours array, which contour to highlight, color for outline, thickness of contour)
        cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        contoursList = contours


        CenterList = [] #empty list that will contain all the centroids of the blocks

        #Moments finds the centroid of each contour
        for i in contoursList:
            Moments = cv2.moments(i)  # moment of areas of shapes
            cx = int(Moments['m10'] / Moments['m00'])
            cy = int(Moments['m01'] / Moments['m00'])

            Center = (cx -20,cy -20)
            CenterList.append(Center)

            # draws center as circle in each image
            cv2.circle(image, (cx, cy), 7, (255, 255, 255), -1)
            cv2.putText(image, "center", (cx - 20, cy - 20),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        print("Outputting list of all the centers of objects found")
        print(CenterList)

        n = len(CenterList)
        self.OutlineDic = {}
        CenterList = list(CenterList)
        Key = list(np.arange(n)) #generating key to associate with the center coordinates

        #create a dictionary to store centers of all objects
        for i in range(len(Key)):
            self.OutlineDic[Key[i]] = CenterList[i]

        print("outputting dictionary containing all the image coordinates of objects")
        print(self.OutlineDic)

        cv2.imshow('image window', image)
        cv2.waitKey(0)

    def GridOverlay(self):

        #Code use to overlay a grid on our workspace. Was unsued in this iteration

        image = Image.open('shapes_and_colors.jpg')
        width, height = image.size
        print(height)
        print(width)

        CmHeight = 22
        CmWidth =21.5

        YCoordScale = height/CmHeight
        XCoordScale = width/CmWidth

        plt.imshow(image)
        ax = plt.gca()

        #creating the grid
        ax.grid(True, color = 'green', linestyle ='--', linewidth =2)
        #put grid below other plot elements?
        ax.set_axisbelow(True)


        #draw a box
        xy = CmWidth,CmHeight,
        w,h = XCoordScale,YCoordScale
        ax.add_patch(mpatches.Rectangle(xy, w,h, facecolor="none", edgecolor='blue', linewidth=2))

        plt.draw()
        plt.show()


camera = Webcam()
