import pygame
import random
import sys
import time
import asyncio

async def main():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()
    # Set up the screen dimensions
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set up the title of the window
    pygame.display.set_caption("Phishing invader !!")

    # Load images
    deepfake = pygame.image.load('deepfake.png')
    unknown_enveloppe = pygame.image.load('unknown_enveloppe.png')
    #player_shield_image = pygame.image.load('player_shield.png')
    player_shield_image = pygame.image.load('pass.png')
    mallicious_enveloppe = pygame.image.load('malicious_enveloppe.png')
    legitimate_enveloppe = pygame.image.load('legitimate_enveloppe.png')
    background_image = pygame.image.load('background.png')


    # Load sound & background music

    #if sys.platform == "Emscripten":
    shoot_sound = pygame.mixer.Sound('pew.ogg')
    notification_sound = pygame.mixer.Sound('notificationalert.ogg')
    background_music = pygame.mixer.music.load('alienalerts.ogg')
    #else:
        
     #   shoot_sound = pygame.mixer.Sound('pew.mp3')
     #   notification_sound = pygame.mixer.Sound('notificationalert.mp3')
     #   background_music = pygame.mixer.music.load('alienalerts.mp3')


    # Define some colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    YELLOW = (255,255,0)
    BLACK = (0,0,0)
    # Initialize game variables
    player_x = SCREEN_WIDTH // 3
    player_y = SCREEN_HEIGHT - 100
    envelopes = []  # List to store envelopes
    deepfakes = []  # List to store envelopes
    score = 0

    

    # Initialize player's bullet
    player_bullet = None



    # Load the font for displaying text
    font  = pygame.font.SysFont('Arial', 46)

    # Play the background music loop
    pygame.mixer.music.play(-1)

    # Define a function to display the Game Over screen
    def show_game_over(score):
        # Clear the screen
        screen.fill((255, 255, 255))

        # Display the "Game Over" text in bold font
        game_over_text  = font.render("GAME OVER", True, (0, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))

        # Display the player's score
        score_text  = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150))

        # Update the display
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()
    

    # Game loop

    while True:
        screen.blit(background_image, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("Quitting game...")
                    print("your score is : "+str(score))
                    pygame.quit()
                    sys.exit()
                elif event.key  == pygame.K_SPACE:
                    # Play the shoot sound effect
                    shoot_sound.play()
                    # Shoot a bullet
                    player_bullet = (player_x, player_y+10)
                    
        score_text = pygame.font.SysFont('Arial', 20).render("Score: " + str(score), True, BLACK)
        
        # Move player character based on input (e.g., arrow keys)
        keys_pressed = pygame.key.get_pressed()    
        if keys_pressed[pygame.K_LEFT]:
            player_x -= 5
        if keys_pressed[pygame.K_RIGHT]:
            player_x += 5
        if keys_pressed[pygame.K_UP]:
            player_y -= 5
        if keys_pressed[pygame.K_DOWN]:
            player_y += 5

        # Move bullet (if exists)
        if player_bullet:
            new_player_bullet = (player_bullet[0] +7 , player_bullet[1])
            if abs(new_player_bullet[1]) > SCREEN_HEIGHT:            
                player_bullet = None
            else:
                player_bullet = new_player_bullet

        # Check for collision between bullet and envelope
        for i, (envelope_x, envelope_y, envelope_type) in enumerate(envelopes):
            if player_bullet and abs(player_bullet[0] - envelope_x) < 20 and abs(player_bullet[1] - envelope_y) < 20:
                # Hit the envelope!

                if envelope_type == "legitimate":
                    score -=2
                    envelopes.pop(i)
                
                elif envelope_type == "unknown":
                    new_envelope_type = random.choice(["legitimate", "malicious"])
                    envelopes[i]  = (envelope_x, envelope_y, new_envelope_type)

                elif envelope_type == "malicious":
                    notification_sound.play()
                    score +=5
                    envelopes.pop(i)
                player_bullet = None

        
        # Generate new envelopes at a steady rate
        if len(envelopes) < 5 and random.randint(0, 100) < 50:
            envelope_type = random.choice(["legitimate", "malicious", "unknown"])
            envelopes.append((random.randint(500, SCREEN_WIDTH), random.randint(5, SCREEN_HEIGHT), envelope_type))

        # Generate some deepfake randomly
        if len(deepfakes) < 1 and random.randint(0, 200) < 5:
            deepfakes.append((random.randint(750, SCREEN_WIDTH), random.randint(5, SCREEN_HEIGHT)))

        # Move envelopes from right to left
        for i, (envelope_x, envelope_y, envelope_type) in enumerate(envelopes):
            new_envelope_x  = envelope_x - 2
            if new_envelope_x  < -20:  # Envelope has gone off the screen, remove it
                envelopes.pop(i)
            else:
                envelopes[i]  = (new_envelope_x, envelope_y, envelope_type)
        
        # Move deepfakes from right to left
        for i, (deepfake_x, deepfake_y) in enumerate(deepfakes):
            new_deepfake_x  = deepfake_x - 5
            if new_deepfake_x < -20:  # deepfake has gone off the screen, remove it
                deepfakes.pop(i)
            else:
                deepfakes[i]  = (new_deepfake_x, deepfake_y)

        # Check if an envelope hits the player's shield
        for i, (envelope_x, envelope_y, envelope_type) in enumerate(envelopes):
            if abs(player_x - envelope_x) < 30 and abs(player_y - envelope_y) < 40:   # Envelope is within the shield range
                if envelope_type == "malicious":   # Malicious envelope, damage the player
                    # Call the function when the game is over
                    show_game_over(score)
                    
                elif envelope_type == "legitimate":   # Legitimate envelope, reward the player
                    notification_sound.play()
                    score += 5
                envelopes.pop(i)   # Remove the envelope from the list

        # Check if a deepfake hits the player's shield
        for i, (deepfake_x, deepfake_y) in enumerate(deepfakes):
            if abs(player_x - deepfake_x) < 20 and abs(player_y - deepfake_y) < 80:   # deepfake is within the shield range
                # Call the function when the game is over
                show_game_over(score)

        # Blit the score text onto the screen
        screen.blit(score_text, (10, 10))  # Adjust the x and y coordinates as needed
        
        # Draw player shield
        screen.blit(player_shield_image, (player_x -35, player_y -25))

        # Draw envelopes
        for envelope_x, envelope_y,envelope_type in envelopes:
            if envelope_type == "legitimate":
                screen.blit(legitimate_enveloppe, (envelope_x -10, envelope_y -10))
            elif envelope_type == "malicious":    
                screen.blit(mallicious_enveloppe, (envelope_x -10, envelope_y -10))
            else:
                screen.blit(unknown_enveloppe, (envelope_x -10, envelope_y -10))

        # Draw deepfakes
        for deepfake_x, deepfake_y in deepfakes:
            screen.blit(deepfake, (deepfake_x -30, deepfake_y -50))

        # Draw bullet (if exists)
        if player_bullet:
            pygame.draw.rect(screen, BLACK, (player_bullet[0]+10, player_bullet[1]+15, 12, 2))

        # Update the screen
        
        pygame.display.update()
        await asyncio.sleep(0)
        clock.tick(60)
asyncio.run(main())