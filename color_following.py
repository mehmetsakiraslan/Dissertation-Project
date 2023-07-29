#!/usr/bin/env python3
import cv2
import numpy as np
from time import sleep
import nanocamera as nano
# Set range for red color and 
# define mask
red_lower = np.array([0, 115, 111], np.uint8)
red_upper = np.array([179, 193, 255], np.uint8)
  
green_lower = np.array([0, 111, 56], np.uint8)
green_upper = np.array([95, 255, 108], np.uint8)

black_lower = np.array([0, 0, 28], np.uint8)
black_upper = np.array([179, 80, 72], np.uint8)
            
kernel = np.ones((15, 15), "uint8")
kernelr = np.ones((5, 5), "uint8")

resx = 640
resy = 360

state = 0;

if __name__ == '__main__':
    # Create the camera instance
    camera = nano.Camera(flip=0, width=resx, height=resy, fps=60)
    sleep(0.3)
    while 1:
        
        try:
            frame = camera.read()
            #cv2.imshow("Video Frame", frame)
            # hsv conversion
            
            hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
            #red_mask = cv2.dilate(red_mask, kernel)
            red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernelr)
            res_red = cv2.bitwise_and(frame, frame, mask = red_mask)   
                     
            green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
            #green_mask = cv2.dilate(green_mask, kernel)
            green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernelr)
            res_green = cv2.bitwise_and(frame, frame, mask = green_mask)

            
            black_mask = cv2.inRange(hsvFrame, black_lower, black_upper)
            #black_mask = cv2.dilate(black_mask, kernel)
            black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel)
            res_black = cv2.bitwise_and(frame, frame, mask = black_mask)



            
            xr = 0; 
            xg = 0; 
            xb = 0;
            
            contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            # Creating contour to track red color
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 1200):
                    xr, yr, wr, hr = cv2.boundingRect(contour)
                    if (xr > resx/6 and xr + wr < resx - resx/6 and yr < 30):
                        frame = cv2.rectangle(frame, (xr, yr), (xr + wr, yr + hr), (0, 0, 255), 2)
                        print("Kırmızı", xr + wr/2, xr, yr, wr, hr)
                        cv2.putText(frame, "Red Colour", (xr, yr), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255))
                    
            # Creating contour to track green color
            contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 1200):
                    xg, yg, wg, hg = cv2.boundingRect(contour)
                    
                    if (xg > resx/6 and xg + wg < resx - resx/6 and yg < 30):
                        frame = cv2.rectangle(frame, (xg, yg), (xg + wg, yg + hg), (0, 255, 0), 2)
                        cv2.putText(frame, "Green Colour", (xg, yg), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0))
                        print("Yesil", xg + wg/2, xg, yg, wg, hg)
             # Creating contour to track green color
            contours, hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            xb = yb = wb = hb = 0
            for pic, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                if(area > 350):
                    xb, yb, wb, hb = cv2.boundingRect(contour)
                    if (((xb >resx/5 and xb + wb < resx - resx/5) or (wb>resx*0.3))):    
                        frame = cv2.rectangle(frame, (xb, yb), (xb + wb, yb + hb), (0, 0, 0), 2)
                  
                        cv2.putText(frame, "Black Colour", (xb, yb), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0))
                        print("Siyah", xb + wb/2, xb, yb, wb, hb)
            cv2.imshow("Multiple Color Detection in Real-TIme", frame)
            
            #print("Red area cordinates: {:.2f}" .format(xr-360))
            #print("Green area cordinates: {:.2f}" .format(xg-360))
            #print("Black area cordinates: {:.2f}" .format(xb-360))
            #mask = cv2.inRange(frame, lower_red, upper_red)
            #detected_output = cv2.bitwise_and(frame, frame, mask =  mask)
            #cv2.imshow("red color detection", detected_output) 
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        except KeyboardInterrupt:
            break
            
    camera.release()
    
    
