#3/2023-6/2023
#Levi's Dash
#Main file of the video game

import pygame, sys, random, math, time

pygame.init()
#general game parameters
clock = pygame.time.Clock()
FPS = 60
tracer_frequency = 1500
last_tracer = pygame.time.get_ticks()
timer = 0
gamefont = pygame.font.Font(None, 30)

#screen dimensions and title
screen_w = 700
screen_h = 700
screen = pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption("Levi's Dash")

#timer placement
timertext = gamefont.render("Timer: "+str(timer), 1 , [255,255,255])
boxsize = timertext.get_rect()
timerXpos = (screen_w)/10

#function used to reset respective game variables
def reset_game():
    tracer_group.empty()
    levi.rect.x = 200
    levi.rect.y = screen_h / 2
    pygame.mixer.music.load("music.wav")
    pygame.mixer.music.play(-1)
    timer = 0
    tracer_frequency = 1500
    return timer,tracer_frequency

#function to quit the game (press the x-button to quit)
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
#Tracer class creation, movement, and animation
class Tracer(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #sprite list set up to store our different tracer imgs
        self.tracers = []
        self.tracers.append(pygame.image.load("tracer.png"))
        self.tracers.append(pygame.image.load("tracer2.png"))
        self.tracers.append(pygame.image.load("tracer3.png"))
        self.current_tracer = 0
        self.image = self.tracers[self.current_tracer]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        #tracer cycles thru list in the update function to animate
        self.current_tracer += 1
        if (self.current_tracer >= len(self.tracers)):
            self.current_tracer = 0
        self.image = self.tracers[self.current_tracer]
        
        self.rect.x -= 10 #speed of Tracers
        if self.rect.right < 0: #gets rid of Tracers when off screen
            self.kill()

#Levi class creation, movement, and animation           
class Levi(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #list created to store and cycle thru imgs
        self.levis = []
        self.levis.append(pygame.image.load("LeviAck.png"))
        self.levis.append(pygame.image.load("LeviAck2.png"))
        self.levis.append(pygame.image.load("LeviAck3.png"))
        self.levis.append(pygame.image.load("LeviAck3.png"))
        self.levis.append(pygame.image.load("LeviAck2.png"))
        self.levis.append(pygame.image.load("LeviAck.png"))
        self.current_levi = 0
        self.image = self.levis[self.current_levi]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
    def update(self):
        self.current_levi += 0.2
        if (self.current_levi >= len(self.levis)):
            self.current_levi = 0
        self.image = self.levis[int(self.current_levi)]

        #sprite key movement using WASD and arrows (bounderies are set)
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]):
            if (self.rect.x > 0):
                self.rect.x -= 4
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
            if (self.rect.x < 600):
                self.rect.x += 4
        if (keys[pygame.K_UP] or keys[pygame.K_w]):
            if (self.rect.y > 0):
                self.rect.y -= 4
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]):
            if (self.rect.y < 590):
                self.rect.y += 4

#Reset button class creation and functionality
class Reset():
    def __init__(self, x, y, image):
        self.image = image
        self.image = pygame.transform.scale(self.image,(200,100))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y*1.5) #multiplied by 1.5 to fix alignment and collion hit box      
    def draw(self):
        action = False
        mous_pos = pygame.mouse.get_pos()
        #if the mouse is over the button and clicked
        if (self.rect.collidepoint(mous_pos)):
            if (pygame.mouse.get_pressed()[0]==1): 
                action = True
        
        #draw button
        screen.blit(self.image, (self.rect.x, self.rect.y)) 
        return action
    
#group additions
levi_group = pygame.sprite.Group()
tracer_group = pygame.sprite.Group()
levi = Levi(200,int(screen_h/2)) #class called and x/y initial set
levi_group.add(levi) #sprite added to group


#image setup
bgimg = pygame.image.load("Stohessdistrict.png").convert()
bgimg_width = bgimg.get_width() #finds width of the background image
gr_img = pygame.image.load("roof.png")
grimg_width = gr_img.get_width()
reset_button = pygame.image.load("reset.png")

#gameover sign is loaded in and the size is transformed
gameover = pygame.image.load("gameover.png")
gameover = pygame.transform.scale(gameover,(500,100))

#define game variables
bg_scroll = 0
bg_tiles = math.ceil(screen_h/bgimg_width) + 100

gr_scroll = 0
gr_tiles = math.ceil(screen_h/grimg_width) + 1

#music played on repeat
pygame.mixer.music.load("music.wav")
pygame.mixer.music.play(-1)

#restart button instance
button = Reset(screen_w/3,screen_h/3,reset_button)

#fixed reset problems by adding new game over variable and making this run only if game is running
running = True
game_over = False
#main game loop
while (running):
    handle_events()
    
    clock.tick(FPS)
    #fixed reset probelm by adding new game over variable and making this run only if game is running
    if game_over == False:  
        #drawing a scrolling background
        for i in range(0,bg_tiles):
            screen.blit(bgimg,(i*bgimg_width + bg_scroll,0))

        #scroll background
        bg_scroll -= 1
        #reset scroll
        if (abs(bg_scroll) > bgimg_width):
            br_scroll = 0

        #drawing a scrolling ground
        for i in range(0,gr_tiles):
            screen.blit(gr_img,(i*grimg_width + gr_scroll,550))

        #scroll ground
        gr_scroll -= 6
        #reset scroll
        if (abs(gr_scroll) > grimg_width):
            gr_scroll = 0

        #generate new Tracers
        time_now = pygame.time.get_ticks()

        if (time_now - last_tracer > tracer_frequency):
            tracer_fly = Tracer(700,random.randint(5,600))
            tracer_group.add(tracer_fly)
            last_tracer = time_now

    #Increase game difficulty (incr. amount of Tracers over time)
    if (timer >= 30):
        tracer_frequency -= 1

    #sprite group draw
    levi_group.draw(screen)
    tracer_group.draw(screen)

    if (game_over == False): #fixed blurr problem
        tracer_group.update()
        levi_group.update()

    #collision
    if (pygame.sprite.groupcollide(levi_group, tracer_group, False, False)):
        pygame.mixer.music.stop()
        game_over = True
        button.draw()
        screen.blit(gameover,(screen_w/8,screen_h/3))   

    if (game_over == False):
        #running timer
        seconds = clock.tick()/300.0
        timer += seconds
        display_timer = math.trunc(timer)

    #draw timer
    timertext = gamefont.render("Timer: "+str(display_timer), 1 , [255,255,255])
    screen.blit(timertext, [timerXpos,50])

    #check for game over and draw rest button
    if (game_over == True):
        if (button.draw()==True):
            timer,tracer_frequency = reset_game()
            game_over = False

    pygame.display.flip()
       






