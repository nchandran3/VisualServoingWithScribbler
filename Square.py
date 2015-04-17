'''
Simple "Square Detector" program.
Loads several images sequentially and tries to find squares in each image.
'''

import numpy as np
import cv2
import math

def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in xrange(0, 255, 26):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in xrange(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

def find_square(img):
    squares = find_squares(img)
    
    smallest = None
    sarea = 10000000
    for square in squares:
        if cv2.contourArea(square) < sarea:
            smallest = square
            sarea = cv2.contourArea(square)
    
    return smallest

def get_centroid(square):
    # GET LINES
    i = 0
    lines = []
    for i in range(len(square)-1):
        lines.append(((square[i][0], square[i][1]), (square[i+1][0], square[i+1][1])))
    lines.append(((square[0][0], square[0][1]),(square[len(square)-1][0], square[len(square)-1][1])))

    #print lines

    # GET CENTROID LINE
    midpoints = []
    for line in lines:
        midpoints.append(( (line[0][0]+line[1][0])/2, (line[0][1]+line[1][1])/2 ))

    #find comparable x coords in midpoints
    threshold = 8
    centroid = None
    for mid1 in midpoints:
        for mid2 in midpoints:
                if mid1 != mid2 and np.abs(mid1[0] - mid2[0]) < threshold:
                    centroid = (mid1, mid2)
                    break

    return centroid

def get_axis(img):
    squares = find_squares(img)

    smallest = None
    sarea = 10000000
    for square in squares:
        if cv2.contourArea(square) < sarea:
            smallest = square
            sarea = cv2.contourArea(square)

    line = get_centroid(square)
    line = [np.asarray(line)]

    squares = [square]
    cv2.drawContours( img, squares, -1, (0, 255, 0), 1 )
    cv2.drawContours( img, line, -1, (255, 0, 0), 1 )
    cv2.imshow('squares', img)
    ch = 0xFF & cv2.waitKey()

    cv2.destroyAllWindows()
    return line[0]


def axis_length(axis):
    x1, y1 = axis[0]
    x2, y2 = axis[1]
    
    return ((x2-x1)**2 + (y2-y1)**2)**.5
    
def get_ratio_LR(square):
    pass

"""
Returns 1 if you should move forward (end axis is larger than start axis), -1 if you should move backwards (end axis is smaller than start axis)
or 0 if you are within the acceptable threshold.
"""
def compare_axes(startimg, endimg, threshold):
    axis_start = get_axis(startimg)
    axis_end = get_axis(endimg)
    
    axis_start_len = axis_length(axis_start)
    axis_end_len = axis_length(axis_end)
    
    result = axis_end_len - axis_start_len
    
    if abs(result) < threshold:
        return 0
    elif result > threshold: 
        return 1
    else:
        return -1
