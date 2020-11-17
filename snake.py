import pygame, random, sqlite3, time, sys
from pygame.locals import *

player_name = ("medeiroscwb")

score = 0

UP     = 0
RIGHT  = 1
DOWN   = 2
LEFT   = 3

blocksize = 20
gamespeed = 20
my_direction = RIGHT

db_name = 'snake_score'
tab_name = 'score'

screen_x = 1900
screen_y = 980
clock = pygame.time.Clock()
pygame.init()
screen=pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption('Snake')

snake = [(700, 500), (720, 500), (740, 500)]
snake_skin = pygame.Surface((blocksize,blocksize))
snake_skin.fill((150,255,220))

apple_pos = (100,100)
apple_skin = pygame.Surface((blocksize,blocksize))
apple_skin.fill((255,0,0))


def gen_table():
    conn = sqlite3.connect("{}.db".format(db_name))
    c = conn.cursor()
    c.execute("""CREATE TABLE {} (
        playername text,                         
        scr integer
        )""".format(tab_name))
    print("Table Created")
    conn.commit()
    conn.close()


def insert_row():
    conn = sqlite3.connect("{}.db".format(db_name))
    c = conn.cursor()
    c.execute(
        """INSERT INTO {} VALUES("{}","{}")""".format(tab_name, player_name, score))
    print("INSERT_LINE Executed")
    conn.commit()
    conn.close()


def query():
    conn = sqlite3.connect("{}.db".format(db_name))
    c = conn.cursor()
    c.execute("SELECT * FROM {}".format(tab_name))
    tab_all = c.fetchall()
    for line in tab_all:
        print(line[0] + "\t" + str(line[1]))
    print("Query completed.")
    conn.commit()
    conn.close()


def get_coord(snake):
    return snake

def on_grid_random():
    x = random.randint(blocksize * 5, screen_x-blocksize*5)
    y = random.randint(blocksize * 5, screen_y-blocksize*5)
    return (x//blocksize*blocksize,y//blocksize*blocksize)


def collision(c1,c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

def order_results():
    conn = sqlite3.connect("{}.db".format(db_name))
    c = conn.cursor()
    c.execute("SELECT scr, * FROM {} ORDER BY scr DESC".format(tab_name))
    tab_all = c.fetchall()
    for line in tab_all:
        print(line)
    print("^SCORE^")
    conn.commit()
    conn.close()
    

def exit():
    insert_row()
    order_results()
    pygame.quit()
    time.sleep(1)
    print('Your score is')
    time.sleep(1)
    print('...')
    time.sleep(1)
    print(score)
    time.sleep(3)
    sys.exit()

pygame.mixer.init()
pygame.mixer.music.load('The_Insider_-_05_-_Right.mp3')
pygame.mixer.music.play()

while True:
    clock.tick(gamespeed)


    for event in pygame.event.get():

        if event.type == QUIT:
            exit()


        if event.type == KEYDOWN:
            if event.key == K_UP:
                my_direction = UP
            if event.key == K_DOWN:
                my_direction = DOWN
            if event.key == K_LEFT:
                my_direction = LEFT
            if event.key == K_RIGHT:
                my_direction = RIGHT
            if event.key == K_TAB:
                snake[0] = ((300,300))
            if event.key == K_ESCAPE:
                print(score)
                pygame.quit()
            if event.key == K_s:
                order_results()

    screen.fill((0,25,25))
    screen.blit(apple_skin,apple_pos)
    for pos in snake:
        screen.blit(snake_skin,pos)


    if my_direction == UP:
        snake[0] = (snake[0][0], snake[0][1] - blocksize)
    if my_direction == DOWN:
        snake[0] = (snake[0][0],snake[0][1] + blocksize)
    if my_direction == RIGHT:
        snake[0] = (snake[0][0] + blocksize ,snake[0][1])
    if my_direction == LEFT:
        snake[0] = (snake[0][0] - blocksize ,snake[0][1])

    if collision(snake[0], apple_pos):
        apple_pos = on_grid_random()
        snake.append((0, 0))
        gamespeed = gamespeed + 10
        score = score + 1
        pygame.mixer.Sound.play(pygame.mixer.Sound('G#.mp3'))



    for i in range(len(snake) -1,0,-1):
        snake[i] = (snake [i-1][0], snake [i-1][1])


    coord = get_coord(snake[0])
    coord_x = coord[0]
    coord_y = coord[1]

    if coord_x < 0:
        exit()

    if coord_x > screen_x - blocksize:
        exit()

    if coord_y < 0:
        exit()

    if coord_y > screen_y - blocksize:
        exit()

    pygame.display.update()

