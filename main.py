#Meteor Shower
#Created By Corey Ling a.k.a. Kasuko
#Written in Python WIth Pygame

#import required libraries 
import random, os
import pygame
#place pygame module in global namespace
from pygame import *

#load our other files
from module import *
from sprites import *

height , width = 500, 400
level = 1
    
def iskeypressed():
    keys = key.get_pressed()
    if keys[K_RETURN]:
        return 1
    else:
        return 0
    
def main():

    #Initialize The random generator and The Screen
    random.seed()
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Meteor Shower by Corey Ling')
    #pygame.mouse.set_visible(False)   //Possible Use Later
    
    #Load the Background Image
    background_image, background_rect = load_image('background.png')
    screen.blit(background_image, (0,0))
    
    #Create All Sprites and Groups
    playermissle_sprite = pygame.sprite.RenderClear()   #Missle Group
    explosion_sprites = pygame.sprite.RenderClear()    #Explosion Group
    meteor_sprites = pygame.sprite.RenderClear()        #Meteor Group
    playerpost_sprite = pygame.sprite.RenderClear() #Command Post Group
    playerpost_sprite.add(Post((200,400)))  #Command Post Sprite
    playerbase_sprites = pygame.sprite.RenderClear()    #Base Group
    playerbase_sprites.add(Base((50,430)))  #Base 1 Sprite
    playerbase_sprites.add(Base((150,430))) #Base 2 Sprite
    playerbase_sprites.add(Base((250,430))) #Base 3 Sprite
    playerbase_sprites.add(Base((350,430))) #Base 4 Sprite
    
    
    explosion = load_sound('Explode.wav')   #Exploding Sound Effect
    firing = load_sound('Fire.wav')     #Firing Sound Effect      
    
    #Top Text Creation
    topfont = pygame.font.Font(None, 24)
    titlefont = pygame.font.Font(None, 48)
    toptext = topfont.render('Score: 0', False, (255, 255, 0))
    toptextpos = toptext.get_rect()
    toptextpos.top = 0
    toptextpos.centerx = 200
    screen.blit(toptext, toptextpos)
    
    #Declare Variables
    running = 1 #Used to exit main game loop 
    counter = 0 #Used to count stuff
    isfired = 0 #Used to detect if missle has been shot or not
    score = 0
    #Main Game Loop
    while running:
        #Timing To Slow Game Down
        pygame.time.delay(10)
        
        #Event Controller
        for event in pygame.event.get():
          if event.type == QUIT:    #on quit exit
                running = 0
                restart = 0
          elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:   #exit when press escape
                    running = 0
                    restart = 0
          elif event.type == MOUSEBUTTONDOWN:   #Mouse Button Down Control
                    if isfired == 0 and event.pos[1] < 420: #If there is no Missle and you clicked above the Post
                        fire_to = event.pos #Set the Destination to the mouse position
                        playermissle_sprite.add(Missle(fire_to))    #Create The Missle Sprite
                        firing.play()   #Play Sound Effect
                        isfired = 1     #Set isfired to 1
                    elif isfired == 1:  #but if the missle is already fired
                        isfired = 0         #We're about to blow it up so you can fire another
                        MissleSprite = playermissle_sprite.sprites()    #Get the missle (used in obtaining position)
                        explosion_sprites.add(Explosion(MissleSprite[0].rect.center))  #Create the explosion
                        playermissle_sprite.empty()     #Remove the Missle
                        playermissle_sprite.clear(screen, background_image) #Erase the missle
                        explosion.play()    #Play Explosion Sound Effect

        #Meteor AI
        if len(meteor_sprites) < random.randint(3,5):
            randvelo = 0
            randvelo = float(score/1000)
            randvelo += random.randint(-1,1)
            if randvelo < 1: randvelo = 1
            meteor_sprites.add(Meteor((random.randint(0,400),500),randvelo,(random.randint(0,400),0)))
        #Clear All Sprites
        playermissle_sprite.clear(screen, background_image)
        explosion_sprites.clear(screen,background_image)
        meteor_sprites.clear(screen, background_image)
        playerbase_sprites.clear(screen, background_image)
        
        #Collison Detection
        MeteorCollision = sprite.groupcollide(meteor_sprites, explosion_sprites, True, False)
        BaseCollision = sprite.groupcollide(meteor_sprites, playerbase_sprites, True, True)
        MeteorCollisionSize = len(MeteorCollision)
        
        for cSprite, ListoSprites in MeteorCollision.items():
            explosion_sprites.add(Explosion(cSprite.rect.center))
        
        playerbasesize = len(playerbase_sprites)
        #Game Logic
        if MeteorCollisionSize != 0 and playerbasesize != 0: #Only change the score when needed for speed
            #Handle Score
            score += 50 * MeteorCollisionSize + (MeteorCollisionSize - 1) * 25
            mystr = "Score: %d" % (score,)
            toptext = topfont.render(mystr, False, (255, 255- (score/50), 0))
            toptextpos = toptext.get_rect()
            toptextpos.centerx = 200
            screen.blit(background_image,toptextpos,toptextpos)
        screen.blit(toptext, toptextpos)
        
        #Handle Game Over
        if playerbasesize == 0:
            titletext = titlefont.render('GAME OVER', False, (255, 0, 0))
            titletextpos = titletext.get_rect()
            titletextpos.centery = height/2
            titletextpos.centerx = width/2
            screen.blit(titletext,titletextpos)
            pygame.time.delay(100)
##            restart = False
##            while not restart:
##                pygame.time.delay(100)
##                print iskeypressed()
##                if iskeypressed():
##                    restart = True
##                    screen.blit(background_image,titletextpos,titletextpos)
##                else:
##                    screen.blit(titletext,titletextpos)
        
        
        #Update Sprites
        playermissle_sprite.update()
        explosion_sprites.update(explosion_sprites)
        meteor_sprites.update(meteor_sprites)
        
        #Draw All Sprites    TODO: Increase Efficency By Drawing Only Whats Needed
        playermissle_sprite.draw(screen)
        explosion_sprites.draw(screen)
        playerpost_sprite.draw(screen)
        playerbase_sprites.draw(screen)
        meteor_sprites.draw(screen)
        
        
        #Display Drawed Sprites to Screen
        pygame.display.flip()
    
    #When not running exit
    return
    
if __name__ == '__main__': main()
