import os
import pygame
from pygame.locals import *


def main():

    is_left_key_down = False
    is_right_key_down = False
    sprite_x_pos = 300.0
    sprite_y_pos = 400.0
    sprite_y_vel = 0.0

    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'  # center the window in the middle of the screen
    screen_size = (800, 600)  # the size of the window for our game in pixels, also known as the 'resolution'
    pygame.display.set_caption('Amazing Mario Pygame!')
    screen = pygame.display.set_mode(screen_size)

    background = pygame.Surface(screen.get_size())
    background = background.convert(screen)
    background.fill((200, 200, 255))

    original_mario_image = pygame.image.load('data/mario.png')  # load an image to use for our player sprite

    mario_sprite = pygame.sprite.Sprite()       # pygame Sprite lets us move and animate images
    mario_sprite.image = original_mario_image.copy()   # set our sprite to use the loaded image
    mario_sprite.rect = mario_sprite.image.get_rect()  # set our sprite to use the image rect as it's position rectangle
    # set the starting position of our sprite - in this case the middle of the screen
    mario_sprite.rect.bottomleft = (int(sprite_x_pos), int(sprite_y_pos))

    all_sprites = pygame.sprite.Group(mario_sprite)  # put our sprite into a Sprite Group, we could add several here

    gravity = 50.0
    mario_speed = 300.0
    mario_jump_velocity = 800.0
    
    # add some blocks for mario to walk on
    block_floor_height = 400.0
    block_num = 0
    block_image = pygame.image.load('data/block.png').convert()  # load an image
    while block_num < 20:
        block_sprite = pygame.sprite.Sprite()       
        block_sprite.image = block_image            
        block_sprite.rect = block_image.get_rect()
        block_sprite.rect.bottom = 448
        block_sprite.rect.left = block_num * 48
        block_num += 1
        all_sprites.add(block_sprite)

    # create a clock to track the frame rate
    clock = pygame.time.Clock()
    # ----------------
    # The game loop
    # ----------------
    running = True  
    while running:
        # make sure the game doesn't run faster than 60FPS
        # and get the 'time delta' which we can use to make movements
        # smooth even if the frame rate changes
        time_delta = clock.tick(60)/1000

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:  # this tests if *any* key has been pressed down this loop round of the game
                if event.key == K_LEFT:  # this tests if the key pressed down is the left arrow
                    is_left_key_down = True
                    mario_sprite.image = pygame.transform.flip(original_mario_image, True, False)
                if event.key == K_RIGHT:
                    is_right_key_down = True
                    mario_sprite.image = original_mario_image

                if event.key == K_SPACE:
                    if sprite_y_pos == block_floor_height:
                        sprite_y_vel = (-mario_jump_velocity * time_delta)
                        sprite_y_pos = block_floor_height - 0.2  # lift mario off the ground a little
                        
            elif event.type == KEYUP:  # this tests if *any* key on the keyboard has been released this loop
                if event.key == K_LEFT:  # this tests if the released key is the left arrow
                    is_left_key_down = False
                if event.key == K_RIGHT:
                    is_right_key_down = False

        # Do the actual sprite movement
        # left and right
        if is_left_key_down:
            sprite_x_pos -= (mario_speed * time_delta)
            # check we haven't moved past the edge of the screen
            if sprite_x_pos < 0:
                sprite_x_pos = 0
                
            mario_sprite.rect.left = int(sprite_x_pos)
        if is_right_key_down:
            sprite_x_pos += (mario_speed * time_delta)
            if sprite_x_pos > screen_size[0] - mario_sprite.rect.width:
                sprite_x_pos = screen_size[0] - mario_sprite.rect.width
            mario_sprite.rect.left = int(sprite_x_pos)

        # jumping movement
        # if our player sprite is in the air we apply gravity to it
        if sprite_y_pos < block_floor_height:
            sprite_y_vel += (gravity * time_delta)  # gravity
        else:
            # if our sprite has fallen back to the ground, stop it from falling
            sprite_y_pos = block_floor_height
            sprite_y_vel = 0.0

        sprite_y_pos += sprite_y_vel
        mario_sprite.rect.bottom = int(sprite_y_pos)

        all_sprites.update()
        screen.blit(background, (0, 0))  # draw the background
        all_sprites.draw(screen)  # draw all our sprites
        pygame.display.flip()  # flip all our drawn stuff onto the screen

    pygame.quit()  # exited game loop so quit pygame


if __name__ == '__main__':
    main()
