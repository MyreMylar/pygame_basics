import os
import pygame
import random

# -------------------------------------
#
# SCROLL DOWN FOR CHALLENGE 3 & 4 !!
#           (line 232)
# ------------------------------------


class Breakout:

    def __init__(self):
        self.x_speed_init = 5
        self.y_speed_init = 5
        self.init_ball_speed = self.x_speed_init, self.y_speed_init

        self.max_lives = 5
        self.score = 0
        self.high_score = 0
        # noinspection PyArgumentList
        self.bg_colour = pygame.color.Color('#2F4F4F')

        self.screen_size = self.width, self.height = 640, 480

        pygame.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pygame.display.set_caption('Breakout')
        self.screen = pygame.display.set_mode(self.screen_size)

        self.bat = Bat(self.screen_size)

        self.ball_rects = []
        self.remove_ball_rect_list = []

        self.ball_image = pygame.image.load("data/ball.png").convert()
        self.start_ball = Ball(self.ball_image, self.screen_size, self.init_ball_speed)
        self.ball_rects.append(self.start_ball)

        self.wall = Wall()
        self.wall.build_wall(self.width)

        self.lives = self.max_lives
        self.clock = pygame.time.Clock()
        # pygame.key.set_repeat(1, 30)
        pygame.mouse.set_visible(0)  # turn off mouse pointer

        self.should_move_left = False
        self.should_move_right = False
   
    def main(self):

        running = True
        while running:

            # 60 frames per second
            time_delta = self.clock.tick(60)/1000

            # process key presses
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_LEFT:
                        self.should_move_left = True
                    if event.key == pygame.K_RIGHT:
                        self.should_move_right = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.should_move_left = False
                    if event.key == pygame.K_RIGHT:
                        self.should_move_right = False

            if self.should_move_left:
                self.bat.move_left(time_delta)

            if self.should_move_right:
                self.bat.move_right(time_delta)

            # check if bat has hit ball
            for i in range(len(self.ball_rects)):
                ball = self.ball_rects[i]
                if self.bat.bat_rect.top <= ball.ball_rect.bottom <= self.bat.bat_rect.bottom and \
                   ball.ball_rect.right >= self.bat.bat_rect.left and \
                   ball.ball_rect.left <= self.bat.bat_rect.right:
                    ball.y_speed = -ball.y_speed
                    offset = ball.ball_rect.center[0] - self.bat.bat_rect.center[0]
                    # offset > 0 means ball has hit RHS of bat                   
                    # vary angle of ball depending on where ball hits bat                      
                    if offset > 0:
                        if offset > 30:  
                            ball.x_speed = 7
                        elif offset > 23:                 
                            ball.x_speed = 6
                        elif offset > 17:
                            ball.x_speed = 5
                    else:  
                        if offset < -30:                             
                            ball.x_speed = -7
                        elif offset < -23:
                            ball.x_speed = -6
                        elif offset < -17:
                            ball.x_speed = -5
                          
                # move bat/ball
                ball.ball_rect = ball.ball_rect.move(ball.x_speed, ball.y_speed)
                if ball.ball_rect.left < 0 or ball.ball_rect.right > self.width:
                    ball.x_speed = -ball.x_speed
                if ball.ball_rect.top < 0:
                    ball.y_speed = -ball.y_speed
                if ball.x_speed < 0 and ball.ball_rect.left < 0:
                    ball.x_speed = -ball.x_speed
                if ball.x_speed > 0 and ball.ball_rect.right > self.width:
                    ball.x_speed = -ball.x_speed

                # check if ball has hit wall
                # if yes then delete brick and change ball direction
                index = ball.ball_rect.collidelist(self.wall.brick_rect)
                if index != -1: 
                    if ball.ball_rect.center[0] > self.wall.brick_rect[index].right or \
                       ball.ball_rect.center[0] < self.wall.brick_rect[index].left:
                        ball.x_speed = -ball.x_speed
                    else:
                        ball.y_speed = -ball.y_speed

                    brick_to_check = self.wall.brick_list[index]
                    if brick_to_check.is_power_up():
                        self.activate_power_up()

                    if brick_to_check.has_hits_left():
                        brick_to_check.on_hit()
                    else:  # delete brick
                        self.score += brick_to_check.get_score()
                        self.wall.brick_rect[index:index + 1] = []
                        self.wall.brick_list[index:index + 1] = []

                self.ball_rects[i] = ball

                # check if ball has gone past bat - lose a ball
                if ball.ball_rect.top > self.height:
                    self.remove_ball_rect_list.append(i)
                    
            for index in self.remove_ball_rect_list:
                self.ball_rects[index:index + 1] = []
                
            self.remove_ball_rect_list = []
            
            if self.is_last_ball():
                
                self.lives -= 1
                self.bat.set_short_bat()
                # start a new ball
                self.start_ball.x_speed = self.x_speed_init

                if random.random() > 0.5:
                    self.start_ball.x_speed = -self.start_ball.x_speed
                self.start_ball.y_speed = self.y_speed_init
                self.start_ball.ball_rect.center = self.width * random.random(), self.height / 3
                self.ball_rects.append(self.start_ball)
                
                if self.lives == 0:
                    if self.score > self.high_score:
                        self.high_score = self.score
                    
                    msg = pygame.font.Font(None, 70).render("Game Over", True, (0, 255, 255), self.bg_colour)
                    msg_rect = msg.get_rect()
                    msg_rect = msg_rect.move(self.width / 2 - (msg_rect.center[0]), self.height / 3)
                    self.screen.blit(msg, msg_rect)
                    pygame.display.flip()
                    # process key presses
                    #     - ESC to quit
                    #     - any other key to restart game
                    while running:
                        restart = False
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    running = False
                                if not (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT):                                    
                                    restart = True      
                        if restart:
                            self.screen.fill(self.bg_colour)
                            self.wall.build_wall(self.width)
                            self.lives = self.max_lives
                            self.score = 0
                            break

            self.screen.fill(self.bg_colour)
            
            string_lives = 'Lives: {:,}'.format(self.lives)
            lives_text = pygame.font.Font(None, 30).render(string_lives, True, (0, 255, 255), self.bg_colour)
            lives_text_rect = lives_text.get_rect()
            lives_text_rect = lives_text_rect.move(0, 0)
            self.screen.blit(lives_text, lives_text_rect)

            string_high = 'High: {:,}'.format(self.high_score)
            high_text = pygame.font.Font(None, 30).render(string_high, True, (0, 255, 255), self.bg_colour)
            high_text_rect = high_text.get_rect()
            high_text_rect = high_text_rect.move((self.width/2) - (high_text_rect.right/2), 0)
            self.screen.blit(high_text, high_text_rect)
            
            string_score = 'Score: {:,}'.format(self.score)
            score_text = pygame.font.Font(None, 30).render(string_score, True, (0, 255, 255), self.bg_colour)
            score_text_rect = score_text.get_rect()
            score_text_rect = score_text_rect.move(self.width - score_text_rect.right, 0)
            self.screen.blit(score_text, score_text_rect)
      
            for i in range(0, len(self.wall.brick_rect)):
                self.screen.blit(self.wall.brick_list[i].brick_image, self.wall.brick_rect[i])

            # if wall completely gone then rebuild it
            if not self.wall.brick_rect:
                self.wall.build_wall(self.width)
                self.init_ball_speed = self.x_speed_init, self.y_speed_init

                for ball_rect in self.ball_rects:
                    ball_rect.center = self.width / 2, self.height / 3

            for ball in self.ball_rects:
                self.screen.blit(ball.ball_image, ball.ball_rect)
            self.screen.blit(self.bat.bat_image, self.bat.bat_rect)
            pygame.display.flip()

        pygame.quit()

