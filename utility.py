"""
2 functions
one for angle between 2 dots or 2 fingers
and the other for distance between them

"""

import numpy as np

#function for angle
def get_angle(a, b, c):
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    #taking difference between ab and x axis, and bc and x axis - angle between ab and bc
    angle = np.abs(np.degrees(radians))
    #converting from radians to degrees
    return angle


#function for distance
def get_distance(landmark_list):
    if len(landmark_list)<2:
        return
    
    (x1, y1), (x2, y2) = landmark_list[0], landmark_list[1] #x,y coordinates
    a = np.hypot(x2-x1, y2-y1)#finding the distance
    return np.interp(a, [0, 1], [0, 1000])#interpolation - multiplying with 1000 to convert into a value between 0 and 1000