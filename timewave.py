import time
import pygame
import timespeed
import random
import sqlite3

# Credit for shipImage thanks to MillionthVector
# link to his blog http://millionthvector.blogspot.de.
#
# Credit for heart pixel art:
# DontMind8.blogspot.com
#
# Credit for coin:
# dontmind8.blogspot.com
#
#


class Ship:
    """
    Description: This class is used for the ship
    """

    def __init__(self, x, y):
        """
        :param x: x cord for the ship
        :param y: y cord for the ship
        """
        self.shipImage = pygame.image.load('blueships.png').convert_alpha()
        if x > 0:
            self.x = x
        else:
            self.x = 0
        if y > 0:
            self.y = y
        else:
            self.y = 0

        self.width = 95
        self.height = 65
        self.velocity = 3
        self.x_center = 300
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.numHearts = 3
        self.score = 0

    def hit(self):
        self.numHearts -= 1

    def addHeart(self):
        if ship.numHearts < 6:
            ship.numHearts += 1
        else:
            pass
            # add points

    def update_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)


class PowerUp:
    """
    Description: This class creates power up objects which are objects that give some type of benefit to the player
                 for example, more life, slow down time, extra points, etc.
    """

    def __init__(self, x, y, version, image, updown):
        """
        :param x:   x cord for screen
        :param y:   y cord for screen
        :param version: type of power up. Can be either 'heart', 'hourglass', 'coin'
        :param image: the image for this power up
        :param updown: True if power up item is moving up and False if moving down
        """
        if x > 0:
            self.x = x
        else:
            self.x = 0
        if y > 0:
            self.y = y
        else:
            self.y = 0

        self.width = 32
        self.height = 32

        if version == 'hourglass':
            self.version = 'hourglass'
        elif version == 'heart':
            self.version = 'heart'
        elif version == 'coin':
            self.version = coin
        elif version == 'bullet':
            self.version = 'bullet'
        else:
            self.version = 'hourglass'

        self.image = image
        self.updown = updown
        self.hitbox = (self.x, self.y, 32, 32)

    def hit(self):
        if self.version == 'hourglass':
            pass
        elif self.version == 'coin':
            pass

    def kill(self):
        # right now just throw the guy off the screen lol
        self.x = 0
        self.y = 2000

    def update_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)

    def reset_pos(self):
        # when meteors exit screen, keep inserting more at random locations
        self.y = random.randrange(-300, screenHeight + 300)
        self.x = screenWidth + random.randrange(300, 2 * screenWidth)


class Meteor:
    def __init__(self, x, y, size, image, upDown):
        if x > 0:
            self.x = x
        else:
            self.x = 0
        if y > 0:
            self.y = y
        else:
            self.y = 0

        if size == "large":
            self.width = 146
            self.height = 143
            self.health = 5
            self.size = "large"
        elif size == "medium":
            self.width = 320
            self.height = 240
            self.health = 3
            self.size = "medium"
        else:
            self.width = 32
            self.height = 32
            self.health = 1
            self.size = "small"

        self.image = image
        self.upDown = upDown
        self.hitbox = (self.x, self.y, self.width, self.height)

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()

    def kill(self):
        self.reset_pos()

    def update_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)

    def reset_pos(self):
        # when meteors exit screen, keep inserting more at random locations
        self.y = random.randrange(-300, screenHeight + 300)
        self.x = screenWidth + random.randrange(0, screenWidth)
        self.reset_health()

    def reset_health(self):
        if self.size == "large":
            self.health = 5
        elif self.size == "medium":
            self.health = 3
        else:
            self.health = 1


class Beam:
    def __init__(self, x, y):

        if x > 0:
            self.x = x
        else:
            self.x = 0
        if y > 0:
            self.y = y
        else:
            self.y = 0

        self.width = 114
        self.height = 43
        self.hitbox = (self.x, self.y, self.width, self.height)
        self.image = beam_image

    def update_hitbox(self):
        self.hitbox = (self.x, self.y, self.width, self.height)

    def kill(self):
        # right now just throw the guy off the screen lol
        self.x = 0
        self.y = 2000
        self.update_hitbox()


