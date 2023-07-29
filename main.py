#!/usr/bin/env python3
import RPi.GPIO as GPIO
from time import sleep
from color_detection import *
from robotfuncs import *
import nanocamera as nano
import random
import requests
from datetime import datetime

pin_servo = 33
pin_detector = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin_servo, GPIO.OUT, initial = GPIO.HIGH)
pwm = GPIO.PWM(pin_servo, 100)
pwm.start(5)

GPIO.setup(pin_detector, GPIO.IN)

resx = 640
resy = 360
margin = resx/8
marginrg = resx/10
center = resx/2
camera = nano.Camera(flip=0, width=resx, height=resy, fps=60)
state = 0 # 0: arama 1: bardak kolda 2:bardak bırakıldı
bardak  = 0
sayac = 5
state_don = 0
while bardak < 3:
    frame = camera.read()
    img_h,img_w,_=frame.shape
    
    if state == 0:
        dets = find_black(frame)
        if dets != []:
            dists = [abs(center - det[0]) for det in dets]
            idx = dists.index(min(dists))
            center_det = dets[idx]
            
            widths = [det[3] for det in dets]
            idx = widths.index(max(widths))
            largest_det = dets[idx]
            #frame = cv2.rectangle(frame, (center_det[1], center_det[2]), (center_det[1] + center_det[2], center_det[2] + center_det[4]), (0, 0, 0), 2)
            #cv2.putText(frame, "Black Colour", (center_det[1], center_det[2]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0))

            if img_w/2-margin < center_det[0] < img_w/2+margin: # 210           
                ileri()
                if(largest_det[3] > resx*0.44):
                    sayac = 5
                    if sayac == 5:
                        dur()
                        
                        print("TUTTU", largest_det)
                        cv2.imwrite("tutuş {0}.jpg".format(datetime.now()), frame)
                        cv2.putText(frame, "Black Colour", (largest_det[1], largest_det[2]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0))
                        print("Siyah", largest_det[0], largest_det[1], largest_det[2], largest_det[3], largest_det[4])
                        
                        pwm.ChangeDutyCycle(10)
                        sleep(0.4)
                        highs = 0
                        for x in range(100):
                            val = GPIO.input(pin_detector)
                            if val == GPIO.HIGH:
                                highs = highs + 1
                        print(highs)
                        metal = highs == 100
                        if not metal:
                            requests.post('https://api.mynotifier.app', {
                            "apiKey": '95443b83-7c22-4759-93d0-bed8a32e40d5',
                            "message": "Metal Olmayan Çöp Tespit Edildi!, Yeşil Noktaya Götürülüyor.",
                            "description": "Başarılı",
                            "type": "info",  #info, error, warning or success
                            })
                            state = 1
                        else:
                            requests.post('https://api.mynotifier.app', {
                            "apiKey": '95443b83-7c22-4759-93d0-bed8a32e40d5',
                            "message": "Metal Tespit Edildi!, Kırmızı Noktaya Götürülüyor.",
                            "description": "Başarılı",
                            "type": "info",  #info, error, warning or success
                            })
                            state = 2
                        geri()
                        sleep(1)
                        
                        dur()
                        continue
            elif center_det[0] < img_w/2-margin:
                sol()
            elif center_det[0] >= img_w/2 + margin:
                sag()
        else:
            if state_don==0:
                sol()
            elif state_don==1:
                sag()
    elif state == 1:
        dets = find_green(frame)
        if dets != []:
            heights = [det[4] for det in dets]
            idx = heights.index(max(heights))
            largest_green = dets[idx]
            if img_w/2-margin < largest_green[0] < img_w/2+margin: # merkez, xb, yb, wb, hb     
                ileri()
                if(largest_green[4] > resy*0.58 and largest_green[3] > 0.39):
                    pwm.ChangeDutyCycle(5)
                    bardak = bardak + 1
                    geri()
                    sleep(1)
                    sol_arka()
                    sleep(1)
                    while False:
                        frame = camera.read()
                        dets = find_black(frame)
                        widths = [det[3] for det in dets]
                        idx = widths.index(max(widths))
                        largest_det = dets[idx]
                        if largest_det[3] < resx*0.13:
                            break
                    sol()
                    while True:
                        frame = camera.read()
                        dets = find_black(frame)
                        if dets == []:
                            break
                    state = 0
                    state_don = 0
                    continue
            elif largest_green[0] < img_w/2-margin:
                sol()
            elif largest_green[0] >= img_w/2 + margin:
                sag()
        
        else:
            sol()
    elif state == 2:
        dets = find_red(frame)
        if dets != []:
            heights = [det[4] for det in dets]
            idx = heights.index(max(heights))
            largest_red = dets[idx]
            if img_w/2-margin < largest_red[0] < img_w/2+margin: # merkez, xb, yb, wb, hb     
                ileri()
                if(largest_red[4] > resy*0.58 and largest_red[3] > 0.39):
                    pwm.ChangeDutyCycle(5)
                    bardak = bardak + 1
                    print("Birakti")
                    geri()
                    sleep(1)
                    sag_arka()
                    sleep(1)
                    while False:
                        frame = camera.read()
                        dets = find_black(frame)
                        widths = [det[3] for det in dets]
                        idx = widths.index(max(widths))
                        largest_det = dets[idx]
                        if largest_det[3] < resx*0.13:
                            break
                    sag()
                    while True:
                        frame = camera.read()
                        dets = find_black(frame)
                        if dets == []:
                            break
                    
                    state_don = 1
                    state=0
                    continue
            elif largest_red[0] < img_w/2-margin:
                sol()
            elif largest_red[0] >= img_w/2 + margin:
                sag()
        
        else:
            sag()
