# Dissertation-Project

![asd](https://github.com/mehmetsakiraslan/Dissertation-Project/assets/87070594/d435e700-956f-4d83-bdec-afeac3a2728a)


Jetson Nano Jetbot based garbage collecting robot designed for final project.  Robot does the following:

1- Uses OpenCV to identify and follow garbage.

2- Identifies type of the garbage by its metal detector.

3- Holds garbage and carries to selected ares determined by garbages type, also uses OpenCV to identify different type of areas.


Below, you can find the important functions and their descriptions: 


1- main.py: Controls robot movement functions and facilitates communication.

2- color_detection.py: Image processing functions to find the orange color in its original state before being pushed.

3- gpioread.py: A function used to read analog input digitally and sample it. By creating this function, we got rid of the burden of using a card (eg. Arduino) that has analog read port.

4- robotfuncs.py: Functions we wrote to ensure that one side of our robot's motor was faster than the other, to enable it to move straight.

5- colorpick.py: One of the most challenging aspects of image processing with color is the variation in color ranges due to lighting conditions. This code allows us to determine the real-time HSV color code manually by looking at the video.
