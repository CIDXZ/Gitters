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
gun_offset_x = 40
gun_offset_y = 0

# Load the bullet image
bullet_path = "bullet.png"
bullet_image = pygame.image.load(bullet_path)
bullet_speed = 10
bullet_list = []

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
            elif event.key == pygame.K_r:
                bullet_x = gun_x + gun_image.get_width() / 2 - bullet_image.get_width() / 2
                bullet_y = gun_y + gun_image.get_height() / 2 - bullet_image.get_height() / 2
                bullet_list.append([bullet_x, bullet_y])

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_direction = "left"
        player_x -= player_speed
        player_image = player_image_left
        gun_image = gun_left_image  # Use the left gun image if facing left
    if keys[pygame.K_RIGHT]:
        player_direction = "right"
        player_x += player_speed
        player_image = pygame.image.load(player_image_path)
        gun_image = gun_right_image  # Use the right gun image if facing right

    # Apply gravity
    player_velocity += gravity
    player_y += player_velocity

    # Check if the player hits the ground
    if player_y + player_image.get_height() > screen_height:
        player_y = screen_height - player_image.get_height()
        player_velocity = 0
        is_jumping = False

    # Move the bullets
    for bullet in bullet_list:
        bullet[0] += bullet_speed

    # Draw the bullets
    for bullet in bullet_list:
        screen.blit(bullet_image, (bullet[0], bullet[1]))

    # Remove bullets that


    # Remove bullets that have gone off-screen
    bullet_list = [bullet for bullet in bullet_list if bullet[0] < screen_width]

    # Update the position of the gun based on the position of the player
    gun_x = player_x + player_image.get_width() / 2 - gun_image.get_width() / 2 - gun_offset_x
    gun_y = player_y + player_image.get_height() / 2 - gun_image.get_height() / 2 - gun_offset_y

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
    clock.tick(60)



















