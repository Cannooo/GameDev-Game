import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Game window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
RED = (255, 0, 0)

# Character attributes
CHAR_WIDTH = 50
CHAR_HEIGHT = 50
CHAR_SPEED = 5

# Treasure attributes
TREASURE_SIZE = 25
NUM_TREASURES = 10
TREASURE_RESPAWN_DELAY = 5  # in seconds

# Hazard attributes
HAZARD_SIZE = 50
MIN_HAZARDS = 5
MAX_HAZARDS = 10
HAZARD_SPEED = 2

# Hazard spawn delay (in seconds)
HAZARD_SPAWN_DELAY = 2

# Initialize the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Treasure Hunt")

# Load game assets
character_img = pygame.image.load("character.png")
treasure_img = pygame.image.load("treasure.png")
hazard_img = pygame.image.load("hazard.png")

# Set up clock for FPS control
clock = pygame.time.Clock()

# Initialize game variables
score = 0
lives = 3
time_remaining = 1800
num_hazards = MIN_HAZARDS

# Create character
character = pygame.Rect(
    WINDOW_WIDTH // 2 - CHAR_WIDTH // 2,
    WINDOW_HEIGHT // 2 - CHAR_HEIGHT // 2,
    CHAR_WIDTH,
    CHAR_HEIGHT,
)

# Create treasures
treasures = []
for _ in range(NUM_TREASURES):
    treasure = pygame.Rect(
        random.randint(0, WINDOW_WIDTH - TREASURE_SIZE),
        random.randint(0, WINDOW_HEIGHT - TREASURE_SIZE),
        TREASURE_SIZE,
        TREASURE_SIZE,
    )
    treasures.append(treasure)

# Create hazards
hazards = []

# Function to spawn a hazard
def spawn_hazard():
    hazard = pygame.Rect(
        random.randint(0, WINDOW_WIDTH - HAZARD_SIZE),
        random.randint(0, WINDOW_HEIGHT - HAZARD_SIZE),
        HAZARD_SIZE,
        HAZARD_SIZE,
    )
    hazards.append(hazard)

# Function to update hazard positions
def update_hazard_positions():
    for hazard in hazards:
        direction_x = character.x - hazard.x
        direction_y = character.y - hazard.y
        distance = math.hypot(direction_x, direction_y)

        # Normalize the direction vector
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Update the hazard position based on the direction
        hazard.x += int(direction_x * HAZARD_SPEED)
        hazard.y += int(direction_y * HAZARD_SPEED)

        # Collision detection for hazards
        for other_hazard in hazards:
            if hazard != other_hazard and hazard.colliderect(other_hazard):
                # Move the hazard away from the other hazard
                if hazard.x < other_hazard.x:
                    hazard.x -= HAZARD_SPEED
                else:
                    hazard.x += HAZARD_SPEED

                if hazard.y < other_hazard.y:
                    hazard.y -= HAZARD_SPEED
                else:
                    hazard.y += HAZARD_SPEED

# Function to respawn treasures
def respawn_treasures():
    for _ in range(NUM_TREASURES):
        treasure = pygame.Rect(
            random.randint(0, WINDOW_WIDTH - TREASURE_SIZE),
            random.randint(0, WINDOW_HEIGHT - TREASURE_SIZE),
            TREASURE_SIZE,
            TREASURE_SIZE,
        )
        treasures.append(treasure)

# Game loop
running = True
next_hazard_spawn_time = pygame.time.get_ticks() + HAZARD_SPAWN_DELAY * 1000
next_treasure_respawn_time = pygame.time.get_ticks() + TREASURE_RESPAWN_DELAY * 1000
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Character movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and character.y > 0:
        character.y -= CHAR_SPEED
    if keys[pygame.K_DOWN] and character.y < WINDOW_HEIGHT - CHAR_HEIGHT:
        character.y += CHAR_SPEED
    if keys[pygame.K_LEFT] and character.x > 0:
        character.x -= CHAR_SPEED
    if keys[pygame.K_RIGHT] and character.x < WINDOW_WIDTH - CHAR_WIDTH:
        character.x += CHAR_SPEED

    # Check for treasure collection
    for treasure in treasures[:]:
        if character.colliderect(treasure):
            treasures.remove(treasure)
            score += 1

    # Update hazard positions
    update_hazard_positions()

    # Check for hazard collision
    for hazard in hazards[:]:
        if character.colliderect(hazard):
            hazards.remove(hazard)
            lives -= 1

    # Update time remaining
    time_remaining -= 1

    # Clear the screen
    window.fill(WHITE)

    # Draw character
    window.blit(character_img, (character.x, character.y))

    # Draw treasures
    for treasure in treasures:
        window.blit(treasure_img, (treasure.x, treasure.y))

    # Draw hazards
    for hazard in hazards:
        window.blit(hazard_img, (hazard.x, hazard.y))

    # Update the display
    pygame.display.update()

    # Spawn a hazard if it's time
    if pygame.time.get_ticks() >= next_hazard_spawn_time and len(hazards) < num_hazards:
        spawn_hazard()
        next_hazard_spawn_time = pygame.time.get_ticks() + HAZARD_SPAWN_DELAY * 1000

    # Respawn treasures if they have all been collected and it's time
    if not treasures and pygame.time.get_ticks() >= next_treasure_respawn_time:
        respawn_treasures()
        next_treasure_respawn_time = pygame.time.get_ticks() + TREASURE_RESPAWN_DELAY * 1000

    # Increase the number of hazards over time
    if time_remaining % 300 == 0 and num_hazards < MAX_HAZARDS:
        num_hazards += 1

    # Check game over conditions
    if lives <= 0 or time_remaining <= 0:
        running = False

    # Control FPS
    clock.tick(60)

# Game over screen
window.fill(WHITE)
game_over_text = pygame.font.SysFont(None, 50).render(
    f"Game Over - Final Score: {score}", True, RED
)
window.blit(
    game_over_text,
    (
        WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
        WINDOW_HEIGHT // 2 - game_over_text.get_height() // 2,
    ),
)
pygame.display.update()

# Wait for a few seconds before quitting
pygame.time.wait(3000)

# Quit the game
pygame.quit()
