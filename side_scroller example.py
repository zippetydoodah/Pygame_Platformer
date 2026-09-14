import pygame
import sys

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([900, 600]) 

exit = True # setting while loop
gravity = 0.025

class Player:
    def __init__(self,x,y):
        self.x = x 
        self.y = y

        self.move_up = False # these are movement flags [true when wasd keys are down and false when up]...
        self.move_right = False
        self.move_left = False
        self.move_down = False
        self.y_axis_velocity = 0 # use velocity simulate gravity...

        self.player = pygame.Surface((35, 35))
        self.rect = pygame.Rect(self.x, self.y, 35, 35) # collision rectangle

    def input_handler(self):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.y_axis_velocity = -1.5 # increase velocity...
                self.move_up = True
                self.move_down = False

            elif event.key == pygame.K_LEFT:
                self.move_left = True
                self.move_right = False

            elif event.key == pygame.K_RIGHT:
                self.move_right = True
                self.move_left = False

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.move_left = False

            elif event.key == pygame.K_RIGHT:
                self.move_right = False

    def move(self):
        self.y += self.y_axis_velocity # y axis movement i.e. gravity and velocity
        self.y_axis_velocity += gravity

        if self.move_left:
            self.x -= 1

        if self.move_right:
            self.x += 1

        if self.y_axis_velocity > 0:
            self.move_up = False
        else:
            self.move_up = True
    
        if self.y_axis_velocity < 0:
            self.move_down = False
        else:
            self.move_down = True

    def collisions(self,platforms): # collisions, probs rly bad, but it works for rectangle based sprites, if having complex sprites/images use pixel perfect collision.
        for platform in platforms:
            rect = platform.rect
            if self.rect.colliderect(rect):
                    
                    if not self.rect.colliderect(rect.move(4, 0)):
                        self.x -= 1
                # Move the player away from the collision while considering the intended direction
                    if self.move_left and not self.rect.colliderect(rect.move(-4, 0)):
                        self.x += 1
        
                    elif self.move_right and not self.rect.colliderect(rect.move(4, 0)):
                        self.x -= 1
        
                    elif self.move_up and not self.rect.colliderect(rect.move(0, -4)):
                        self.y_axis_velocity = 0
                        self.y += 0.5
                            
                    elif self.move_down and not self.rect.colliderect(rect.move(0, 4)):
                        self.y_axis_velocity = 0
                        self.y -= 0.5
        
                    elif self.move_right and self.move_down and not self.rect.colliderect(rect.move(4, 4)):
                        self.x -= 2
        
                    elif self.move_right and self.move_up and not self.rect.colliderect(rect.move(4, -4)):
                        self.x -= 2
        
                    elif self.move_left and self.move_down and not self.rect.colliderect(rect.move(-4, 4)):
                        self.x += 2
        
                    elif self.move_left and self.move_up and not self.rect.colliderect(rect.move(-4, -4)):
                        self.x += 2

    def render(self,screen): # rendering
        screen.blit(self.player, (self.x, self.y))
        self.player.fill((200, 200, 200))
        self.rect = pygame.Rect(self.x, self.y, 35, 35)



class Platform:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y,80,20)

    def render(self,screen):
        self.rect = pygame.Rect(self.x,self.y,80,20)
        pygame.draw.rect(screen,(200,100,100),self.rect)

def generate():
    platforms = []
    y = 50
    x = 900

    for i in range(5):
        platforms.append(Platform(x,y))
        y += 100
        x -= 150

    return platforms

platforms = generate()
player = Player(20,500)

while exit:

    clock.tick(120)
    screen.fill((255,255,255))  # filling screen white each frame.

    for event in pygame.event.get(): # events
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        player.input_handler()

    player.collisions(platforms)
    player.move()
    
    for plat in platforms:
        plat.render(screen) # rendering all platforms on top of white screen

    player.render(screen)

    pygame.display.flip() # refreshing screen