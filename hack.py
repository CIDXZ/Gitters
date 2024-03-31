import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Constants
fullscreen = True  # Set to False if you don't want fullscreen
if fullscreen:
    info_object = pygame.display.Info()
    WIDTH, HEIGHT = info_object.current_w, info_object.current_h
else:
    WIDTH, HEIGHT = 1200, 800  # Set your preferred window size
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (169, 169, 169)
FPS = 60

# Game setup
if fullscreen:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberDefender")
clock = pygame.time.Clock()

# Load images
background_image = pygame.image.load("background.jpg")  # Replace with your background image
threat_icon = pygame.image.load("threat_icon.png")  # Replace with your threat icon image

# Load sounds
correct_sound = pygame.mixer.Sound("correct.wav")  # Replace with your sound file
incorrect_sound = pygame.mixer.Sound("incorrect.wav")  # Replace with your sound file

# Button class
class Button:
    def __init__(self, text, x, y, width, height, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action

    def draw(self, color=WHITE):
        pygame.draw.rect(screen, color, self.rect, border_radius=15)  # Increased border radius
        pygame.draw.rect(screen, GRAY, self.rect.inflate(-10, -10), border_radius=12)  # Increased inflation
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, color)
        screen.blit(text, (self.rect.centerx - text.get_width() // 2, self.rect.centery - text.get_height() // 2))

def display_intro():
    font = pygame.font.Font(None, 36)
    intro_text = ["Welcome to CyberDefender!",
                  "You are a cybersecurity professional defending a network.",
                  "Your task is to identify and block the incoming threat."]
    for i, line in enumerate(intro_text):
        text = font.render(line, True, WHITE)
        screen.blit(text, (50, 50 + i * 50))

def generate_threat():
    threat_types = [
        {"name": "Malware", "response": "Run a malware scan"},
        {"name": "Phishing Attack", "response": "Analyze network traffic"},
        {"name": "DDoS Attack", "response": "Update firewall rules"},
        {"name": "SQL Injection", "response": "Analyze network traffic"},
        # Add more threat types here
    ]
    return random.choice(threat_types)

def display_threat(threat):
    font = pygame.font.Font(None, 48)
    text = font.render(f"Incoming Threat: {threat['name']}", True, RED)
    screen.blit(text, (50, HEIGHT // 2 - 150))  # Increased vertical position

def evaluate_response(threat, response):
    return threat["response"] == response

# Update the display_score function
def display_score(score, high_score, current_text):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score} | High Score: {high_score}", True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.topright = (WIDTH - 70, 50)  # Adjusted position to the top right
    screen.blit(score_text, score_rect)

    font = pygame.font.Font(None, 28)
    text = font.render(current_text, True, WHITE)
    screen.blit(text, (50, HEIGHT // 2 - 200))  # Display text above buttons

def play_game():
    score = 0
    attempts = 0
    time_limit = 10  # seconds
    high_score = 0
    current_text = ""  # Text to display on the window
    
    while True:
        threat = generate_threat()
        answer_submitted = False
        start_time = time.time()

        # Create buttons
        buttons = [
            Button("Run a malware scan", 50, HEIGHT // 2, 300, 60, "Run a malware scan"),  # Increased button size
            Button("Analyze network traffic", 400, HEIGHT // 2, 300, 60, "Analyze network traffic"),  # Increased button size
            Button("Update firewall rules", 750, HEIGHT // 2, 300, 60, "Update firewall rules")  # Increased button size
        ]

        while not answer_submitted and time.time() - start_time < time_limit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.rect.collidepoint(event.pos):
                            correct_answer = evaluate_response(threat, button.action)
                            answer_submitted = True

                            if correct_answer:
                                button.draw(GREEN)
                                pygame.mixer.Sound.play(correct_sound)
                                current_text = "Correct! Well done!"
                                score += 1
                            else:
                                button.draw(RED)
                                pygame.mixer.Sound.play(incorrect_sound)
                                current_text = "Incorrect. Try again."

            screen.blit(background_image, (0, 0))  # Draw background
            display_intro()
            display_score(score, high_score, current_text)
            display_threat(threat)

            # Display timer
            elapsed_time = int(time.time() - start_time)
            timer_font = pygame.font.Font(None, 36)
            timer_color = RED if elapsed_time >= time_limit else WHITE
            timer_text = timer_font.render(f"Time left: {time_limit - elapsed_time}s", True, timer_color)
            screen.blit(timer_text, (50, HEIGHT // 2 - 250))  # Increased vertical position

            # Draw threat icon
            screen.blit(threat_icon, (WIDTH // 2 - 75, HEIGHT // 2 - 75))  # Increased size

            for button in buttons:
                button.draw()

            pygame.display.flip()
            clock.tick(FPS)

        if not answer_submitted:
            current_text = "Time's up! The threat got through."
            attempts += 1

        # Display feedback for 1 second
        pygame.display.flip()
        pygame.time.wait(1000)

        # Update high score
        if score > high_score:
            high_score = score

        # Adjust time limit based on score
        if score >= 5:
            time_limit = max(5, time_limit - 1)

        # Generate a new threat and reset the state
        if attempts >= 5:  # Limit to 5 attempts for demonstration purposes
            current_text = f"Game Over! Your final score: {score}"
            pygame.quit()
            sys.exit()

if __name__ == "__main__":
    play_game()




















