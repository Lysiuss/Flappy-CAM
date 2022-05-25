import pygame
import pygame,sys
import random
from pathlib import Path
from os import listdir
from os.path import isfile, join
import easygui
from random import randint

#Couleurs déterminées à l'avance
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,128,0)


#Here we get every files in each directories
player_face = [f for f in listdir(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Bird image') if isfile(join(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Bird image', f))]

background_image = [f for f in listdir(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Background_images Stock') if isfile(join(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Background_images Stock', f))]

floor_image = [f for f in listdir(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Floor images stock') if isfile(join(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Floor images stock', f))]


#We then remove the extension for a cleaner look on the GUI
for i in range (0, len(background_image)):
    background_image[i] = background_image[i][0 : len(background_image[i])-4]

for i in range (0, len(player_face)):
    player_face[i] = player_face[i][0 : len(player_face[i])-4]

for i in range (0, len(floor_image)):
    floor_image[i] = floor_image[i][0 : len(floor_image[i])-4]

#We then start the interaction with the player
number_players = easygui.enterbox("Welcome to Flappy Bird ! Enter the number of players (1 or 2)")

if number_players == "1":
    #Here we give the choice of the avatar the player wants
    number_one_name = easygui.enterbox("Which bird do you want to play with ? Enter the corresponding number : "+"1. "+player_face[0]+", "+"2. "+player_face[1]+", "+"3. "+player_face[2]+", "+"4. "+player_face[3]+", "+"5. "+player_face[4]+", "+"6. "+player_face[5]+", "+"7. "+player_face[6]+", "+"8. "+player_face[7]+", "+"9. "+player_face[8]+".")
    player_one_name = player_face[int(number_one_name)-1] #this line allows the user to only enter a number and still have the corresponding avatar

if number_players == "2":
    #Same here but 2 times because we have two players
    number_one_name = easygui.enterbox("Welcome to Flappy Bird 1v1 ! Let's see who is the best... First, choose which bird you want to play with : "+"1. "+player_face[0]+", "+"2. "+player_face[1]+", "+"3. "+player_face[2]+", "+"4. "+player_face[3]+", "+"5. "+player_face[4]+", "+"6. "+player_face[5]+", "+"7. "+player_face[6]+", "+"8. "+player_face[7]+", "+"9. "+player_face[8]+".")
    number_two_name = easygui.enterbox("Enter the number of the character that the second player wants to play (a different one preferably) : "+"1. "+player_face[0]+", "+"2. "+player_face[1]+", "+"3. "+player_face[2]+", "+"4. "+player_face[3]+", "+"5. "+player_face[4]+", "+"6. "+player_face[5]+", "+"7. "+player_face[6]+", "+"8. "+player_face[7]+", "+"9. "+player_face[8]+".")
    player_one_name = player_face[int(number_one_name)-1]
    player_two_name = player_face[int(number_two_name)-1]

#Here we allow the user to change the default background, floor and difficulty if he wants to
change_settings = easygui.enterbox("Do you want to change basic settings (floor, background and  difficulty) ? (yes/no)")

if change_settings == "yes":
    background_name = easygui.enterbox("You can choose on which background you want to play ! Choose wisely... You can play on : "+background_image[0]+", "+background_image[1]+", "+background_image[2]+".")
    floor_name = easygui.enterbox("Choose the floor of the flappy bird : "+floor_image[0]+", "+floor_image[1]+".")
    difficulty = easygui.enterbox("Choose your difficulty : 1 = Normal, 2 = Hard, 3 = Extreme")
else : #Those by defaults are the ECAM and the floor of original Flappy Bird, we also have a difficulty Normal by default
    background_name = "ECAM"
    floor_name = "Default"
    difficulty = "1"

pygame.init()

screen = pygame.display.set_mode((1600,1065))
pygame.display.set_caption("Flappy Multiplayer")
clock = pygame.time.Clock()
game_font = pygame.font.Font('freesansbold.ttf', 33)
game_font2 = pygame.font.Font('freesansbold.ttf', 20)
game_over = pygame.font.Font('freesansbold.ttf', 60)
pause_text = pygame.font.SysFont('freesansbold.ttf', 80).render('Pause', True, pygame.color.Color('White'))
pause_text2 = pygame.font.SysFont('freesansbold.ttf', 40).render('Press Backspace to resume', True, pygame.color.Color('White'))

#game variables
gravity = 0.25
bird_movement = 0
game_active = False
score =0
high_score=0
first_try = True
playerone= False
playertwo = False


background = pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Background_images Stock\{}.jpg'.format(background_name)).convert()
floor = pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Floor images stock\{}.png'.format(floor_name)).convert()
floor = pygame.transform.scale2x(floor)
floorsX = 0


def getFloor():
    screen.blit(floor, (floorsX, 825))
    screen.blit(floor, (floorsX + 387, 825))
    screen.blit(floor, (floorsX + 774, 825))
    screen.blit(floor, (floorsX + 1161, 825))
    screen.blit(floor, (floorsX + 1548, 825))

def gameover(x):
    over = game_over.render("GAME OVER", True, (255,2,2))
    sp = game_font2.render("Press R to retry", True, (255,5,2))
    screen.blit(over, (15,255))
    screen.blit(sp, (28,320 ))
    if number_players == "2":
        playerwins(x)
    if number_players == "1":
        over = game_over.render(player_one_name+" has scored "+str(scoref)+" !", True, (0,230,23))
        screen.blit(over, (15,200))

def create_pipe():
    rand_pipeh = random.choice(pipe_height)
    rand_gap = random.choice(gap_dist)
    i = randint(0,3)
    new_pipe = pipe[i].get_rect(midtop=(1600,rand_pipeh))
    opp_pipe = pipe[i].get_rect(midbottom=(1600,rand_pipeh-rand_gap))
    return new_pipe, opp_pipe

def move_pipe(pipes):
    for pipex in pipes:
        pipex.centerx -=5
    return pipes

def show_pipe(pipes):
    for pipex in pipes:
        if pipex.bottom>600:
            i = randint(0,3)
            screen.blit(pipe[i], pipex)
        else:
            screen.blit(pygame.transform.flip(pipe[i],False, True), pipex)

def check_collision(pipes):
    for pipex in pipes:
        if bird_rect.colliderect(pipex):
            return True
    return False

def rcheck_collision(pipes):
    for pipex in pipes:
        if bird2_rect.colliderect(pipex):
            return True
    return False

def rotated_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def score_display():
    score_surf = game_font.render("Score " + str(score),True, (0,0,0))
    screen.blit(score_surf, (20,35))

def high_score_display():
    high_score_surf = game_font2.render("High Score "+str(high_score),True,(0,0,0))
    screen.blit(high_score_surf, (20,85))

def welcome():
    over = game_over.render("Welcome!! ", True, (0,0,230))
    ll = game_font2.render("Press R to play !", True,(0,0,230))
    if number_players == "1":
        touche = game_font2.render("Jump = Space", True,(0,0,230))
    if number_players == "2":
        touche = game_font2.render("Jump (Player 1) : Space, Jump (Player 2) : UP_Arrow", True,(0,0,230))
    screen.blit(over, (15,255))
    screen.blit(ll, (25,320))
    screen.blit(touche, (25, 380))


def playerwins(who):
    over = game_over.render(who+" wins!!", True, (0,230,23))
    screen.blit(over, (15,200))

bird2 = pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Bird image\{}.png'.format(player_one_name)).convert_alpha()
bird1 = pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Bird image\{}.png'.format(player_one_name)).convert_alpha()
bird3 = pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Bird image\{}.png'.format(player_one_name)).convert_alpha()
birdlist = [bird1, bird2, bird3]
bird_index = 0
bird = birdlist[bird_index]
bird_rect = bird.get_rect(center=(50,300))
BIRDFLAP =  pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)


#second brid info
if number_players == "2" :

    bird2_1 = pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Bird image\{}.png'.format(player_two_name)).convert_alpha()
    bird2_2 = pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Bird image\{}.png'.format(player_two_name)).convert_alpha()
    bird2_3 = pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\Bird image\{}.png'.format(player_two_name)).convert_alpha()
    bird2list = [bird2_1, bird2_2, bird2_3]
    bird2index = 1
    bird2 = bird2list[bird2index]
    bird2_rect = bird2.get_rect(center=(50,300))
    bird2_movement = 0

pipe = [pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\PipesFolder\pipe_green.png'), pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\PipesFolder\pipe_blue.png'), pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\PipesFolder\pipe_yellow.png'), pygame.image.load(r'C:\Users\lysiu\OneDrive\Desktop\Flappy Bird\local-multiplayer-flappy-bird-main\PipesFolder\pipe_red.png')]

for i in range (0, len(pipe)):
    pipe[i] = pygame.transform.scale(pipe[i],(80,600))

pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1300)
pipe_height = [450,350,400,375,285,225,300,425,275]

#Difficulty parameters
if difficulty == "1":
    gap_dist = [225,250,300,175,280]
elif difficulty == "2":
    gap_dist = [160,170,180,210,220,250]
elif difficulty == "3":
    gap_dist = [140,150,170,190,210,130]

running, pause = 0, 1
state = running
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                bird_movement=0
                bird_movement -=7
            if event.key ==pygame.K_UP and number_players == "2":
                bird2_movement = 0
                bird2_movement -=7
            if event.key == pygame.K_r and game_active==False:
                game_active = True
            if event.key == pygame.K_RETURN:
                state = pause
            if event.key == pygame.K_BACKSPACE:
                state = running

        if event.type == SPAWNPIPE and game_active and state == running:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index <2:
                bird_index +=1
            else:
                bird_index=0
            bird = birdlist[bird_index]
            if number_players == "2":
                if bird2index <2:
                    bird2index +=1
                else:
                    bird2index=0
                bird2 = bird2list[bird2index]


    screen.blit(background,(0,0))
    if not game_active and first_try:
        welcome()
    if game_active:
            # bird movement
        if state == running:
            first_try = False
            if bird_rect.centery < 5:
                bird_movement = 0
                bird_rect.centery = 5
            if number_players == "2":
                if bird2_rect.centery < 5:
                    bird2_movement = 0
                    bird2_rect.centery = 5

            bird_movement += gravity
            rot_bird = rotated_bird(bird)
            bird_rect.centery += bird_movement
            screen.blit(rot_bird, bird_rect)
            if number_players == "2":
                rot_bird2 = rotated_bird(bird2)
                bird2_rect.centery += bird2_movement
                bird2_movement += gravity
                screen.blit(rot_bird2, bird2_rect)

            # collision code
            if  check_collision(pipe_list) or bird_rect.centery > 494:
                game_active = False
                pipe_list.clear()
                bird_movement = 0
                bird_rect.centery = 300
                if number_players == "2":
                    bird2_movement = 0
                    bird2_rect.centery = 300
                scoref = score
                score = 0
                high_score_display()
                playertwo = True
            if number_players == "2":
                if rcheck_collision(pipe_list) or bird2_rect.centery>494:
                    game_active = False
                    pipe_list.clear()
                    bird_movement = 0
                    bird_rect.centery = 300
                    bird2_movement = 0
                    bird2_rect.centery = 300
                    score = 0
                    high_score_display()
                    playerone = True
            #pipe movement
            pipe_list = move_pipe(pipe_list)
            show_pipe(pipe_list)

            # floor movement
            floorsX -= 1
            if floorsX < -400:
                floorsX = 0
            if len(pipe_list) > 7 and  pipe_list[-8].centerx==bird_rect.centerx:
                score +=1
            if score > high_score:
                high_score = score

        #pause code
        elif state == pause:
            screen.fill(black)
            score_aff = pygame.font.SysFont('freesansbold.ttf', 40).render('Score : '+str(score), True, pygame.color.Color('White'))
            high_score_aff = pygame.font.SysFont('freesansbold.ttf', 40).render('Highscore : '+str(high_score), True, pygame.color.Color('White'))
            screen.blit(score_aff, (722, 500))
            screen.blit(high_score_aff, (690, 400))
            screen.blit(pause_text, (692, 200))
            screen.blit(pause_text2, (590, 300))

    elif not first_try:
        if number_players== "2":
            if playerone:
                win = player_one_name
            if playertwo:
                win = player_two_name
            playertwo = False
            playerone = False
            gameover(win)
        if number_players == "1":
            gameover(player_one_name)

    score_display()
    high_score_display()
    getFloor()
    pygame.display.update()
    clock.tick(64)

#mettre des boutons dans le menu (et enlever numéro du coup si ok) --> chaud du cul
#rajouter du son (romain)
#rajouter une icone (valoche)
#rajouter temps après pause et afficher jeu (bizarre)
#randomize les pipes (réflexion à faire --> pas sûr)
#vies tout seul (lié difficulté) --> faisable (romain)
#faire (rapport romain : 	Les objectifs fonctionnels recherchés;	Les choix de design UI/UX; Les problèmes rencontrés et leur résolution En conclusion : l’état actuel du projet et les pistes d’évolutions envisagées) (database valoche + github) (UML mathilde)
#finir jeudi



