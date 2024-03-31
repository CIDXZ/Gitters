import pygame

# Initialize Pygame
pygame.init()

# Get the desktop size
info = pygame.display.Info()
screen_width = 1920
screen_height = 1080

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))

# Load the player images
player_image_path = "player.png"
player_image = pygame.image.load(player_image_path)
player_image_left_path = "player_left.png"
player_image_left = pygame.image.load(player_image_left_path)
player_x = 0
player_y = screen_height - player_image.get_height()
player_speed = 5
player_direction = "right"
player_velocity = 0

# Load the background image
background_path = "background.png"
background_image = pygame.image.load(background_path)

# Load the gun images
gun_right_path = "gun_right.png"
gun_right_image = pygame.image.load(gun_right_path)
gun_left_path = "gun_left.png"
gun_left_image = pygame.image.load(gun_left_path)
gun_image = gun_right_image  # Start with the gun facing right
gun_x = gun_x = player_x + player_image.get_width() / 2 - gun_image.get_width() / 2 - 20
gun_y = player_y + player_image.get_height() / 2
gun_velocity = 0

# Set up the clock
clock = pygame.time.Clock()

# Set up gravity and jump variables
gravity = 0.5
jump_velocity = 10
is_jumping = False

# Start the game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                player_velocity = -jump_velocity
                gun_velocity = -jump_velocity

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_direction = "left"
        player_x -= player_speed
        player_image = player_image_left
        gun_image = gun_left_image  # Use the left gun image if facing left
        gun_x = player_x + player_image.get_width() / 2 - gun_image.get_width() / 2 - 20
    if keys[pygame.K_RIGHT]:
        player_direction = "right"
        player_x += player_speed
        player_image = pygame.image.load(player_image_path)
        gun_image = gun_right_image  # Use the right gun image if facing right
        gun_x = player_x + player_image.get_width() / 2 - gun_image.get_width() / 2 - 20

    # Apply gravity
    player_velocity += gravity
    player_y += player_velocity
    gun_velocity += gravity
    gun_y += gun_velocity

    # Check if the player hits the ground
    if player_y + player_image.get_height() > screen_height:
        player_y = screen_height - player_image.get_height()
        player_velocity = 0
        is_jumping = False
    if gun_y + gun_image.get_height() > screen_height:
        gun_y = screen_height - gun_image.get_height()
        gun_velocity = 0

    # Draw the background
    screen.blit(background_image, (0, 0))

    # Draw the player
    if player_direction == "left":
        screen.blit(player_image_left, (player_x, player_y))
    else:
        screen.blit(player_image, (player_x, player_y))

    # Draw the gun
    screen.blit(gun_image, (gun_x, gun_y))

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock. tick(60)

   











