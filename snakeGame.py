import pygame
import pygame.mixer
import random
import time
import sys

# Initialize all pygame modules
pygame.init()

# Initialize the mixer module
pygame.mixer.init()

# Game window setup
windowWidth = 500
windowHeight = 500
windowScreen = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Snake Game by Shade')

# Colors
# RGB tuples
black = (7, 7, 7)
white = (255, 255, 255)
red = (255, 0, 0)
pink = (231, 97, 247)

pygame.init()

# Clock object for FPS
fps = pygame.time.Clock()
 
# Game Elements
# Snake body ( first 3 blocks)
snakeBody = [[100, 50], [90, 50], [80, 50]]
# Default snake position
snakePosition = [100, 50]
# Increase/Decrease the number of px per movement
snakeMovement = 10
# Default snake direction
direction = 'RIGHT'
nextDirection = direction
# Snake speed
difficulty = 20
# Fruit spawn
fruitSpawn = True
# fruit position
fruitPosition = [random.randrange(1, (windowWidth//10)) * 10,
				random.randrange(1, (windowHeight//10)) * 10]
# Initial Score
score = 0

# Score function
def totalScore(choice, color, font, size):
    # Creates a font object
    scoreFont = pygame.font.SysFont(font, size)
    # Live score
    scoreSurface = scoreFont.render('Score : ' + str(score), True, color)
    # Rectangle object
    scoreRect = scoreSurface.get_rect()
    # Score surface and rectangle will be drawn
    windowScreen.blit(scoreSurface, scoreRect)

# Game Over function
def gameOver():
    # Load GameOver image
    gameOverImg = pygame.image.load('res/GameOver.png')
    # Scale down the image
    gameOverImg = pygame.transform.scale(gameOverImg, (324.5, 191.5))
    # Get the rect for the image
    gameOverImgRect = gameOverImg.get_rect()
    # Set the position of the image in the middle of the screen
    gameOverImgRect.center = (windowWidth/2, windowHeight/2)
    # Create a font object for the score
    scoreeFont = pygame.font.SysFont('times new roman', 20)
    # Render the score text
    scoreeSurface = scoreeFont.render('score: ' + str(score), True, white)
    # Get the rect for the score text
    scoreeRect = scoreeSurface.get_rect()
    # Set the position of the score text below the image
    scoreeRect.midtop = (windowWidth/2, gameOverImgRect.bottom + 20)
    # Fill the screen with black color
    windowScreen.fill(black)
    # Draw the image on the screen
    windowScreen.blit(gameOverImg, gameOverImgRect)
    # Draw the score text on the screen
    windowScreen.blit(scoreeSurface, scoreeRect)
    # Update the display
    pygame.display.flip()
    # Load the sound file
    gameOverSound = pygame.mixer.Sound('res/GameOverSound.mp3')
    # Play the sound
    gameOverSound.play()
    # Wait for 3 seconds before quitting
    time.sleep(3)
    # Quit pygame and terminate the script
    pygame.quit()
    sys.exit()

# Main function
while True:

    # Key events
    # Arrow keys and WASD keys
    # ESC to exit
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                nextDirection = 'UP'
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                nextDirection = 'DOWN'
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                nextDirection = 'LEFT'
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                nextDirection = 'RIGHT'
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Direction management                    
    if nextDirection == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif nextDirection == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif nextDirection == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif nextDirection == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the Snake
    # snakeMovement = 10
    # Y - coordinate decreases by 10px
    if direction == 'UP':
        snakePosition[1] -= snakeMovement
    # Y - coordinate increases by 10px
    elif direction == 'DOWN':
        snakePosition[1] += snakeMovement
    # X - coordinate decreases by 10px
    elif direction == 'LEFT':
        snakePosition[0] -= snakeMovement
    # X - coordinate increases by 10px
    elif direction == 'RIGHT':
        snakePosition[0] += snakeMovement

    # Snake body growing mechanism
	# if fruits and snakes collide then scores
	# will be incremented by 10
    snakeBody.insert(0, list(snakePosition))
    if (abs(snakePosition[0] - fruitPosition[0]) < 10) and (abs(snakePosition[1] - fruitPosition[1]) < 10):
        score += 1
        fruitSpawn = False
        # Load the sound file
        gameOverSound = pygame.mixer.Sound('res/EatSound.mp3')
        # Play the sound
        gameOverSound.play()
    else:
        snakeBody.pop()
		
    if not fruitSpawn:
        fruitPosition = [random.randrange(1, (windowWidth//10)) * 10,
						random.randrange(1, (windowHeight//10)) * 10]
		
    fruitSpawn = True
    windowScreen.fill(black)
	
    for pos in snakeBody:
        pygame.draw.rect(windowScreen, pink, pygame.Rect(pos[0], pos[1], 10, 10))
        # Load apple image with alpha channel
        appleImg = pygame.image.load('res/apple.png').convert_alpha() 
        # Scale down the apple image to 10x10 pixels
        appleImg = pygame.transform.scale(appleImg, (10, 10)) 
        # Draw the apple image on the screen
        windowScreen.blit(appleImg, (fruitPosition[0], fruitPosition[1])) 

    # Game Over conditions
    # Touching the edge of the screen (Wall Collision)
    if snakePosition[0] < 0 or snakePosition[0] > windowWidth-10:
        gameOver()
    elif snakePosition[1] < 0 or snakePosition[1] > windowWidth-10:
        gameOver()

    # Touching the snake body (Body Collision)
    # First block/Snake's head = snakeBody[1:]
    for block in snakeBody[1:]:
        if snakePosition[0] == block[0] and snakePosition[1] == block[1]:
            gameOver()

    # displaying score countinuously
    totalScore(1, white, 'times new roman', 20)

    # Updates the entire pygame display
    pygame.display.update()

    # Maximum FPS allowed
    fps.tick(difficulty)