def redraw(shots):
    """
    Description: this function redraws the input to the screen for everything
    """
    # screen.fill((80, 80, 80))
    screen.blit(space, (0, 0))

    # heart containers
    for i in range(ship.numHearts):
        screen.blit(heart16, (i*25+15, 15))

    # power ups
    for power in powerUps:
        screen.blit(power.image, (power.x, power.y))
        # pygame.draw.rect(screen, (255, 0, 0), power.hitbox, 2)

    # meteors
    for meteor in meteors:
        screen.blit(meteor.image, (meteor.x, meteor.y))
    # ship
    screen.blit(ship.shipImage, (ship.x, ship.y))
    # pygame.draw.rect(screen, (255, 0, 0), ship.hitbox, 2)

    for shot in shots:
        screen.blit(beam_image, (shot.x, shot.y))

    # score system
    font = pygame.font.Font('ARCADECLASSIC.TTF', 32)
    text = font.render("SCORE  " + str(ship.score), 1, (255, 255, 0))
    screen.blit(text, (15, 40))

    # title
    screen.blit(textSurf, textRect)
    pygame.display.update()


def game_over():        # source: https://pythonprogramming.net/pause-game-pygame/
    """
        Description: this function displays a game over screen when
        player runs out of hearts
    """
    # uses space image as background
    screen.blit(space, (0, 0))
    font = pygame.font.Font('ARCADECLASSIC.TTF', 64)
    text_end = font.render("GAME OVER", True, (200, 0, 0))
    rect = text_end.get_rect()
    rect.center = ((screenWidth / 2), (screenHeight / 4))
    screen.blit(text_end, rect)
    # score system
    font = pygame.font.Font('ARCADECLASSIC.TTF', 32)
    text = font.render("FINAL SCORE  " + str(ship.score), 1, (255, 255, 0))
    text_rect = text.get_rect()
    text_rect.center = ((screenWidth / 2), (screenHeight / 4) + 100)
    enter = font.render("Press    y    to  enter  score  or    n    to  quit", True, (200, 200, 200))
    enter_rect = enter.get_rect()
    enter_rect.center = ((screenWidth / 2), (screenHeight / 4) + 200)
    screen.blit(text, text_rect)
    dev = font.render("Developers ", True, (255, 255, 0))
    dev_rect = dev.get_rect()
    dev_rect.center = ((screenWidth / 2), (screenHeight / 4) + 150)
    screen.blit(dev, dev_rect)
    chelsea = font.render("Chelsea  Gary                     Peiyao     Han" , True, (255, 255, 200))
    chelsea_rect = chelsea.get_rect()
    chelsea_rect.center = ((screenWidth / 2), (screenHeight / 4) + 200)
    screen.blit(chelsea, chelsea_rect)
    ryan = font.render("Ryan    Leigh                     Myra      Mullis", True, (255, 255, 200))
    ryan_rect = ryan.get_rect()
    ryan_rect.center = ((screenWidth / 2), (screenHeight / 4) + 250)
    screen.blit(ryan, ryan_rect)
    john = font.render("John    Rawley", True, (255, 255, 200))
    john_rect = john.get_rect()
    john_rect.center = ((screenWidth / 2), (screenHeight / 4) + 300)
    screen.blit(john, john_rect)
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(died_sound)
    enter_start = time.time()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_y]:
            enter_score()
            display_leaderboard()
            pygame.quit()
            quit()
        elif keys[pygame.K_n]:
            pygame.quit()
            quit()
        # update screen

        screen.blit(space, (0, 0))
        screen.blit(text_end, rect)
        screen.blit(text, text_rect)
        screen.blit(dev, dev_rect)
        screen.blit(chelsea, chelsea_rect)
        screen.blit(ryan, ryan_rect)
        screen.blit(john, john_rect)
        if time.time() - enter_start < 1:
            screen.blit(enter, enter_rect)
        if time.time() - enter_start > 2:
            enter_start = time.time()
        pygame.display.update()
        clock.tick(15)
        
