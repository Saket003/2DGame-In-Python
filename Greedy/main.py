from re import A
import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

#Screen setup
WIDTH, HEIGHT = 600,600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collector")

#Color Bank
WHITE = (98,99,97)
BLACK = (0,0,0)
A = ()
B = ()
C = ()
D = (94,87,104)
E = (58,68,93)

#Constants
FPS = 60
HEALTH = 1
VEL = 5
MAX_CHOC = 9
#VEL = 

#Events
BORDER_HIT = pygame.USEREVENT + 1
CHOC_HIT = pygame.USEREVENT + 2


#Image import and rectangle size set
PLAYER_WIDTH, PLAYER_HEIGHT = 40,32
CHOC_WIDTH, CHOC_HEIGHT = 20,20
PLAYER_IMAGE = pygame.image.load(os.path.join('Assets', 'player.png'))
PLAYER = pygame.transform.scale(PLAYER_IMAGE,(PLAYER_WIDTH, PLAYER_HEIGHT))
CHOC_IMAGE = pygame.image.load(os.path.join('Assets', 'collect.png'))
CHOC = pygame.transform.scale(CHOC_IMAGE,(CHOC_WIDTH, CHOC_HEIGHT))
B1 = pygame.Rect(0,0,10,HEIGHT)
B2 = pygame.Rect(0,0,WIDTH,10)
B3 = pygame.Rect(WIDTH-10,0,10,HEIGHT)
B4 = pygame.Rect(0,HEIGHT-10,WIDTH,10)
#Audio Import

#https://stackoverflow.com/questions/38001898/what-fonts-can-i-use-with-pygame-font-font#:~:text=freetype%20module%20which%20supports%20TTF,font%20files%20by%20calling%20pygame.
#Font import
END_FONT = pygame.font.Font('Assets/DynaPuff.ttf',100)
COUNT_FONT = pygame.font.Font('Assets/DynaPuff.ttf',60)
HIGHSCORE_FONT = pygame.font.Font('Assets/DynaPuff.ttf',60)
#SysFont for built-in

#Functions - motion and draws
def handle_motion(keys_pressed, player, vel, grav_vel):
    player.y +=grav_vel
    if keys_pressed[pygame.K_a]:
        player.x -= vel
    if keys_pressed[pygame.K_w]:
        player.y -= vel
    if keys_pressed[pygame.K_s]:
        player.y += vel
    if keys_pressed[pygame.K_d]:
        player.x += vel
    if player.x<0 or player.y<0 or player.x + player.width>WIDTH or player.y + player.height>HEIGHT:
        pygame.event.post(pygame.event.Event(BORDER_HIT))

def collide_choc(player, choc):
    for c in choc:
        if player.colliderect(c):
            pygame.event.post(pygame.event.Event(CHOC_HIT))
            choc.remove(c)

def draw_choc(choc):
    x = int(random.random()*(WIDTH-40)+20)
    y = int(random.random()*(HEIGHT-40)+20)
    c = pygame.Rect(x,y,CHOC_WIDTH,CHOC_HEIGHT)
    choc.append(c)


def draw_window(player,choc, choc_count):
    WIN.fill(D)
    pygame.draw.rect(WIN, E, B1)
    pygame.draw.rect(WIN, E, B2)
    pygame.draw.rect(WIN, E, B3)
    pygame.draw.rect(WIN, E, B4)
    draw_text = COUNT_FONT.render("Count: "+str(choc_count), 1 , WHITE)
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2) )
    WIN.blit(PLAYER,(player.x,player.y))
    for c in choc:
        WIN.blit(CHOC,(c.x,c.y)) 
    pygame.display.update()

def draw_end(choc_count, high_score):
    WIN.fill(BLACK)
    draw_text = END_FONT.render("F", 1 , WHITE)
    WIN.blit(draw_text,(WIDTH/2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2 - 50) )
    draw_text2 = COUNT_FONT.render("Count: "+str(choc_count), 1 , WHITE)
    WIN.blit(draw_text2,(WIDTH/2 - draw_text2.get_width()//2, HEIGHT//2 - draw_text2.get_height()//2 + draw_text.get_height()//2-30) )
    if(choc_count > high_score[0]):
        high_score[0] = choc_count
    draw_text3 = HIGHSCORE_FONT.render("Best: "+str(high_score)[1:-1], 1 , WHITE)
    WIN.blit(draw_text3,(WIDTH/2 - draw_text3.get_width()//2, HEIGHT//2 - draw_text2.get_height()//2 + draw_text.get_height()//2 + draw_text2.get_height()//2- 12) )
    pygame.display.update()
    pygame.time.delay(2000)

def main(high_score):
    #Initialise rectangles, lists and values resetting
    player = pygame.Rect(WIDTH/2 - PLAYER_WIDTH/2,HEIGHT/2 - PLAYER_HEIGHT/2,PLAYER_WIDTH,PLAYER_HEIGHT)
    
    choc = []
    choc_count = 0

    health = HEALTH
    vel = VEL
    grav_vel = vel//4

    clock = pygame.time.Clock()
    run = True
    health = HEALTH
    while(run):
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                fo = open("Assets/hs.txt", "w")
                s = str(high_score[0])
                fo.write(s)
                fo.close()
                pygame.quit()

            if event.type == BORDER_HIT:
                health -= 1
            
            if event.type == CHOC_HIT:
                vel += 0.5
                grav_vel = vel//4
                choc_count +=1
        
        if health<=0:
            draw_end(choc_count, high_score)
            break
        
        while len(choc) < MAX_CHOC:
            draw_choc(choc)
        keys_pressed = pygame.key.get_pressed()
        handle_motion(keys_pressed,player,vel,grav_vel)
        collide_choc(player, choc)
        draw_window(player, choc, choc_count)
    main(high_score)

if __name__ == "__main__":
    fo = open("Assets/hs.txt", "r")
    high_score = []
    try:
        high_score.append(int(fo.read()))
    except:
        high_score.append(0)
    fo.close()
    main(high_score)