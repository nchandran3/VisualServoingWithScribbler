"""
@author Naveen Chandran, Justin Jackson, Christian Nash
This robot class essentially controls the robot and uses Visual Servoing to navigate between two different
locations that are given through images. It calculates its pose at each succession of the algorithm and compares it
to the ending result. If they are within a certain threshold, it returns successful and stops all movement. 
"""
from Scribbler2 import Scribbler2

class ScribblerIBVS(Scribbler2):
    
    def __init__(self, port, filename, baud=38400):
        super(ScribblerIBVS, self).__init__(port, filename, baud) 
        