def intro_screen():
    """
        Description: this function displays which keys to press in order to play the game
    """
    screen.blit(space, (0, 0))  # same background as game play
    font = pygame.font.Font('ARCADECLASSIC.TTF', 64)
    font2 = pygame.font.Font('ARCADECLASSIC.TTF', 32)
    intro_title = font.render("Timewave   Introduction", True, (200, 0, 0))
    intro_rect = intro_title.get_rect()
    intro_rect.center = ((screenWidth / 2), (screenHeight / 4))
    screen.blit(intro_title, intro_rect)
    press_w = font2.render("Press   w   to go up", True, (200, 200, 200))
    w_rect = press_w.get_rect()
    w_rect.center = ((screenWidth / 2), (screenHeight / 4) + 50)
    screen.blit(press_w, w_rect)
    press_a = font2.render("Press   a   to  go back", True, (200, 200, 200))
    a_rect = press_a.get_rect()
    a_rect.center = ((screenWidth / 2), (screenHeight / 4) + 125)
    screen.blit(press_a, a_rect)
    press_s = font2.render("Press   s   to  go down", True, (200, 200, 200))
    s_rect = press_s.get_rect()
    s_rect.center = ((screenWidth / 2), (screenHeight / 4) + 200)
    screen.blit(press_s, s_rect)
    press_d = font2.render("Press   d   to go front", True, (200, 200, 200))
    d_rect = press_d.get_rect()
    d_rect.center = ((screenWidth / 2), (screenHeight / 4) + 275)
    screen.blit(press_d, d_rect)
    press_space = font2.render("Press   space   to shoot beam", True, (200, 200, 200))
    space_rect = press_space.get_rect()
    space_rect.center = ((screenWidth / 2) , (screenHeight / 4) + 350)
    screen.blit(press_space, space_rect)
    press_enter = font2.render("Press   enter   to play", True, (200, 0, 0))
    enter_rect = press_enter.get_rect()
    enter_rect.center = ((screenWidth / 2), (screenHeight / 4) + 425)
    screen.blit(press_enter, enter_rect)
    enter_start = time.time()

    intro = True
    while intro:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:  # If they click the Close button on the display
                pygame.quit()
                quit()

        intro_keys = pygame.key.get_pressed()
        if intro_keys[pygame.K_RETURN]:
            intro = False
            start_over()
        elif intro_keys[pygame.K_l]:
            display_leaderboard()
        elif intro_keys[pygame.K_p]:
            pause_menu()
        else:
            # update screen
            screen.blit(space, (0, 0))
            screen.blit(intro_title, intro_rect)
            screen.blit(press_w, w_rect)
            screen.blit(press_a, a_rect)
            screen.blit(press_s, s_rect)
            screen.blit(press_d, d_rect)
            screen.blit(press_space, space_rect)
            screen.blit(press_enter, enter_rect)

            if time.time() - enter_start < 1:
                screen.blit(press_enter, enter_rect)
            if time.time() - enter_start > 2:
                enter_start = time.time()
            pygame.display.update()


def title_screen():
    global run

    font = pygame.font.Font('ARCADECLASSIC.TTF', 128)
    font2 = pygame.font.Font('ARCADECLASSIC.TTF', 24)
    the_title = font.render("Timewave", True, (200, 0, 0))
    rect = the_title.get_rect()
    rect.center = ((screenWidth / 2), (screenHeight / 2))
    press_enter = font2.render("Press ENTER to play                Press i for introduction", True, (200, 200, 200))
    enter_rect = press_enter.get_rect()
    enter_rect.center = ((screenWidth / 2), (screenHeight / 2) + 100)
    enter_start = time.time()

    title = True
    while title:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:  # If they click the Close button on the display
                pygame.quit()
                quit()

        title_keys = pygame.key.get_pressed()
        if title_keys[pygame.K_RETURN]:
            title = False
        elif title_keys[pygame.K_l]:
            display_leaderboard()
        elif title_keys[pygame.K_p]:
            pause_menu()
        elif title_keys[pygame.K_i]:
            intro_screen()
        else:
            # update screen
            screen.blit(space, (0, 0))
            screen.blit(the_title, rect)

            if time.time() - enter_start < 1:
                screen.blit(press_enter, enter_rect)
            if time.time() - enter_start > 2:
                enter_start = time.time()
            pygame.display.update()


def pause_menu():
    """
        Description: this function displays a menu of options
         triggered by pressing "p" key during play
    """
    screen.blit(space, (0, 0))  # same background as game play
    font = pygame.font.Font('ARCADECLASSIC.TTF', 64)
    font2 = pygame.font.Font('ARCADECLASSIC.TTF', 32)
    the_title = font.render("Timewave", True, (200, 0, 0))
    rect = the_title.get_rect()
    rect.center = ((screenWidth / 2), (screenHeight / 3))
    screen.blit(the_title, rect)
    press_p = font.render("Paused", True, (200, 0, 0))
    p_rect = press_p.get_rect()
    p_rect.center = ((screenWidth / 2), (screenHeight / 3) + 50)
    screen.blit(press_p, p_rect)
    press_r = font2.render("Press   u   to resume", True, (200, 200, 200))
    r_rect = press_r.get_rect()
    r_rect.center = ((screenWidth / 2), (screenHeight / 3) + 125)
    screen.blit(press_r, r_rect)
    press_s = font2.render("Press   s   to  start   over", True, (200, 200, 200))
    s_rect = press_s.get_rect()
    s_rect.center = ((screenWidth / 2), (screenHeight / 3) + 200)
    screen.blit(press_s, s_rect)
    press_q = font2.render("Press   q   to  quit", True, (200, 200, 200))
    q_rect = press_q.get_rect()
    q_rect.center = ((screenWidth / 2), (screenHeight / 3) + 350)
    screen.blit(press_q, q_rect)
    press_l = font2.render("Press   l   for  leaderboard", True, (200, 200, 200))
    l_rect = press_q.get_rect()
    l_rect.center = ((screenWidth / 2) - 70, (screenHeight / 3) + 275)
    screen.blit(press_l, l_rect)
    elap = 0
    paused = True
    while paused:

        elap += 1
        pygame.mixer.music.pause()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
        # update screen
        pygame.display.update()
        clock.tick(10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_u]:
            pygame.mixer.music.unpause()
            paused = False
            return elap
        if keys[pygame.K_s]:
            pygame.mixer.music.unpause()
            start_over()
            paused = False
            return elap
            # implement starting over here
        elif keys[pygame.K_q]:
            pygame.quit()
            quit()
        elif keys[pygame.K_l]:
            display_leaderboard()
        else:
            screen.blit(space, (0, 0))  # same background as game play
            screen.blit(the_title, rect)
            screen.blit(press_p, p_rect)
            screen.blit(press_r, r_rect)
            screen.blit(press_s, s_rect)
            screen.blit(press_q, q_rect)
            screen.blit(press_l, l_rect)


