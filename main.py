import pygame
import time
import random

pygame.mixer.init()
pygame.font.init()

# Size of the screen
WIDTH, HEIGHT = (1370, 705)

# Displaying the gui windows
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Peaky Invaders")
pygame.display.set_icon(pygame.image.load('icon.png'))

VELOCITY = 10   # Velocity of my ship
FPS = 60        # Main loop will iterate at this many Frames per second

# Images for background and other different characters
BG = pygame.transform.scale(pygame.image.load("galaxy2.jfif"), (WIDTH, HEIGHT))
KNIFE = pygame.transform.scale(pygame.image.load("knife.png"), (100, 100))
MYSHIP = pygame.transform.scale(pygame.image.load("ufo.png"), (100, 100))
ENEMY_SHIP = pygame.transform.scale(pygame.image.load("ufoalien.png"), (100, 100))
ROCKET = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("bullet.png"), (40, 40)), 225)
BULLET = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("fire.png"), (20, 20)), 90)

ENEMY_HIT = pygame.USEREVENT + 1
MYSHIP_HIT = pygame.USEREVENT + 2

BULLET_HIT = pygame.mixer.Sound("collision.wav")
BULLET_HIT.set_volume(1)

ALGERIAN = pygame.font.SysFont('algerian', 40)
GAMEFONT = pygame.font.SysFont('Bauhaus 93', 100)

def main():
    myShip = pygame.Rect(680, HEIGHT - 145, 100, 100)

    music = pygame.mixer.Sound("RedRight.wav")
    gameoverMusic = pygame.mixer.Sound('gameover_music.wav')
    gameover = pygame.mixer.Sound('gameover.wav')
    gameover.set_volume(.7)

    music.play()
    
    # Initiates current time (My perception ☹)
    t = time.time()

    clock  = pygame.time.Clock()
    my_bullets, my_raaket, enemy_list = [], [], []
    
    first20sec = [100, 300, 500]
    second20sec = [100, 200, 300, 400, 500]
    tillEnd = list(range(100, 600, 50))

    var_time = 0
    kills = 0
    knife = False
    knifeTime = 0.0

    run = True
    while run:
        knife_rect = pygame.Rect((myShip.x - myShip.width, myShip.y),(100, 100))
        knife_rect2 = pygame.Rect((myShip.x + myShip.width, myShip.y),(100, 100))
        clock.tick(FPS)

        # New enemy apearance
        if time.time() - t > 3 + var_time:
            enemy = pygame.Rect(random.randint(2,WIDTH-102), 0, 100, 100)
            enemy_list.append(enemy)

            if time.time()-t < 40:
                var_time += 3
            elif time.time()-t < 60:
                var_time += 2
            else:
                var_time += 1

        # Enemy fires here
        for enemy in enemy_list:
            if (time.time() - t > 40 and enemy.y + enemy.height in tillEnd) or (time.time() - t < 20 and enemy.y + enemy.height in first20sec) or (time.time() - t > 20 and time.time() - t < 40 and enemy.y + enemy.height in second20sec):
                raaket = pygame.Rect(enemy.x + enemy.width/2 - 30, enemy.y + enemy.height - 30, 40, 40)
                my_raaket.append(raaket)

        for event in pygame.event.get():

            # Quit if closed
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:

                # New Bullets fired here
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(myShip.x + 5, myShip.y, 20, 20)
                    bullet2 = pygame.Rect(myShip.x + myShip.width - 25, myShip.y, 20, 20)
                    my_bullets.append((bullet,bullet2))

                # Hidden Knife
                if event.key == pygame.K_c:
                    knife = True
                    knifeTime = time.time()-t

            pressing_key = pygame.key.get_pressed()

            if event.type == ENEMY_HIT:
                kills += 1

            if event.type == MYSHIP_HIT:
                music.fadeout(3000)
                gameoverMusic.play()
                gameover.play()
                fin_kills = GAMEFONT.render("Kills: " + str(kills), 1, (255,255,0))
                fin_over = GAMEFONT.render("Game Over!", 1, (255,255,0))
                WIN.blit(fin_kills, (WIDTH/2-fin_kills.get_width() + 140,HEIGHT/2 - 50))
                WIN.blit(fin_over, (WIDTH/2-fin_kills.get_width() + 30,HEIGHT/2 - 200))
                pygame.display.update()
                pygame.time.delay(5000)
                run = False

        if time.time() - t - knifeTime >= .1:
            knife = False

        main_display(myShip, my_bullets, my_raaket, enemy_list, knife, knife_rect, knife_rect2, kills)
        handle_movements_of_myShip(myShip, pressing_key)


    pygame.quit()

