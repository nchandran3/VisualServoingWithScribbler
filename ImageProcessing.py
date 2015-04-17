"""
Used for testing image processing functionality for the ScribblerIBVO Class
@author Naveen Chandran
"""
from PIL import Image
import cv2
import numpy as np
from cv2 import drawContours

class ImageProcessing():
    
    @staticmethod
    def getBlackBox(img):
        pass
    
    """
    **METHOD NOT USED** Because most stuff is happening with CV2
    Converts and image to black and white (not grayscale) from a color image.
    @param img: A PIL Image object
    @return    An image object representing the color picture in black and white
    """
    @staticmethod
    def imgToBlackAndWhite(img):
        gray_img = img.convert('L')
        bw_img = gray_img.point(lambda x: 1 if x>50 else 0, '1')
        return bw_img



    """
    Crops the image the specified percent from the left, right, top, and bottom
    @param img:    The PIL image object
    @param percent:     (double) The percent to crop from all sides from 0 - 0.5
    @param cv2:         True if using cv2 image manipulation, False if using PIL 
    """
    @staticmethod
    def cropFromSides(img, percent, cv2 = True):
        if cv2:
            height, width = img.shape[:2]
            left, upper, right, bottom = (int(width*percent), int(height*percent), int(width*(1-percent)), int(height*(1-percent)))
            return img[upper:bottom, left:right] 
            
        else:
            width, height = img.size
            left, upper, right, bottom = (int(width*percent), int(height*percent), int(width*(1-percent)), int(height*(1-percent)))
            return img.crop((left,upper,right,bottom))
            
    

def main(args):
    #set args values here
    img_path = args[0]
    
    """
    Begin debugging code here
    """
    
    img_raw = cv2.imread(img_path)
    img = ImageProcessing.cropFromSides(img_raw, .15)   #crop out unnecessary space
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)     #convert to grayscale
    ret,thresh = cv2.threshold(img_gray,30,255,0)       #convert to binary (black and white)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #find contours
    cv2.drawContours(img,contours,-1,(0,255,0),1)   #draw contours on cropped image
    
    cv2.imshow("Contours",img_raw)      #display contours on normal image
    cv2.waitKey()
    
    epsilon = 0.1*cv2.arcLength(contours, True)
    img2 = img.clone()
    
    for cnt in contours:
        approx = cv2.approxPolyDP(contours, epsilon, True)
        if len(approx == 4):
            break
        
    cv2.drawContours(img2, approx, -1, (0,255,0), 1)
    cv2.imshow("Approximates", img2)
    cv2.waitKey()
    
        
if __name__ == "__main__":
    import sys
    import Square
    img_path1 = sys.argv[1]
    img_path2 = sys.argv[2]
    startimg = cv2.imread(img_path1)
    endimg = cv2.imread(img_path2)

    print Square.compare_axes(endimg, startimg, 1)    
    #main(sys.argv[1:])
        