def start_over():
    global beams, meteors, powerUps, ship, k, start, bullet_start, fast_bullets,slow, wait_between_hit, speed_offset
    global pause_time, slowDown, slow_hourglass, moved
    ship = Ship(300, 275)
    powerUps = [PowerUp(screenWidth + 700, 400, 'bullet', bullet_power, True),
                PowerUp(screenWidth + 800, 100, 'hourglass', hourglass, False),
                PowerUp(screenWidth + 1500, 250, 'heart', heart32, False),
                PowerUp(screenWidth + 1100, 300, 'coin', coin, True)]

    meteors = [Meteor(screenWidth + 400, 200, "small", small_meteor, True),
               Meteor(screenWidth + 845, 0, "small", small_meteor, True),
               Meteor(screenWidth + 1050, 0, "large", large_meteor, False),
               Meteor(screenWidth + 777, 333, "large", large_meteor, True),
               Meteor(screenWidth + 475, 600, "small", small_meteor, False),
               Meteor(screenWidth + 500, 300, "small", small_meteor, False),
               Meteor(screenWidth + 723, 100, "small", small_meteor, False),
               Meteor(screenWidth + 546, 60, "small", small_meteor, True),
               Meteor(screenWidth + 805, 430, "large", large_meteor, True),
               Meteor(screenWidth + 777, 333, "large", large_meteor, False),
               Meteor(screenWidth + 475, 600, "small", small_meteor, True),
               Meteor(screenWidth + 200, 350, "small", small_meteor, True)]
    beams = []

    k = 0  # k is used to add small delay to updating the movement of the ship and power ups
    start = 0
    bullet_start = 0  # used for delay between bullets
    fast_bullets = 1  # used for bullet power up
    slow = 0  # used for delay when slowing ship down
    wait_between_hit = 0
    speed_offset = 0
    pause_time = 0
    slowDown = False
    slow_hourglass = False
    moved = False


