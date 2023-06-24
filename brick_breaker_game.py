import pygame
import sys
import random, math

class Ball(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.x = 300
        self.y = 350
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.angles= [-0.7,-0.5,-0.3, 0.3, 0.5, 0.7]
        self.angle = random.choice(self.angles)
        self.speed = 2
        
    def collision(self, group):
        global score
        self.collide_brick = pygame.sprite.groupcollide(group, brick_group, False, True)
        tollerance = self.speed +5

        if len(self.collide_brick) > 0:
            for i in self.collide_brick:
                score += self.collide_brick[i][0].points
                if abs(self.rect.top - self.collide_brick[i][0].rect.bottom) < tollerance:
                    self.rect.top = self.collide_brick[i][0].rect.bottom
                    self.angle = math.pi - self.angle
                if abs(self.rect.bottom - self.collide_brick[i][0].rect.top) < tollerance:
                    self.rect.bottom = self.collide_brick[i][0].rect.top
                    self.angle = math.pi - self.angle
                if abs(self.rect.right - self.collide_brick[i][0].rect.left) < tollerance:
                    self.rect.right = self.collide_brick[i][0].rect.left
                    self.angle = 2*math.pi - self.angle
                if abs(self.rect.left - self.collide_brick[i][0].rect.right) < tollerance:
                    self.rect.left = self.collide_brick[i][0].rect.right
                    self.angle = 2*math.pi - self.angle

        self.collide_bar = pygame.sprite.groupcollide(group, bar_group, False, False)
        if len(self.collide_bar) > 0:
            for sprite in self.collide_bar:
                if abs(self.rect.bottom - self.collide_bar[sprite][0].rect.top) < tollerance:
                    sprite.rect.bottom = self.collide_bar[sprite][0].rect.top
                    sprite.angle = math.pi - self.angle

        self.rect.x += self.speed * math.sin(self.angle)
        self.rect.y -= self.speed * math.cos(self.angle)

    def movement(self):
      global counter

      if self.rect.left <= 6 or self.rect.right >= win_width-6: 
            self.angle = 2*math.pi - self.angle
            
      if self.rect.top <= 6: self.angle = math.pi - self.angle

      if self.rect.bottom >= win_height-5:
            counter -= 1
            ball.speed = 2
            ball.image = pygame.image.load("PNG/ball.png").convert_alpha()
            #ball.rect = self.image.get_rect(midbottom = (self.x, self.y)) 
            pygame.time.delay(300)
            self.rect.midbottom = (self.x,self.y)
            self.angle = random.choice(self.angles)

      self.rect.x += self.speed * math.sin(self.angle)
      self.rect.y -= self.speed * math.cos(self.angle)

    def update(self):
        self.movement()
        self.collision(ball_group)



class ExtraBall(Ball): 
    def __init__(self, picture_path, x, y):
        super().__init__(picture_path) 
        self.rect.x = x
        self.rect.y = y
        self.angles= [-0.6,-0.5,-0.3, -0.2, 0.2,0.3, 0.4, 0.5, 0.6]
        self.angle = random.choice(self.angles)
        
    def fall(self):
        if self.rect.bottom >= win_height-5:
             pygame.sprite.Sprite.remove(self, extra_balls_group)

    def update(self):
        self.movement()
        self.collision(extra_balls_group)
        self.fall()



class BallContainer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.uniform(40, win_width-40)
        self.y = 50
        self.image = pygame.image.load("PNG/ball_container.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.speed = 2
        
    def movement(self):
        self.rect.y += self.speed
        if self.rect.bottom >= win_height-5:
            pygame.sprite.Sprite.remove(self, ball_container_group) 

    def catch(self):
       tollerance = self.speed +5
       self.collide_bar = pygame.sprite.groupcollide(ball_container_group, bar_group, True, False)
       if len(self.collide_bar) > 0:
            for i in self.collide_bar:
                if abs(self.rect.bottom - self.collide_bar[i][0].rect.top) < tollerance:
                    for _ in range(3):
                        self.extra_ball = ExtraBall("PNG/ball_extra.png", self.rect.x, self.rect.y)
                        extra_balls_group.add(self.extra_ball) 

    def update(self):
        self.movement()
        self.catch()
        








class FastBall(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = random.uniform(40, win_width-40)
        self.y = 50
        self.image = pygame.image.load("PNG/fast_container.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        self.speed = 2

    def catch(self):
       tollerance = self.speed +5
       self.collide_fast_bar = pygame.sprite.groupcollide(fast_ball_group, bar_group, True, False)
       if len(self.collide_fast_bar) > 0:
           ball.speed += 2 
           ball.image = pygame.image.load("PNG/fireball.png").convert_alpha()
           pygame.sprite.Sprite.remove(self, fast_ball_group)
 
    def movement(self):
        self.rect.y += self.speed
        if self.rect.bottom >= win_height-5:
            pygame.sprite.Sprite.remove(self, fast_ball_group) 

    

    def update(self):
        self.movement()
        self.catch()
 




class Brick(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, points):
        super().__init__()
        self.image = pygame.image.load(picture_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)
        self.points = points



class Bar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 300
        self.y = 450
        bar_3_balls = pygame.image.load("PNG/bar3.png").convert_alpha()
        bar_2_balls = pygame.image.load("PNG/bar2.png").convert_alpha()
        bar_1_ball = pygame.image.load("PNG/bar1.png").convert_alpha()
        bar_0_ball = pygame.image.load("PNG/bar0.png").convert_alpha()

        self.balls_nb = [bar_3_balls, bar_2_balls, bar_1_ball, bar_0_ball]
        self.image = pygame.image.load("PNG/bar3.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (self.x,self.y))

    def bar_image(self):
        global counter
        if counter == 3: self.image = self.balls_nb[0]
        if counter == 2: self.image = self.balls_nb[1]
        if counter == 1: self.image = self.balls_nb[2]
        if counter == 0:
            self.image = self.balls_nb[3]
            self.rect = self.image.get_rect(midbottom = (self.x,self.y))

    def movement(self):
        if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.right < win_width-15:
            self.rect.x += 10
        elif pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.left > 10:
            self.rect.x -= 10   

    def update(self):
        self.movement()
        self.bar_image()








def brick_line(group, brick_file, brick_nb, col, row, points):
    i = 0
    brick_width = 51

    for brick in range(brick_nb):
        new_brick = Brick(brick_file, col+i, row, points)
        i= i+ brick_width
        group.add(new_brick)


def brickwall_lev_1():
    brick_colors = ["PNG/brick_red.png"] #,"PNG/brick_blue.png","PNG/brick_yellow.png"]                  
    nb_of_bricks = [ 12] #, 11, 12]
    first_brick_x = [ 10] #, 35, 10]
    points = 30
    brick_height = 8

    for color, number, x in zip(brick_colors, nb_of_bricks, first_brick_x):
        brick_line(brick_group_lev_1 , color, number, x, brick_height, points)
        brick_height += 26
        points -= 10


def brickwall_lev_2():
    brick_colors = ["PNG/brick_yellow.png"]#,"PNG/brick_green.png"]#,"PNG/brick_blue.png",
                   # "PNG/brick_yellow.png", "PNG/brick_purple.png"]
    nb_of_bricks = [ 12]#, 11]# , 12, 11, 12]
    first_brick_x = [ 10]#, 35]#, 10, 35, 10]
    points = 50
    brick_height = 8

    for color, number, x in zip(brick_colors, nb_of_bricks, first_brick_x):
        brick_line(brick_group_lev_2 , color, number, x, brick_height, points)
        brick_height += 26
        points -= 10





        

class Button(pygame.sprite.Sprite):
    def __init__(self, image_path, pos):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (pos)
       
    

class GameStage():
    def __init__(self):
        self.last_level = 2
        self.level_nb = 0

    def counting(self):
        global level, brick_group, brick_group_lev_1, brick_group_lev_2

        pygame.mouse.set_visible(False) 
        ball.rect.x, ball.rect.y  = 300, 350
        ball.angle = random.choice(ball.angles)
        ball.speed = 2
        ball.image = pygame.image.load("PNG/ball.png").convert_alpha()

        extra_balls_group.empty()
        fast_ball_group.empty()
        ball_container_group.empty()

        bar.rect.x , bar.rect.y = 260, 430

        count_lev_1 = ["PNG/count_lev1_3.png", "PNG/count_lev1_2.png","PNG/count_lev1_1.png"] 
        count_lev_2 = ["PNG/count_lev2_3.png", "PNG/count_lev2_2.png","PNG/count_lev2_1.png"]
##        count_3 = pygame.image.load("PNG/count3.png").convert_alpha()
##        count_2 = pygame.image.load("PNG/count2.png").convert_alpha()
##        count_1 = pygame.image.load("PNG/count1.png").convert_alpha()
##        self.counting_nb = [count_3, count_2, count_1]

        #image = pygame.image.load("PNG/bar3.png").convert_alpha()
        if self.level_nb == 0: self.count_lev = count_lev_1
        if self.level_nb == 1: self.count_lev = count_lev_2   
        for i in range(3):
            self.image = pygame.image.load(self.count_lev[i]).convert_alpha()
            self.image.get_rect()
            win.blit(self.image, (0, 0))
            text_score = "SCORE: " + str(score)
            text_surface = game_font.render(text_score,False,(0, 255,0))
            pygame.time.wait(1000)
            win.blit(text_surface, (30,465)) 

            pygame.display.flip()      

            if i == 2:
                pygame.time.wait(1000)
            
                if self.level_nb == 0:
                    level = "level_1"
                    brick_group = brick_group_lev_1
                    brickwall_lev_1()
                if self.level_nb == 1:
                    level = "level_2"
                    #brick_group_lev_2 = pygame.sprite.Group()
                    brick_group = brick_group_lev_2
                    brickwall_lev_2()
                    extra_balls_group.empty()
                    fast_ball_group.empty()
                    ball.speed = 2
                    ball.image = pygame.image.load("PNG/ball.png").convert_alpha()
                    #ball.rect = self.image.get_rect(midbottom = (self.x, self.y)) 
                if self.level_nb == 2:
                    level = "new_game"
                    #self.level_nb = 0
 
    def start(self):
        global level
        
        pygame.mouse.set_visible(True) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in [pygame.MOUSEBUTTONDOWN , pygame.KEYDOWN]: #or event.key == pygame.K_RETURN:
                level = "counting"

        win.blit(start_bg,(0,0))
        start_btn_group.draw(win)
        pygame.display.flip()


    def level(self):
        global counter, level, brick_group
        
        pygame.mouse.set_visible(False) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if len(brick_group)== 0:
                if level == "level_2":
                    pygame.time.wait(1000)
                    self.level_nb = 0
                    level = "new_game"
                else:
                    self.level_nb += 1
                    counter = 3
                    level = "counting"

        if counter == 0:
            pygame.time.wait(1000)
            level = "new_game"
            self.level_nb = 0

        win.blit(background,(0,0))

        rand_extra = random.randrange(500)
        if rand_extra == 1:
            ball_container = BallContainer()
            ball_container_group.add(ball_container)
    
        if level == "level_1": level_range = 800
        else: level_range = 400
        rand_fast = random.randrange(level_range)
        if rand_fast == 1:
            fast_ball = FastBall()
            fast_ball_group.add(fast_ball)

        ball_container_group.draw(win)
        ball_container_group.update()

        ball_group.draw(win)
        ball_group.update() 

        extra_balls_group.draw(win)
        extra_balls_group.update()

        fast_ball_group.draw(win)
        fast_ball_group.update()

        brick_group.draw(win)
        brick_group.update() 

        text_score = "SCORE: " + str(score)
        text_surface = game_font.render(text_score, False,(0, 255,0))
        win.blit(text_surface, (30,465))

        bar_group.draw(win)
        bar_group.update()

        pygame.display.flip()
    

    def new_game(self):
        global counter, score, level

        pygame.mouse.set_visible(True) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: #.KEYDOWN:
                    pygame.quit()
                    sys.exit()
                if event.key in [ pygame.K_RETURN, pygame.K_KP_ENTER]: #.KEYDOWN:
                    level = "counting"
                    counter = 3
                    score = 0
                    self.level_nb = 0 
            if newgame_btn.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                level = "counting"
                counter = 3
                score = 0
                self.level_nb = 0 
            if exit_btn.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()

        win.blit(game_over_bg,(0,0))

        text_score = "SCORE: " + str(score)
        text_surface = game_font.render(text_score,False,(0, 255,0))
        win.blit(text_surface, (250,150))

        
        newgame_btn_group.draw(win)
        exit_btn_group.draw(win)

        pygame.display.flip()


    def set_game_level(self):
        global counter, level

        if level == "start":
           self.start()
        elif level == "counting":
           self.counting()
        elif level in ["level_1", "level_2"]:
           self.level()
        elif level == "new_game":
           self.new_game()



#-------START------------

pygame.init()

clock = pygame.time.Clock()
level = "start"
counter = 3
score = 0

win_width = 630
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Brick Breaker')
icon = pygame.image.load('PNG/icon.png')
pygame.display.set_icon(icon)

game_font = pygame.font.Font('PNG/squaredance10.ttf',24)

##cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
##pygame.mouse.set_cursor(cursor)

start_bg = pygame.image.load("PNG/start.png").convert_alpha()
background = pygame.image.load("PNG/tlo.png").convert_alpha()
game_over_bg = pygame.image.load("PNG/game_over.png").convert_alpha()

start_btn = Button("PNG/start_button.png",(310,300))
start_btn_group = pygame.sprite.GroupSingle()
start_btn_group.add(start_btn)

newgame_btn = Button("PNG/new_game_button.png", (300, 350))
newgame_btn_group = pygame.sprite.GroupSingle()
newgame_btn_group.add(newgame_btn)

exit_btn = Button("PNG/exit_button.png", (300, 420))
exit_btn_group = pygame.sprite.GroupSingle()
exit_btn_group.add(exit_btn)

#set the mouse visibility (not visible on win screen
#pygame.mouse.set_visible(False) 

ball = Ball("PNG/ball.png")
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)

ball_container_group = pygame.sprite.Group()
extra_balls_group = pygame.sprite.Group()
fast_ball_group = pygame.sprite.Group()

brick_group_lev_1 = pygame.sprite.Group()
brickwall_lev_1()

brick_group_lev_2 = pygame.sprite.Group()
brickwall_lev_2()

brick_group = brick_group_lev_1

bar = Bar()
bar_group = pygame.sprite.GroupSingle()
bar_group.add(bar)

game_stage = GameStage()

while True:
    game_stage.set_game_level()
    clock.tick(60)
