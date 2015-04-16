"""
Used for testing image processing functionality for the ScribblerIBVO Class
@author Naveen Chandran
"""
from PIL import Image
import cv2 as cv

class ImageProcessing():
    
    @staticmethod
    def getBlackBox(img):
        pass
    
    """
    Converts and image to black and white (not grayscale) from a color image.
    @param img: The relative file path of the image
    @return    An image object representing the color picture in black and white
    """
    @staticmethod
    def imgToBlackAndWhite(img):
        color_img = Image.open(img)
        gray_img = color_img.convert('L')
        bw_img = gray_img.point(lambda x: 1 if x>50 else 0, '1')
        return bw_img



    """
    Crops the image the specified percent from the left, right, top, and bottom
    @param img:    The image 
    @param percent:     (double) The percent to crop from all sides from 0 - 0.5
    """
    @staticmethod
    def cropFromSides(img, percent):
        width, height = img.size
        left, upper, right, bottom = (int(width*percent), int(height*percent), int(width*(1-percent)), int(height*(1-percent)))
        return img.crop((left,upper,right,bottom))
        


def main(args):
    #set args values here
    img = args[0]
    
    """
    Begin debugging code here
    """
 
        
        
        
        
if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
        