def display_leaderboard():
    font = pygame.font.Font('ARCADECLASSIC.TTF', 64)
    font2 = pygame.font.Font('ARCADECLASSIC.TTF', 32)
    the_title = font.render("Leaderboard", True, (200, 0, 0))
    rect = the_title.get_rect()
    rect.center = (screenWidth / 2, 102)
    top10 = get_top_ten()
    leader1 = font2.render('1   ' + top10[0][0], True, (200, 0, 0))
    leader1_rect = leader1.get_rect()
    leader1_rect.center = (screenWidth / 2 - 120, 160)
    leader2 = font2.render('2   ' + top10[1][0], True, (200, 0, 0))
    leader2_rect = leader1.get_rect()
    leader2_rect.center = (screenWidth / 2 - 120, 190)
    leader3 = font2.render('3   ' + top10[2][0], True, (200, 0, 0))
    leader3_rect = leader1.get_rect()
    leader3_rect.center = (screenWidth / 2 - 120, 220)
    leader4 = font2.render('4   ' + top10[3][0], True, (200, 0, 0))
    leader4_rect = leader1.get_rect()
    leader4_rect.center = (screenWidth / 2 - 120, 250)
    leader5 = font2.render('5   ' + top10[4][0], True, (200, 0, 0))
    leader5_rect = leader1.get_rect()
    leader5_rect.center = (screenWidth / 2 - 120, 280)
    leader6 = font2.render('6   ' + top10[5][0], True, (200, 0, 0))
    leader6_rect = leader1.get_rect()
    leader6_rect.center = (screenWidth / 2 - 120, 310)
    leader7 = font2.render('7   ' + top10[6][0], True, (200, 0, 0))
    leader7_rect = leader1.get_rect()
    leader7_rect.center = (screenWidth / 2 - 120, 340)
    leader8 = font2.render('8   ' + top10[7][0], True, (200, 0, 0))
    leader8_rect = leader1.get_rect()
    leader8_rect.center = (screenWidth / 2 - 120, 370)
    leader9 = font2.render('9   ' + top10[8][0], True, (200, 0, 0))
    leader9_rect = leader1.get_rect()
    leader9_rect.center = (screenWidth / 2 - 120, 400)
    leader10 = font2.render('10  ' + top10[9][0], True, (200, 0, 0))
    leader10_rect = leader1.get_rect()
    leader10_rect.center = (screenWidth / 2 - 120, 430)
    score1 = font2.render(str(top10[0][1]), True, (255, 255, 0))
    score1_rect = leader1.get_rect()
    score1_rect.center = (screenWidth / 2 + 150, 160)
    score2 = font2.render(str(top10[1][1]), True, (255, 255, 0))
    score2_rect = leader1.get_rect()
    score2_rect.center = (screenWidth / 2 + 150, 190)
    score3 = font2.render(str(top10[2][1]), True, (255, 255, 0))
    score3_rect = leader1.get_rect()
    score3_rect.center = (screenWidth / 2 + 150, 220)
    score4 = font2.render(str(top10[3][1]), True, (255, 255, 0))
    score4_rect = leader1.get_rect()
    score4_rect.center = (screenWidth / 2 + 150, 250)
    score5 = font2.render(str(top10[4][1]), True, (255, 255, 0))
    score5_rect = leader1.get_rect()
    score5_rect.center = (screenWidth / 2 + 150, 280)
    score6 = font2.render(str(top10[5][1]), True, (255, 255, 0))
    score6_rect = leader1.get_rect()
    score6_rect.center = (screenWidth / 2 + 150, 310)
    score7 = font2.render(str(top10[6][1]), True, (255, 255, 0))
    score7_rect = leader1.get_rect()
    score7_rect.center = (screenWidth / 2 + 150, 340)
    score8 = font2.render(str(top10[7][1]), True, (255, 255, 0))
    score8_rect = leader1.get_rect()
    score8_rect.center = (screenWidth / 2 + 150, 370)
    score9 = font2.render(str(top10[8][1]), True, (255, 255, 0))
    score9_rect = leader1.get_rect()
    score9_rect.center = (screenWidth / 2 + 150, 400)
    score10 = font2.render(str(top10[9][1]), True, (255, 255, 0))
    score10_rect = leader1.get_rect()
    score10_rect.center = (screenWidth / 2 + 150, 430)

    press_enter = font2.render("Press Backspace to return", True, (200, 200, 200))
    enter_rect = press_enter.get_rect()
    enter_rect.center = ((screenWidth / 2) - 15, screenHeight - 100)
    enter_start = time.time()

    title = True
    while title:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:  # If they click the Close button on the display
                pygame.quit()
                quit()

        title_keys = pygame.key.get_pressed()
        if title_keys[pygame.K_BACKSPACE]:
            title = False
        else:
            # update screen
            screen.blit(space, (0, 0))
            screen.blit(the_title, rect)
            screen.blit(leader1, leader1_rect)
            screen.blit(leader2, leader2_rect)
            screen.blit(leader3, leader3_rect)
            screen.blit(leader4, leader4_rect)
            screen.blit(leader5, leader5_rect)
            screen.blit(leader6, leader6_rect)
            screen.blit(leader7, leader7_rect)
            screen.blit(leader8, leader8_rect)
            screen.blit(leader9, leader9_rect)
            screen.blit(leader10, leader10_rect)
            screen.blit(score1, score1_rect)
            screen.blit(score2, score2_rect)
            screen.blit(score3, score3_rect)
            screen.blit(score4, score4_rect)
            screen.blit(score5, score5_rect)
            screen.blit(score6, score6_rect)
            screen.blit(score7, score7_rect)
            screen.blit(score8, score8_rect)
            screen.blit(score9, score9_rect)
            screen.blit(score10, score10_rect)

            if time.time() - enter_start < 1:
                screen.blit(press_enter, enter_rect)
            if time.time() - enter_start > 2:
                enter_start = time.time()
            pygame.display.update()


def get_top_ten():
    global cursor
    cursor.execute("SELECT * FROM Leaderboard ORDER BY score DESC LIMIT 10")
    return cursor.fetchall()


