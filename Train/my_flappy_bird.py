import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

collision_img = pygame.image.load("game_over.png")
collision_img = pygame.transform.scale(collision_img, (WIDTH, HEIGHT))  # Resize to fit the screen dimensions

collision_sound = pygame.mixer.Sound("game_over_audio.wav")


# Pipe properties
pipe_width = 80
pipe_x = WIDTH
pipe_height = random.randint(150, 400)  # Initialize with a random height
pipe_y = pipe_height + 200
pipe_speed = 10

# Bird properties
bird_x = 400
bird_y = 200
bird_velocity = 2

# Load images and resize them
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (70, 70))  # Resize to 30x30 pixels

background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Resize to fit the screen dimensions

# Bird properties
bird_rect = bird_img.get_rect()
bird_rect.center = (100, 300)

# Game variables
score = 0
font = pygame.font.Font(None, 36)

start_text = pygame.font.Font(None, 72).render("Use space bar to go up", True, (255, 0, 0))
screen.blit(start_text, (150, 250))
pygame.display.update()
pygame.time.delay(1000)  # Display the text for 2 seconds (2000 milliseconds)

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -10

    # Update bird position and velocity
    bird_rect.y += bird_velocity
    bird_velocity += 0.5
    if bird_rect.y > HEIGHT:
        bird_rect.y = HEIGHT
        bird_velocity = 0

    # Update pipe position and height
    pipe_x -= pipe_speed
    if pipe_x < -pipe_width:
        pipe_x = WIDTH
        pipe_height = random.randint(150, 400)  # Randomize the pipe's height for each new pipe
        pipe_y = pipe_height + 200
        score += 1

    # Collision detection
    bird_rect_copy = bird_rect.copy()
    bird_rect_copy.x += 10  # Adjust the collision box for a better gameplay feel

    if (bird_rect.y < 0 or bird_rect.y > HEIGHT) or (bird_rect_copy.colliderect(pipe_x, 0, pipe_width, pipe_height) or bird_rect_copy.colliderect(pipe_x, pipe_y,
                                                                                                    pipe_width,
                                                                                            HEIGHT - pipe_y)):
        # Play collision sound
        collision_sound.play()

        # Display collision image
        screen.blit(collision_img, (0, 0))
        pygame.display.update()

        # Pause for a moment to show the collision effect
        pygame.time.delay(1500)  # Delay in milliseconds (1.5 seconds)

        pygame.quit()
        sys.exit()

    # Clear the screen
    screen.blit(background_img, (0, 0))

    # Draw the bird
    screen.blit(bird_img, bird_rect)

    # Draw the pipe
    pipe_img = pygame.image.load("pipe.png")
    pipe_img = pygame.transform.scale(pipe_img, (pipe_width, pipe_height))
    screen.blit(pipe_img, (pipe_x, 0))

    pipe_img = pygame.image.load("pipe.png")
    pipe_img = pygame.transform.scale(pipe_img, (pipe_width, HEIGHT - pipe_y))
    screen.blit(pipe_img, (pipe_x, pipe_y))

    # Draw the score
    text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    # Update the display
    pygame.display.update()

    # Control game speed
    pygame.time.Clock().tick(30)