# -----------------------------------------------------------------------------
# Challenge 3
# -------------
#
# Make some changes to the activate_power_up function below so that there is a
# 50% chance of activating each power up.
#
# The second power up is activated using the 'self.start_multi_ball()' function.
# I've left it commented out below.
#
# TIPS
# -----
#
# - random.uniform(1, 100) creates a random number between 1 and 100
#
# - the if statement below makes use of the 'less than' comparison operator '<'
#   this comparison condition will return True if the random number is less than 100
# ------------------------------------------
# Challenge 4 is further down on line 423
# ------------------------------------------------------------------------------
    def activate_power_up(self):
        random_number = random.uniform(1, 100)  # this function produces a random number between 1 & 100
        if random_number < 100:
            self.bat.set_large_bat()

            # self.start_multi_ball()

    def start_multi_ball(self):
        if self.ball_rects:
            old_ball = self.ball_rects[0]
            new_ball = Ball(self.ball_image, self.screen_size, self.init_ball_speed)
            new_ball.ball_rect.center = old_ball.ball_rect.center
            new_ball.x_speed = -old_ball.x_speed
            new_ball.y_speed = -old_ball.y_speed
            self.ball_rects.append(new_ball)

    def is_last_ball(self):
        if not self.ball_rects:
            return True
        

class Ball:

    def __init__(self, ball_image, screen_size, init_speed):
        self.ball_image = ball_image
        self.ball_image.set_colorkey((255, 255, 255))
        self.ball_rect = self.ball_image.get_rect()
        self.ball_rect = self.ball_rect.move(screen_size[0] / 2, screen_size[1] / 2)
        self.x_speed = init_speed[0]
        self.y_speed = init_speed[1]
        
        
