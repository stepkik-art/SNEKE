import pygame, random

# Initialize pygame
pygame.init()

# Set display window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("~~SNEKE~~")

# Set FSP and clock
FPS = 20
clock = pygame.time.Clock()

# Set game values
SNAKE_SIZE = 20
head_x = WINDOW_WIDTH // 2
head_y = WINDOW_HEIGHT // 2 + 100
snake_dx = 0
snake_dy = 0
score = 0

# Set colors
GREEN = (0, 255, 0)
DARKGREEN = (10, 50, 10)
RED = (255, 0, 0)
DARKRED = (50, 50, 50)
WHITE = (255, 255, 255 )

# Set fonts
font = pygame.font.SysFont('gabriola', 48)
# Set text
title_text = font.render("~~Snake~~", True, GREEN, DARKRED)  # make a text object
title_rect = title_text.get_rect()  # gets the box containing the text object
title_rect.center = (WINDOW_WIDTH // 2,
                     WINDOW_HEIGHT // 2)  # places the box containing the text object's center to the middle of the screen.
score_text = font.render("score: 0", True, DARKGREEN, RED)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

# do this
game_over_text = font.render("GAME OVER", True, DARKGREEN, RED)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("Continue", True, DARKGREEN, RED)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 64)

# Set sounds and music
pick_up_sound = pygame.mixer.Sound("pick_up_sound.wav")
# Set images (in this case, use simple rects...so just create their coordinates)
# For a rectangle you need (top-left x, top-left y, width, height)

apple_coord = (500, 500, SNAKE_SIZE, SNAKE_SIZE)
apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)
head_coord = head_x, head_y, SNAKE_SIZE, SNAKE_SIZE
head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)

body_coords = []

# The main game loop
running = True
is_paused = False
while running:
    # Check to see if the user wants to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Move the snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                snake_dx = -1 * SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_RIGHT:
                snake_dx = 1 * SNAKE_SIZE
                snake_dy = 0
            if event.key == pygame.K_UP:
                snake_dx = 0
                snake_dy = -1 * SNAKE_SIZE
            if event.key == pygame.K_DOWN:
                snake_dx = 0
                snake_dy = 1 * SNAKE_SIZE

    # Add the head coordinate to the first index of the body coordinate list
    # This will essentilalyl move allof the snakes body by one position in the list
    body_coords.insert(0, head_coord)
    body_coords.pop()

    # Update the x,y position of the snakes head and make a new coordinate
    head_x += snake_dx
    head_y += snake_dy
    head_coord = (head_x, head_y, SNAKE_SIZE, SNAKE_SIZE)

    # Check for game over
    if head_rect.left < 0 or head_rect.right > WINDOW_WIDTH or head_rect.top < 0 or head_rect.bottom > WINDOW_HEIGHT or head_coord in body_coords:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()
        is_paused = True

    while is_paused:
        for event in pygame.event.get():
            # The player wants to quit
            if event.type == pygame.QUIT:
                is_paused = False
                running = False
            # The player wishes to continue.
            if event.type == pygame.KEYDOWN:
                score = 0
                head_x = WINDOW_WIDTH // 2
                head_y = WINDOW_HEIGHT // 2 + 100
                head_coord = head_x, head_y, SNAKE_SIZE, SNAKE_SIZE
                is_paused = False

    # Check for collisions
    if head_rect.colliderect(apple_rect):
        score += 1
        pick_up_sound.play()
        apple_x = random.randint(0, WINDOW_WIDTH - SNAKE_SIZE)
        apple_y = random.randint(0, WINDOW_HEIGHT - SNAKE_SIZE)
        apple_coord = (apple_x, apple_y, SNAKE_SIZE, SNAKE_SIZE)
        body_coords.append(head_coord)

    # Update HUD
    score_text = font.render(f"score: {score}", True, DARKGREEN, RED)

    # Fill the surface
    display_surface.fill(WHITE)

    # Blit HUD
    display_surface.blit(title_text, title_rect)
    display_surface.blit(score_text, score_rect)

    # Blit assets
    for body in body_coords:
        pygame.draw.rect(display_surface, DARKGREEN, body)
    head_rect = pygame.draw.rect(display_surface, GREEN, head_coord)
    apple_rect = pygame.draw.rect(display_surface, RED, apple_coord)

    # Update display and tick clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
