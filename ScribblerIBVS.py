"""
@author Naveen Chandran, Justin Jackson, Christian Nash
This robot class essentially controls the robot and uses Visual Servoing to navigate between two different
locations that are given through images. It calculates its pose at each succession of the algorithm and compares it
to the ending result. If they are within a certain threshold, it returns successful and stops all movement. 
"""
from Scribbler2 import Scribbler2
import Square
import ImageProcessing

class ScribblerIBVS(Scribbler2):
    
    def __init__(self, port, filename, baud=38400):
        super(ScribblerIBVS, self).__init__(port, filename, baud) 
        

    """
    Given the startimg and endimg, performs Image Based Visual Servoing and navigates to the end pose from its start pose
    """
    def visual_servo(self, endimg):
        axis_result = 1
        #navigate to radial circumference
        while axis_result != 0:
            startimg = self.takePicture()
            axis_result = Square.compare_axes(startimg, endimg, 5)
    
            if axis_result > 0:
                self.runCommands([100,100,1])
            elif axis_result < 0:
                self.runCommands([-100, -100, 1])
            else:
                break
            

        #compute angle to Target
        self.runCommands([100,-100,.5])
        #compute distance to Target
        self.runCommands([100,100,3])
        
        #drive
        self.runCommands([-100,100,.5])