class Bat:

    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.small_bat_image = pygame.image.load("data/bat.png").convert()
        self.large_bat_image = pygame.image.load("data/long_bat.png").convert()
        self.bat_image = self.small_bat_image
        self.bat_rect = self.bat_image.get_rect()
        self.bat_rect = self.bat_rect.move((screen_size[0] / 2) - (self.bat_rect.right / 2), screen_size[1] - 20)
        self.bat_speed = 600.0

    def set_large_bat(self):
        bat_center = self.bat_rect.center
        self.bat_image = self.large_bat_image
        self.bat_rect = self.bat_image.get_rect()
        self.bat_rect.center = bat_center

    def set_short_bat(self):
        bat_center = self.bat_rect.center
        self.bat_image = self.small_bat_image
        self.bat_rect = self.bat_image.get_rect()
        self.bat_rect.center = bat_center

    def move_left(self, time_delta):
        self.bat_rect = self.bat_rect.move(-self.bat_speed * time_delta, 0)
        if self.bat_rect.left < 0:
            self.bat_rect.left = 0

    def move_right(self, time_delta):
        self.bat_rect = self.bat_rect.move(self.bat_speed * time_delta, 0)
        if self.bat_rect.right > self.screen_size[0]:
            self.bat_rect.right = self.screen_size[0]


class Brick:
    def __init__(self, brick_image):
        self.brick_image = brick_image
        self.brick_rect = self.brick_image.get_rect()
        self.brick_length = self.brick_rect.right - self.brick_rect.left
        self.brick_height = self.brick_rect.bottom - self.brick_rect.top

    def is_power_up(self):
        return False

    def has_hits_left(self):
        return False

    def on_hit(self):
        pass

    def get_score(self):
        return 100


# -----------------------------------------------------------------------
# The DoubleBrick class
#
# to create an object of this class you will need to pass in *two* images
# -----------------------------------------------------------------------
class DoubleBrick(Brick):

    def __init__(self, brick_image, double_brick_image):
        Brick.__init__(self, brick_image)
        self.brick_image = double_brick_image  
        self.normal_brick_image = brick_image 
        self.brick_rect = self.brick_image.get_rect()
        self.brick_length = self.brick_rect.right - self.brick_rect.left
        self.brick_height = self.brick_rect.bottom - self.brick_rect.top
        self.has_hits_left = True

    def is_power_up(self):
        return False

    def has_hits_left(self):
        return self.has_hits_left

    def on_hit(self):
        self.has_hits_left = False
        self.brick_image = self.normal_brick_image

    def get_score(self):
        return 200
        

class PowerUpBrick(Brick):

    def __init__(self, brick_image):
        Brick.__init__(self, brick_image)
        self.brick_image = brick_image
        self.brick_rect = self.brick_image.get_rect()
        self.brick_length = self.brick_rect.right - self.brick_rect.left
        self.brick_height = self.brick_rect.bottom - self.brick_rect.top

    def is_power_up(self):
        return True

    def has_hits_left(self):
        return False

    def on_hit(self):
        pass

    def get_score(self):
        return 100
        

class Wall:
    def __init__(self):
        # load images
        self.double_brick_image = pygame.image.load("data/double_brick.png").convert()
        self.normal_brick_image = pygame.image.load("data/brick.png").convert()
        self.power_up_brick_image = pygame.image.load("data/power_brick.png").convert()

        self.brick_rectangle = self.normal_brick_image.get_rect()
        self.brick_length = self.brick_rectangle.right - self.brick_rectangle.left
        self.brick_height = self.brick_rectangle.bottom - self.brick_rectangle.top

        self.brick_rect = []
        self.brick_list = []
           
    def build_wall(self, width):        
        x_pos = 0
        y_pos = 60
        adj = 0
        self.brick_rect = []
        self.brick_list = []
        for i in range(0, 52):
            if x_pos > width:
                if adj == 0:
                    adj = self.brick_length / 2
                else:
                    adj = 0
                x_pos = -adj
                y_pos += self.brick_height

            if i is 15 or i is 35:
                power_up_brick = PowerUpBrick(self.power_up_brick_image)
                self.brick_list.append(power_up_brick)
            else:
                # -----------------------------------------------------------------------------------
                # Challenge 4
                # -------------
                #
                # Replace all the normal bricks in the wall with DoubleBricks.
                # You may need to inspect the __init__ function of the DoubleBrick class further up.
                # ------------------------------------------------------------------------------------
                normal_brick = Brick(self.normal_brick_image)
                self.brick_list.append(normal_brick)
                
            self.brick_rect.append(self.brick_rectangle)
            self.brick_rect[i] = self.brick_rect[i].move(x_pos, y_pos)
            x_pos = x_pos + self.brick_length
    

if __name__ == '__main__':
    br = Breakout()
    br.main()
