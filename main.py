import pygame
import pygame.mixer
import random
import time
import sys

# Initialize all pygame modules
pygame.init()

# Game window setup
window_width = 500
window_height = 500
window_screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game by Shade')

# Colors
# RGB tuples
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
pink = (231, 97, 247)

# Clock object for FPS
fps = pygame.time.Clock()
 
# Game Elements
# Snake body (first 3 blocks)
snake_body = [[100, 50], [90, 50], [80, 50]]
# Default snake position
snake_position = [100, 50]
# Increase/Decrease the number of px per movement
snake_movement = 10
# Default snake direction
direction = 'RIGHT'
next_direction = direction
# Snake speed
difficulty = 20
# Fruit spawn
fruit_spawn = True
# fruit position
fruit_position = [random.randrange(1, (window_width//10)) * 10,
				random.randrange(1, (window_height//10)) * 10]
# Initial Score
score = 0

# Load the main menu images
menu_background = pygame.image.load('res/MenuBackground.png')
menu_apples = pygame.image.load('res/MenuApples.png')
menu_clouds = pygame.image.load('res/MenuClouds.png')
menu_enter = pygame.image.load('res/MenuEnter.png')
menu_title = pygame.image.load('res/MenuTitle.png')

# Scale down the main menu images
# 951 x 951 px original size
menu_scale_factor = min(window_width / 951, window_height / 951)

menu_background = pygame.transform.scale(menu_background, (window_width, window_height))
menu_apples = pygame.transform.scale(menu_apples, (int(951 * menu_scale_factor), int(951 * menu_scale_factor)))
menu_clouds = pygame.transform.scale(menu_clouds, (int(951 * menu_scale_factor), int(951 * menu_scale_factor)))
menu_enter = pygame.transform.scale(menu_enter, (int(951 * menu_scale_factor), int(951 * menu_scale_factor)))
menu_title = pygame.transform.scale(menu_title, (int(951 * menu_scale_factor), int(951 * menu_scale_factor)))

# Center the main menu images on the screen
menu_apples_rect = menu_apples.get_rect(center=(window_width//2, window_height//2))
menu_clouds_rect = menu_clouds.get_rect(center=(window_width//2, window_height//2))
menu_enter_rect = menu_enter.get_rect(center=(window_width//2, window_height//2))
menu_title_rect = menu_title.get_rect(center=(window_width//2, window_height//2))

# Load the game over images
game_over_background = pygame.image.load('res/GameOverBackground.png')
game_over_apples = pygame.image.load('res/GameOverApples.png')
game_over_text = pygame.image.load('res/GameOver.png')

# Scale down the game over images
# 951 x 951 px original size
game_over_scale_factor = min(window_width / 951, window_height / 951)

game_over_background = pygame.transform.scale(game_over_background, (window_width, window_height))
game_over_text = pygame.transform.scale(game_over_text, (int(951 * game_over_scale_factor), int(951 * game_over_scale_factor)))
game_over_apples = pygame.transform.scale(game_over_apples, (int(951 * game_over_scale_factor), int(951 * game_over_scale_factor)))

# Center the game over images on the screen
game_over_background_rect = game_over_background.get_rect(center=(window_width//2, window_height//2))
game_over_text_rect = game_over_text.get_rect(center=(window_width//2, window_height//2))
game_over_apples_rect = game_over_apples.get_rect(center=(window_width//2, window_height//2))

# Main menu function
def main_menu():
    # Load the main menu background song
    main_menu_sound = pygame.mixer.Sound('res/MainMenuSound.mp3')
    # Play the main menu background song in an infinite loop
    main_menu_sound.play(loops=-1)
    # Initial transparency value
    alpha = 255
    # The alpha change rate
    alpha_change_rate = -8
    while True:
        # Main Menu Key Events
        for event in pygame.event.get():
            # When the Enter key is pressed, start the game loop and exit the main menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                # Start the game loop
                return
            # When the Escape key is pressed, quit the game and exit the main menu
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # If the user closes the game window, quit the game and exit the main menu
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Fill the screen with black color
        window_screen.fill(black)

        # Draw the menu images
        window_screen.blit(menu_background, (0, 0))
        window_screen.blit(menu_apples, menu_apples_rect)
        window_screen.blit(menu_clouds, menu_clouds_rect)
        window_screen.blit(menu_title, menu_title_rect)

        # Adjust the MenuEnter transparency value
        alpha += alpha_change_rate
        if alpha >= 255 or alpha <= 100:
            alpha_change_rate = -alpha_change_rate

        # Set the MenuEnter transparency value
        menu_enter.set_alpha(alpha)
        window_screen.blit(menu_enter, menu_enter_rect)

        # Update the display
        pygame.display.update()

        # Set the frame rate
        fps.tick(30)

# Call the main menu function
main_menu()
# When exiting the main menu, stop the background song
pygame.mixer.stop()

# Score function
def total_score(choice, color, font, size):
    # Creates a font object
    score_font = pygame.font.Font('res/Pixel.ttf', 20)
    # Live score
    score_surface = score_font.render('Score : ' + str(score), True, color)
    # Rectangle object
    scoreRect = score_surface.get_rect()
    # Score surface and rectangle will be drawn
    window_screen.blit(score_surface, scoreRect)

# Game Over function
def game_over():
    # Draw the game over images
    window_screen.blit(game_over_background, (0, 0))
    window_screen.blit(game_over_text, game_over_text_rect)
    window_screen.blit(game_over_apples, game_over_apples_rect)
    # Render the score text
    font = pygame.font.Font('res/Pixel.ttf', 20)
    text = font.render(f"Score : {score}", True, white)
    text_rect = text.get_rect(center=(window_width//2, window_height//2 + 100))
    window_screen.blit(text, text_rect)
    # Load the sound file
    game_over_sound = pygame.mixer.Sound('res/GameOverSound.mp3')
    # Play the sound
    game_over_sound.play()
    # Print the score
    print(f"Score: {score}")
    # Update the display
    pygame.display.update()
    # Wait for 3 seconds before quitting
    time.sleep(3)
    # Quit pygame and terminate the script
    pygame.quit()
    sys.exit()

# Key events function
def key_events():
    global next_direction
    # Arrow keys and WASD keys
    # ESC to exit
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                next_direction = 'UP'
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                next_direction = 'DOWN'
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                next_direction = 'LEFT'
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                next_direction = 'RIGHT'
            elif event.key in (pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

# Direction management function
def manage_direction():
    global direction, next_direction
    if next_direction == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif next_direction == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif next_direction == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif next_direction == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

# Snake movement function
def move_snake():
    global direction, snake_position, snake_body, fruit_position, fruit_spawn, score
    # snake_movement = 10
    # Y - coordinate decreases by 10px
    if direction == 'UP':
        snake_position[1] -= snake_movement
    # Y - coordinate increases by 10px
    elif direction == 'DOWN':
        snake_position[1] += snake_movement
    # X - coordinate decreases by 10px
    elif direction == 'LEFT':
        snake_position[0] -= snake_movement
    # X - coordinate increases by 10px
    elif direction == 'RIGHT':
        snake_position[0] += snake_movement

    # Snake body growing mechanism
	# if fruits and snakes collide then scores
	# will be incremented by 10
    snake_body.insert(0, list(snake_position))
    if (abs(snake_position[0] - fruit_position[0]) < 10) and (abs(snake_position[1] - fruit_position[1]) < 10):
        score += 1
        fruit_spawn = False
        # Load the sound file
        game_over_sound = pygame.mixer.Sound('res/EatSound.mp3')
        # Play the sound
        game_over_sound.play()
    else:
        snake_body.pop()

# Fruit spawn function
def spawn_fruit():
    global fruit_position, fruit_spawn, snake_body
    # Finds a valid spawn for the fruit and prevents the fruit to spawn on the snake's body	
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_width//10)) * 10,
                        random.randrange(1, (window_height//10)) * 10]
        while fruit_position in snake_body:
            fruit_position = [random.randrange(1, (window_width//10)) * 10,
                            random.randrange(1, (window_height//10)) * 10]
    fruit_spawn = True

# Object function
def draw_object():
    window_screen.fill(black)
    for pos in snake_body:
        pygame.draw.rect(window_screen, pink, pygame.Rect(pos[0], pos[1], 10, 10))
        # Load apple image with alpha channel
        apple_img = pygame.image.load('res/Apple.png').convert_alpha() 
        # Scale down the apple image to 10x10 pixels
        apple_img = pygame.transform.scale(apple_img, (10, 10)) 
        # Draw the apple image on the screen
        window_screen.blit(apple_img, (fruit_position[0], fruit_position[1])) 
        # Displays the score countinuously
        total_score(1, white, 'times new roman', 20)

# Game Over conditions function
def check_game_over():
    # Touching the edge of the screen (Wall Collision)
    if snake_position[0] < 0 or snake_position[0] > window_width-10:
        game_over()
    elif snake_position[1] < 0 or snake_position[1] > window_width-10:
        game_over()

    # Touching the snake body (Body Collision)
    # First block/Snake's head = snake_body[1:]
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

# Main function
def main():
    while True:
        key_events()
        manage_direction()
        move_snake()
        spawn_fruit()
        draw_object()
        check_game_over()
        # Updates the entire pygame display
        pygame.display.update()
        # Maximum FPS allowed
        fps.tick(difficulty)

if __name__ == '__main__':
    main()
