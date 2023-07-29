#!/usr/bin/env python3
import cv2
import numpy as np
from time import sleep
from datetime import datetime

resx = 640
resy = 360
red_lower = np.array([0, 115, 111], np.uint8)
red_upper = np.array([179, 193, 175], np.uint8)
  
green_lower = np.array([0, 111, 56], np.uint8)
green_upper = np.array([95, 255, 108], np.uint8)

black_lower = np.array([0, 0, 28], np.uint8)
black_upper = np.array([179, 80, 72], np.uint8)

kernel = np.ones((15, 15), "uint8")
kernelr = np.ones((5, 5), "uint8")

def find_black(frame):
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    black_mask = cv2.inRange(hsvFrame, black_lower, black_upper) 
    #black_mask = cv2.dilate(black_mask, kernel)
    black_mask = cv2.morphologyEx(black_mask, cv2.MORPH_OPEN, kernel)
    res_black = cv2.bitwise_and(frame, frame, mask = black_mask)
    contours, hierarchy = cv2.findContours(black_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    dets = []
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 350):
            xb, yb, wb, hb = cv2.boundingRect(contour)
            if (((xb >resx/5 and xb + wb < resx - resx/5) or (wb>resx*0.3))):
                dets.append([xb + wb/2, xb, yb, wb, hb])
    return dets
    
def find_red(frame):
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)
    #red_mask = cv2.dilate(red_mask, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernelr)
    res_red = cv2.bitwise_and(frame, frame, mask = red_mask)
    contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    dets = []
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1200):
            xr, yr, wr, hr = cv2.boundingRect(contour)
            if (xr >resx/6 and xr + wr < resx - resx/6 and yr < 60):
                dets.append([xr + wr/2, xr, yr, wr, hr])
    return dets

def find_green(frame):
    hsvFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)
    #green_mask = cv2.dilate(green_mask, kernel)
    green_mask = cv2.morphologyEx(green_mask, cv2.MORPH_OPEN, kernelr)
    res_green = cv2.bitwise_and(frame, frame, mask = green_mask)
    contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    dets = []
    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if(area > 1200):
            xg, yg, wg, hg = cv2.boundingRect(contour)
            if (xg >resx/6 and xg + wg < resx - resx/6 and yg < 60):
                dets.append([xg + wg/2, xg, yg, wg, hg])
    return dets
            
