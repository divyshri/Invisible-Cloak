import cv2
import numpy as np
import time

# Creating an VideoCapture object
# This will be used for image acquisition later in the code.
cap = cv2.VideoCapture(0)

# We give some time for the camera to setup
time.sleep(3)
# count = 0
# To store the background
background=0

# Capturing and storing the static background frame
for i in range(30):
	active,background = cap.read()   #it returns two value one is boolean and another is image

#background = np.flip(background,axis=1)

while(cap.isOpened()):
	active, img = cap.read()
	if not active:
		break
	# count+=1
	# img = np.flip(img,axis=1)
	
	# Converting the color space from BGR to HSV
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	# Generating mask to detect red color for lower red
	# Considering red color hue in the range of 0-10 and saturation to be 120 and brightness to be 70
	lower_red = np.array([0,120,70])
	# Considering red color hue in the range of 0-10 and saturation to be 255 and brightness to be 255 which is max
	upper_red = np.array([10,255,255])
	mask1 = cv2.inRange(hsv,lower_red,upper_red)

	# Generating mask to detect red color for darker red
	# Considering red color hue in the range of 170-180 and saturation and brightness to be same as previous
	lower_red = np.array([170,120,70])
	upper_red = np.array([180,255,255])
	mask2 = cv2.inRange(hsv,lower_red,upper_red)

	mask1 = mask1+mask2  # + operator overloaded for or operation

	# Refining the mask corresponding to the detected red color
	mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8),iterations=2)	
	#The MORPH function removes noise from the image so that the cloak must be smooth and proper
	mask1 = cv2.dilate(mask1,np.ones((3,3),np.uint8),iterations = 1)
	#After the MORPH function is applied the dilate function adds more smoothness to the image

	#Bitwise Not with eventually invert the image as per the mask that everthing apart from the mask is removed
	mask2 = cv2.bitwise_not(mask1)


	# Generating the final output
	#Segmenting the color with the backgroud with the bitwise and
	res1 = cv2.bitwise_and(background,background,mask=mask1)
	#Segmenting the color with the cloak part
	res2 = cv2.bitwise_and(img,img,mask=mask2)

	#addWeighted is used to linearly add two images
	final_output = cv2.addWeighted(res1,1,res2,1,0)

	#Displays the ouput on the screen
	cv2.imshow('Magic !!!',final_output)

	#Terminate the program if the user presses the escape (ESC) key
	k = cv2.waitKey(1)
	if k == 27:
		break

cv2.destroyAllWindows()
	