def handle_movements_of_myShip(myShip, pressing_key):
    # Moving Left
    if pressing_key[pygame.K_LEFT] and myShip.x > 5:
        myShip.x -= VELOCITY
    # Moving Right
    if pressing_key[pygame.K_RIGHT] and myShip.x < WIDTH - 105:
        myShip.x += VELOCITY
    # Moving Up
    if pressing_key[pygame.K_UP] and myShip.y > 300:
        myShip.y -= VELOCITY
    # Moving Down
    if pressing_key[pygame.K_DOWN] and myShip.y < HEIGHT - 115:
        myShip.y += VELOCITY

def main_display(myShip, my_bullets, my_raaket, enemy_list, knife, knife_rect, knife_rect2, kills):
    WIN.blit(BG, (0, 0))
    kills_text = ALGERIAN.render("Kills: " + str(kills), 1, (255,255,255))
    WIN.blit(kills_text, (10, 0))
    if knife:
        WIN.blit(KNIFE, knife_rect)
        WIN.blit(KNIFE, knife_rect2)

        for enemy in enemy_list:
            if knife_rect.colliderect(enemy) or knife_rect2.colliderect(enemy):
                BULLET_HIT.play()
                enemy_list.remove(enemy)
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
        


    WIN.blit(MYSHIP, (myShip.x, myShip.y))
    
    for enemy in enemy_list:
        g = random.choice([-5,-4,-3,-2,-1,1,2,3,4,5])
        WIN.blit(ENEMY_SHIP, (enemy.x, enemy.y))

        # (Bug here) Deal with the enemy going out of boundry
        
        enemy.y += 1    # Move down
        enemy.x += g    # vibratory motion

        if enemy.colliderect(myShip):
            pygame.event.post(pygame.event.Event(MYSHIP_HIT))

        # Remove enemy after it gets out of the screen boundary
        if enemy.y > HEIGHT:
            enemy_list.remove(enemy)


    # -------- Bullet handling upahead -------- #  
    
    for (bullet,bullet2) in my_bullets:
        WIN.blit(BULLET, (bullet.x, bullet.y))
        WIN.blit(BULLET, (bullet2.x, bullet2.y))

        bullet.y -= 10
        bullet2.y -= 10
        
        # Remove bullets if they get out of the screen boundary
        if bullet.y < 0:
            my_bullets.remove((bullet,bullet2))
            continue

        # Bullets collided with the enemy ship will be removed
        for enemy in enemy_list:
            if bullet.colliderect(enemy) or bullet2.colliderect(enemy):
                BULLET_HIT.play()
                my_bullets.remove((bullet,bullet2))
                enemy_list.remove(enemy)
                pygame.event.post(pygame.event.Event(ENEMY_HIT))
                break


    for rocket in my_raaket:
        WIN.blit(ROCKET, (rocket.x, rocket.y))
        rocket.y += 5

        if rocket.y > HEIGHT  or myShip.colliderect(rocket):
            my_raaket.remove(rocket)

        if myShip.colliderect(rocket):
            pygame.event.post(pygame.event.Event(MYSHIP_HIT))

    # ------------- Bullets Handled ------------ #

    pygame.display.update()

main()