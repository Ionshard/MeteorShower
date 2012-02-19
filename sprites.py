import pygame, random
from pygame import *
from module import *

#Class used when creating Base Sprites
class Base(pygame.sprite.Sprite):
    """This class is for the players bases or life"""
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self) #call Sprite initalizer
        self.image, self.rect = load_image('Base.png', (255, 255, 255, 0))  #Load sprite image
        self.rect.center = location #Set the position to the given location
        
#Class used when creating Command Post Sprites
class Post(pygame.sprite.Sprite):
    """This class is for the players command post"""
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self) #call Sprite initalizer
        self.image, self.rect = load_image('CommandPost.png', (180, 180, 180, 0))   #Load sprite image
        self.rect.center = location #set position to given location

#Class used to create missle sprite
class Missle(pygame.sprite.Sprite):
    """This is the missle fired from user """
    #Because of so many missles being fired we want to load image once
    image = None
    #Initialization
    def __init__(self, destination):
        pygame.sprite.Sprite.__init__(self) #call Sprite initalizer
        if Missle.image is None:    #Is this the first time making a missle
            Missle.image, self.rect = load_image('Missle.png', (255, 255, 255, 0))  #Well then load the image
        self.image = Missle.image   #Set the single image to the global image
        self.rect = self.image.get_rect()   #get the rectangle from the single image
        self.rect.center = (195,400)    #All missles get launched from the command post
        self.vector = GetVector(self.rect.center, destination, 10) # Get the vector to calculate movement
        self.dest = destination     #Get the missles destination that is givien
        self.image = transform.rotate(Missle.image, GetAngle(destination, self.rect.center))  #Rotate the image so it travels to the destination straight
        self.counter = 0    #Counting Variable (used in Update)
        self.x = self.rect.centerx #We need a float to hold the x to avoid rounding errors of using the rect
        self.y = self.rect.centery #We also need a float to hold the y for the same reason

    def update(self):   #Moves the missle towards dest on path
        self.x += self.vector[0]
        self.y += self.vector[1]
        self.rect.centerx = self.x
        self.rect.centery  = self.y

#Class used to have the explosion 
class Explosion(pygame.sprite.Sprite):
    """The Explosion Used When Blowing Up a Missle"""
    image = None    #Again there will be multiple explosions so we only want to load image once
    def __init__(self, position):
            pygame.sprite.Sprite.__init__(self) #call Sprite initalizer
            if Explosion.image is None:     #first explosion
                Explosion.image, self.rect = load_image('Explosion.png', (255, 255, 255, 0))    #Then load image
            self.image = Explosion.image        #Set the image to gloabal image
            self.rect = self.image.get_rect()   #Get the rectangle of the image
            self.rect.center = position     #Set postion to given position
            self.life = 30  #Life span of how long explosion stays
            self.scale = 0.97

    def update(self, MyGroup):   #Keeps explosion alive for so long
        if self.life == 0:  # if its time to die
            MyGroup.empty() #Remove the explosion
        else:
            self.life -= 1     #Minus one from its life
            self.image = Explosion.image    #revert back to original image
            self.scale = 1./self.scale  #invert the scale so if it was small now it gets big
            self.image = transform.rotozoom(self.image, 0, self.scale)  #Scale (we use rotozoom for its Scale multiplier)
            
##    def remove_internal(self):
##        print 'Removing Explosion'

#Class used when making meteor sprite
class Meteor(pygame.sprite.Sprite):
    images = []
    def __init__(self, Destination, Velocity, Origin = (0,0)):
        pygame.sprite.Sprite.__init__(self) #call Sprite initalizer
        if len(Meteor.images) == 0:
            temp = None
            temp, self.rect = load_image('Meteor1.png')
            Meteor.images.append(temp)
            temp, self.rect = load_image('Meteor2.png')
            Meteor.images.append(temp)
            temp, self.rect = load_image('Meteor3.png')
            Meteor.images.append(temp)
        self.image = Meteor.images[random.randint(0,2)]
        self.rect = self.image.get_rect()
        self.rect.center = Origin
        self.dest = Destination
        self.image = transform.rotate(self.image, (GetAngle(self.dest,Origin)*-1))  #Rotate the image so it travels to the destination straight(we need to *-1 because it is travelling down)
        self.vector = GetVector(Origin, Destination, Velocity)
        self.x = self.rect.centerx
        self.y = self.rect.centery
        
    def update(self, parentgroup):
        self.x += self.vector[0]
        self.y += self.vector[1]
        self.rect.centerx = self.x
        self.rect.centery  = self.y
        if self.y > 500:
            parentgroup.remove(self)
