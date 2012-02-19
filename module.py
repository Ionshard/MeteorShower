import random, os, math
import pygame
from pygame import *

#Function Used To Load an Image File
def load_image(file_name, colorkey=None):
    #Grab the directory
    full_name = os.path.join('data', file_name)
    
    #try to load it
    try:
        image = pygame.image.load(full_name)
    except pygame.error, message:
        print 'Cannot load image:', full_name
        raise SystemExit, message
    #Should Convert But Causes Trouble With Alphas
    #image = image.convert()
   # Set the color key
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
            print colorkey
        image.set_colorkey(colorkey, RLEACCEL)
    #Return the image, and the images rectangle
    return image, image.get_rect()

# Function Used to Load Sound Effects
def load_sound(name):
    #Class that will allow game to continue with no sound
    class No_Sound:
        def play(self): pass
    #If the mixer failed to initialize
    if not pygame.mixer or not pygame.mixer.get_init():
        #Nice error message and return safe class
        print 'Error, Mixer not Initialized'
        return No_Sound()
    #get the directory of sound file
    fullname = os.path.join('data', name)
    #Make sure it exists
    if os.path.exists(fullname):
        #Get the sound and return in
        sound = pygame.mixer.Sound(fullname)
        return sound
    else:
        #Error message and return safe class
        print 'File does not exist:', fullname
        return No_Sound()

#Function Used to Calculate Angle Needed to Rotate Missle
def GetAngle(ClickedAt, Origin):
    o = abs(ClickedAt[0] - Origin[0])   #Get the Oppsite Length
    a = abs(ClickedAt[1] - Origin[1])   #Get Adjacent Length
    
    if a == 0:  #Avoid Division by 0
        return 0
    else:
        #Find the Angle Needed (in radians)
        Angle = math.atan2(o,a)
        #Convert Radians to Degrees
        Angle = Angle * 180 / math.pi
        #if the hypotanuse is to the right of the center we need to rotate clockwise or negative angle
        if ClickedAt[0] > Origin[0]:
            return Angle*-1
        else:
            return Angle
            
def GetVector(pA, pB, Velocity):
    Vmx = pB[0] - pA[0]
    Vmy = pB[1] - pA[1]
    divisor = math.sqrt( (pB[0] - pA[0])**2 + (pB[1] - pA[1])**2)
    Vnorm = (Vmx / divisor, Vmy / divisor)
    Vmove = (Vnorm[0] * Velocity, Vnorm[1] * Velocity)
    return Vmove

tuple_adder = lambda P,Q: (P[0]+Q[0], P[1]+Q[1])