def enter_score():
    global cursor, connection
    font = pygame.font.Font('ARCADECLASSIC.TTF', 32)
    name = ""
    wait = time.time()
    msg = font.render("Enter  name  up  to  10  characters  then  press  enter ", True, (200, 0, 0))
    rect = msg.get_rect()
    rect.center = (screenWidth / 2, screenHeight / 2 - 110)
    display = True
    while display:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:  # If they click the Close button on the display
                pygame.quit()
                quit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_BACKSPACE] and len(name) > 0 and time.time() - wait > 0.20:
            name = name[:-1]
            wait = time.time()
        elif keys[pygame.K_a] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'A'
            wait = time.time()
        elif keys[pygame.K_b] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'B'
            wait = time.time()
        elif keys[pygame.K_c] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'C'
            wait = time.time()
        elif keys[pygame.K_d] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'D'
            wait = time.time()
        elif keys[pygame.K_e] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'E'
            wait = time.time()
        elif keys[pygame.K_f] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'F'
            wait = time.time()
        elif keys[pygame.K_g] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'G'
            wait = time.time()
        elif keys[pygame.K_h] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'H'
            wait = time.time()
        elif keys[pygame.K_i] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'I'
            wait = time.time()
        elif keys[pygame.K_j] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'J'
            wait = time.time()
        elif keys[pygame.K_k] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'K'
            wait = time.time()
        elif keys[pygame.K_l] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'L'
            wait = time.time()
        elif keys[pygame.K_m] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'M'
            wait = time.time()
        elif keys[pygame.K_n] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'N'
            wait = time.time()
        elif keys[pygame.K_o] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'O'
            wait = time.time()
        elif keys[pygame.K_p] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'P'
            wait = time.time()
        elif keys[pygame.K_q] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'Q'
            wait = time.time()
        elif keys[pygame.K_r] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'R'
            wait = time.time()
        elif keys[pygame.K_s] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'S'
            wait = time.time()
        elif keys[pygame.K_t] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'T'
            wait = time.time()
        elif keys[pygame.K_u] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'U'
            wait = time.time()
        elif keys[pygame.K_v] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'V'
            wait = time.time()
        elif keys[pygame.K_w] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'W'
            wait = time.time()
        elif keys[pygame.K_x] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'X'
            wait = time.time()
        elif keys[pygame.K_y] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'Y'
            wait = time.time()
        elif keys[pygame.K_z] and time.time() - wait > 0.20 and len(name) < 10:
            name += 'Z'
            wait = time.time()
        elif keys[pygame.K_0] and time.time() - wait > 0.20 and len(name) < 10:
            name += '0'
            wait = time.time()
        elif keys[pygame.K_1] and time.time() - wait > 0.20 and len(name) < 10:
            name += '1'
            wait = time.time()
        elif keys[pygame.K_2] and time.time() - wait > 0.20 and len(name) < 10:
            name += '2'
            wait = time.time()
        elif keys[pygame.K_3] and time.time() - wait > 0.20 and len(name) < 10:
            name += '3'
            wait = time.time()
        elif keys[pygame.K_4] and time.time() - wait > 0.20 and len(name) < 10:
            name += '4'
            wait = time.time()
        elif keys[pygame.K_5] and time.time() - wait > 0.20 and len(name) < 10:
            name += '5'
            wait = time.time()
        elif keys[pygame.K_6] and time.time() - wait > 0.20 and len(name) < 10:
            name += '6'
            wait = time.time()
        elif keys[pygame.K_7] and time.time() - wait > 0.20 and len(name) < 10:
            name += '7'
            wait = time.time()
        elif keys[pygame.K_8] and time.time() - wait > 0.20 and len(name) < 10:
            name += '8'
            wait = time.time()
        elif keys[pygame.K_9] and time.time() - wait > 0.20 and len(name) < 10:
            name += '9'
            wait = time.time()
        elif keys[pygame.K_RETURN] and time.time() - wait > 0.20 and len(name) > 0:
            cursor.execute("INSERT INTO Leaderboard VALUES (? , ?)", (name,ship.score))
            connection.commit()
            display = False
        # update screen

        display_name = font.render(name, True, (200, 0, 0))
        name_rect = display_name.get_rect()
        name_rect.center = (screenWidth/2, screenHeight/2)

        screen.blit(space, (0, 0))
        screen.blit(msg, rect)
        screen.blit(display_name, name_rect)
        pygame.display.update()


