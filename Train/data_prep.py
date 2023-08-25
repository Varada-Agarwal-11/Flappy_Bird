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
bird_flap = 0  # Initialize as no flap
bird_flap_active = False  # To track if bird is currently flapping

# Load images and resize them
bird_img = pygame.image.load("bird.png")
bird_img = pygame.transform.scale(bird_img, (100, 50))  # Resize to 30x30 pixels

background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))  # Resize to fit the screen dimensions

# Bird properties
bird_rect = bird_img.get_rect()
bird_rect.center = (100, 300)

# Game variables
font = pygame.font.Font(None, 36)

# Data collection
all_game_data = []

# Function to reset game variables
def reset_game():
    global pipe_x, pipe_height, pipe_y, bird_velocity, bird_rect, score, bird_flap, bird_flap_active
    pipe_x = WIDTH
    pipe_height = random.randint(150, 400)
    pipe_y = pipe_height + 200
    bird_velocity = 2
    bird_rect.center = (100, 300)
    score = 0
    bird_flap = 0  # Reset bird flap to no flap
    bird_flap_active = False  # Reset flap status

# Main game loop for multiple games
while True:
    data = []  # Data for the current game
    score = 0  # Initialize the score for each new game
    bird_flap_cooldown = 0  # Cooldown for allowing a new flap

    # Game loop for a single game
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and bird_rect.y >= 0 and bird_flap_cooldown <= 0:
                    bird_velocity = -10
                    bird_flap_active = True  # Bird is actively flapping
                    bird_flap_cooldown = 20  # Cooldown for next flap

        # Decrease flap cooldown
        if bird_flap_cooldown > 0:
            bird_flap_cooldown -= 1

        # Reset bird flap status when bird starts falling
        if bird_velocity > 0:
            bird_flap_active = False

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
            pipe_height = random.randint(150, 400)
            pipe_y = pipe_height + 200
            score += 1

        # Collision detection
        bird_rect_copy = bird_rect.copy()
        bird_rect_copy.x += 10

        if (bird_rect.y < 0 or bird_rect.y > HEIGHT) or (bird_rect_copy.colliderect(pipe_x, 0, pipe_width, pipe_height) or bird_rect_copy.colliderect(pipe_x, pipe_y, pipe_width, HEIGHT - pipe_y)):
            # # Play collision sound
            # collision_sound.play()

            # Display collision image
            screen.blit(collision_img, (0, 0))
            pygame.display.update()

            # Pause for a moment to show the collision effect
            pygame.time.delay(500)

            # Save data for the current game
            all_game_data.append(data)

            # Reset the game for a new round
            reset_game()
            break

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

        # Data collection: Record the game state and action
        game_state = {
            "bird_x": bird_rect.x,
            "bird_y": bird_rect.y,
            "pipe_x": pipe_x,
            "pipe_height": pipe_height,
            "bird_velocity": bird_velocity,
            "pipe_speed": pipe_speed,
            "bird_flap": bird_flap,
            "score": score,
            "game_over": 0  # 0 for ongoing
        }

        action = 1 if bird_flap_active else 0  # Capture bird's flap action

        data.append((game_state, action))

        # Control game speed
        pygame.time.Clock().tick(30)

    # Check if you want to start another game or exit
    play_again = input("Play again? (y/n): ")
    if play_again.lower() != 'y':
        break

# Save all collected data to a file
with open('flappy_bird_data.txt', 'w') as file:
    for game_data in all_game_data:
        for frame_data in game_data:
            file.write(f"{frame_data}\n")
        file.write("Game Over\n")