if __name__ == "__main__":
    connection = sqlite3.connect('leaderboard.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Leaderboard")
    print(cursor.fetchall())
    screenWidth = 1200
    screenHeight = 600
    dimensions = (screenWidth, screenHeight)
    screen = pygame.display.set_mode(dimensions)
    pygame.display.set_mode((0, 0), pygame.DOUBLEBUF)

    pygame.init()
    pygame.display.set_caption("TimeWave")
    clock = pygame.time.Clock()

    # sound and music
    bg_music = pygame.mixer.music.load("Battleship.wav")
    crash_sound = pygame.mixer.Sound("Meteor.wav")
    laser_sound = pygame.mixer.Sound("Laser_Shoot1.wav")
    died_sound = pygame.mixer.Sound("gameover.wav")
    powerup_sound = pygame.mixer.Sound("powerup.wav")
    crash_sound = pygame.mixer.Sound("Explosion.wav")

    # images
    heart16 = pygame.image.load('heart_pixel_art_16x16.png')
    heart32 = pygame.image.load('heart_pixel_art_32x32.png')
    hourglass = pygame.image.load('Hourglass.png')
    coin = pygame.image.load('money_power.png')
    background = pygame.image.load('back.png')
    beam_image = pygame.image.load('beam.png')
    bullet_power = pygame.image.load('bullet_power.png')
    space = pygame.image.load('space2.png').convert_alpha()
    large_meteor = pygame.image.load('large_brown_meteor.png').convert_alpha()
    small_meteor = pygame.image.load('small_silver_meteor.png').convert_alpha()
    arcade_font = pygame.font.Font('ARCADECLASSIC.TTF', 64)
    textSurf = arcade_font.render("TIMEWAVE", True, (200, 0, 0))
    textRect = textSurf.get_rect()
    textRect.center = (screenWidth/2, 32)

    run = True  # state of game
    pygame.mixer.music.play(-1)

    # create ship, power ups, meteors, and beams
    ship = Ship(300, 275)
    powerUps = [PowerUp(screenWidth + 700, 400, 'bullet', bullet_power, True), PowerUp(screenWidth + 800, 100, 'hourglass', hourglass, False),
                PowerUp(screenWidth + 1500, 250, 'heart', heart32, False), PowerUp(screenWidth + 1100, 300, 'coin', coin, True)]

    meteors = [Meteor(screenWidth + 400, 200, "small", small_meteor, True), Meteor(screenWidth + 845, 0, "small", small_meteor, True),
               Meteor(screenWidth + 1050, 0, "large", large_meteor, False), Meteor(screenWidth + 777, 333, "large", large_meteor, True),
               Meteor(screenWidth + 475, 600, "small", small_meteor, False), Meteor(screenWidth + 500, 300, "small", small_meteor, False),
               Meteor(screenWidth + 723, 100, "small", small_meteor, False), Meteor(screenWidth + 546, 60, "small", small_meteor, True),
               Meteor(screenWidth + 805, 430, "large", large_meteor, True), Meteor(screenWidth + 777, 333, "large", large_meteor, False),
               Meteor(screenWidth + 475, 600, "small", small_meteor, True), Meteor(screenWidth + 200, 350, "small", small_meteor, True)]
    beams = []
    k = 0  # k is used to add small delay to updating the movement of the ship and power ups
    start = 0
    bullet_start = 0        # used for delay between bullets
    fast_bullets = 1        # used for bullet power up
    slow = 0                # used for delay when slowing ship down
    wait_between_hit = 0
    speed_offset = 0
    pause_time = 0
    slowDown = False
    slow_hourglass = False
    moved = False
    score_start = time.time()
    # first draw to screen
    title_screen()
    intro_screen()
    pygame.init()
    pygame.display.set_caption("TimeWave")
    redraw(beams)
    while run:
        game_running = True
        if time.time() - score_start > 0.03:
            ship.score += 1                     # currently increases score every 30 millisecond
            score_start = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # If they click the Close button on the display
                run = False

        # Keyboard Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            pause_time += pause_menu()
        if keys[pygame.K_w] and ship.y > 5:  # Key: w    :   Move Ship Up
            ship.y -= 4
            moved = True
            ship.update_hitbox()

        if keys[pygame.K_s] and ship.y < screenHeight - 69:  # key: s    :   Move ship down
            ship.y += 4
            moved = True
            ship.update_hitbox()
        if keys[pygame.K_SPACE] and time.time() - start > 0.35 / fast_bullets:
            start = time.time()

            end_time = pygame.time.get_ticks() + 300 # 300 millisconds = 0.3 seconds
            #beams.append( (end_time, Beam(ship.x + 25, ship.y + 16)) )

            beams.append(Beam(ship.x + 25, ship.y + 16))
            pygame.mixer.Sound.play(laser_sound)
        if keys[pygame.K_a]:  # key: a    :   Slow down
            moved = True
            if ship.x > 20:  # move the ship back a little of time until a defined distance
                slowDown = False
                ship.x -= ship.velocity
                ship.update_hitbox()

        if keys[pygame.K_d]:  # key: a    :   Slow down
            moved = True
            if ship.x < ship.x_center:  # and move ship closer to center over time if not at center
                ship.x += ship.velocity
                ship.update_hitbox()

        wait = 12       # small break between iterations
        temp_x, temp_y = timespeed.progression(pygame.time.get_ticks()-pause_time, speed_offset)  # speeding up time
        if temp_x < 0:
            speed_offset += timespeed.movespeed(moved)
        moved = False
        if k == wait:
            k = 0       # reset break
            for power in powerUps:
                if power.updown:  # if power up item is moving up
                    power.y -= temp_y
                    power.hitbox = (power.x, power.y, 32, 32)
                    if power.y < 5:  # begin to move down when at top of screen
                        power.updown = False
                else:  # else power up item is moving down
                    power.y += temp_y
                    power.hitbox = (power.x, power.y, 32, 32)
                    if power.y > screenHeight - 32:  # begin to move up if at bottom of screen
                        power.updown = True

                if slowDown or slow_hourglass:  # move all the power up items slower

                    power.x -= temp_x / 2
                    power.hitbox = (power.x, power.y, 32, 32)

                else:
                    power.x -= temp_x  # else move at normal pace
                    power.hitbox = (power.x, power.y, 32, 32)

            # move the meteors
            for meteor in meteors:
                if meteor.upDown:
                    meteor.y -= temp_y
                    meteor.update_hitbox()
                    if meteor.y < 0:
                        meteor.upDown = False
                else:
                    meteor.y += temp_y
                    meteor.update_hitbox()
                    if meteor.y > screenHeight - meteor.height:
                        meteor.upDown = True

                if slowDown or slow_hourglass:  # move all meteors slower
                    meteor.x -= temp_x / 2
                    meteor.update_hitbox()

                else:
                    meteor.x -= temp_x  # else move at normal pace
                    meteor.update_hitbox()

                # reset meteor if it goes off the screen
                if meteor.x + meteor.width < 0:
                    meteor.reset_pos()
        # power up hit detection
        for power in powerUps:
            if power.y < ship.y + 65 and power.y + 32 > ship.y:
                if power.x + 16 < ship.x + 95 and power.x + 32 > ship.x:
                    power.hit()
                    pygame.mixer.Sound.play(powerup_sound)
                    # these two are easier to handle outside of class
                    if power.version == 'heart':
                        ship.addHeart()
                        pygame.mixer.Sound.play(powerup_sound)
                    elif power.version == 'bullet':
                        fast_bullets = 2
                        bullet_start = time.time()
                        pygame.mixer.Sound.play(powerup_sound)
                    elif power.version == 'hourglass':
                        slow_hourglass = True
                        hour_start = time.time()
                        speed_offset = timespeed.slowdown(speed_offset)
                        pygame.mixer.Sound.play(powerup_sound)
                    elif power.version == 'coin':
                        ship.score += 4000
                        pygame.mixer.Sound.play(powerup_sound)
                    power.reset_pos()

            if power.x + power.width < 0:
                power.reset_pos()

        # meteor and beam hit detection
        for meteor in meteors:
            if meteor.y < ship.y + ship.height and meteor.y + meteor.height > ship.y:
                if meteor.x < ship.x + ship.width and meteor.x + meteor.height > ship.x:
                    if time.time() - wait_between_hit > 2 or wait_between_hit == 0:
                        meteor.kill()
                        ship.hit()
                        pygame.mixer.Sound.play(crash_sound)
                        if meteor.size == 'small':
                            ship.score -= 1000
                        else:
                            ship.score -= 3000
                        wait_between_hit = time.time()

            for beam in beams:
                if meteor.y < beam.y + beam.height and beam.y + meteor.height > beam.y:
                    if meteor.x < beam.x + beam.width and meteor.x + meteor.height > beam.x:
                        meteor.hit()
                        beams.remove(beam)
                        if meteor.size == 'small':
                            ship.score += 1000
                        else:
                            ship.score += 3000
            for beam in beams:
                if beam.x > screenWidth:
                    beams.remove(beam)

        if start != 0 and time.time() - bullet_start > 10:
            fast_bullets = 1

        k += 1
        redraw(beams)  # redraw the screen
        
        # if you have no hearts then the game is over
        if ship.numHearts == 0:
            game_over()          # game over screen appears
            run = False

        # move bullets over by one
        for shot in beams:
            shot.x += 2
            for beam in beams:
                if shot.x > 500:
                    beams.remove(beam)

        if slow_hourglass and time.time() - hour_start > 15:
            slow_hourglass = False

    pygame.quit()
