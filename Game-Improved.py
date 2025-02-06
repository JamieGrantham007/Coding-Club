import pygame
import sys
import random

def main():
    # Initialize pygame
    pygame.init()
    
    # Constants
    WHITE = (255, 255, 255)
    SPEED = 5
    FPS = 30  # Frames per second
    PROJECTILE_LIFETIME = 100  # Frames
    PROJECTILE_MAX_DISTANCE = 500  # Pixels

    # Screen setup
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Simple Character Game")

    # Load background image
    bg = pygame.image.load('freepik__expand__3427.jpeg').convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # Load character sprite sheet
    sprite_sheet = pygame.image.load( 'Pink_Monster_Run_6.png').convert_alpha()

    # Load enemy sprite sheet
    enemy_sprite_sheet = pygame.image.load('Red_Slime/Walk.png').convert_alpha()

    # Load attack sprite sheet
    attack_sprite_sheet = pygame.image.load('Attack2.png').convert_alpha()

    # Load hurt sprite sheet
    hurt_sprite_sheet = pygame.image.load('Hurt.png').convert_alpha()

    # Define enemy color and size
    ENEMY_COLOR = (255, 0, 0)  # Red color
    ENEMY_SIZE = (50, 50)

    # Define projectile color and size
    PROJECTILE_COLOR = (0, 255, 0)  # Green color
    PROJECTILE_SIZE = (20, 20)

    # Define health bar properties
    MAX_HEALTH = 3
    health = MAX_HEALTH
    health_regen_time = 0

    # Enemy and projectile lists
    enemies = []
    projectiles = []
    enemies_killed = 0

    # Define function to extract frames from sprite sheet
    def get_sprite_frames(sheet, rows, cols, scale_factor=1):
        frames = []
        sheet_width, sheet_height = sheet.get_size()
        frame_width = sheet_width // cols
        frame_height = sheet_height // rows
        for row in range(rows):
            for col in range(cols):
                frame = sheet.subsurface((col * frame_width, row * frame_height, frame_width, frame_height))
                frame = pygame.transform.scale(frame, (int(frame_width * scale_factor), int(frame_height * scale_factor)))
                frames.append(frame)
        return frames

    # Extract frames from enemy sprite sheet (assuming 1 row, 8 columns)
    enemy_frames = get_sprite_frames(enemy_sprite_sheet, 1, 8)
    enemy_current_frame = 0

    # Extract frames from attack sprite sheet (assuming 1 row, 6 columns)
    attack_frames = get_sprite_frames(attack_sprite_sheet, 1, 6, scale_factor=2)
    attack_current_frame = 0
    attacking = False

    # Extract frames from hurt sprite sheet (assuming 1 row, 4 columns)
    hurt_frames = get_sprite_frames(hurt_sprite_sheet, 1, 4, scale_factor=2)
    hurt_current_frame = 0
    hurt = False

    # Function to spawn an enemy
    def spawn_enemy():
        x = random.randint(0, WIDTH - ENEMY_SIZE[0])
        y = random.randint(0, HEIGHT - ENEMY_SIZE[1])
        enemy_rect = pygame.Rect(x, y, *ENEMY_SIZE)
        enemies.append(enemy_rect)

    # Function to display game over menu
    def game_over_menu():
        font = pygame.font.Font(None, 74)
        text = font.render(f'Game Over! Enemies killed: {enemies_killed}', True, (0, 0, 0))  # Black color
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(text, text_rect)

        play_again_text = font.render('Play Again', True, (0, 0, 0))  # Black color
        play_again_rect = play_again_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(play_again_text, play_again_rect)

        quit_text = font.render('Quit', True, (0, 0, 0))  # Black color
        quit_rect = quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 150))
        screen.blit(quit_text, quit_rect)

        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if play_again_rect.collidepoint(event.pos):
                        main()
                    elif quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

    # Spawn initial enemies
    for _ in range(5):
        spawn_enemy()

    # Extract frames from sprite sheet (assuming 1 row, 6 columns)
    character_frames = get_sprite_frames(sprite_sheet, 1, 6, scale_factor=2)
    current_frame = 0

    # Create character rect
    character_rect = character_frames[0].get_rect(center=(WIDTH//2, HEIGHT//2))

    # Define direction constants
    LEFT = "left"
    RIGHT = "right"
    UP = "up"
    DOWN = "down"

    # Initialize direction
    direction = DOWN
    moving = False

    # Initialize font
    pygame.font.init()
    font = pygame.font.Font(None, 36)

    # Main game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Start attack animation
                attacking = True
                attack_current_frame = 0
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Determine movement direction
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character_rect.x -= SPEED
            direction = LEFT
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            character_rect.x += SPEED
            direction = RIGHT
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            character_rect.y -= SPEED
            direction = UP
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            character_rect.y += SPEED
            direction = DOWN
            moving = True

        # Limit character to screen boundaries
        if character_rect.left < 0:
            character_rect.left = 0
        if character_rect.right > WIDTH:
            character_rect.right = WIDTH
        if character_rect.top < 0:
            character_rect.top = 0
        if character_rect.bottom > HEIGHT:
            character_rect.bottom = HEIGHT

        # Update animation frame
        if moving:
            current_frame = (current_frame + 1) % len(character_frames)
        else:
            current_frame = 0  # Reset to idle frame if not moving

        # Update attack animation frame
        if attacking:
            attack_current_frame += 1
            if attack_current_frame >= len(attack_frames):
                attacking = False
                attack_current_frame = 0

        # Update hurt animation frame
        if hurt:
            hurt_current_frame += 1
            if hurt_current_frame >= len(hurt_frames):
                hurt = False
                hurt_current_frame = 0

        # Update projectiles
        for projectile in projectiles[:]:
            rect, target, start_pos, lifetime = projectile
            dx, dy = target[0] - rect.centerx, target[1] - rect.centery
            dist = (dx**2 + dy**2) ** 0.5
            if dist > 0:
                dx, dy = dx / dist, dy / dist
                rect.x += int(dx * SPEED)
                rect.y += int(dy * SPEED)
            lifetime -= 1
            if not screen.get_rect().contains(rect) or lifetime <= 0 or (abs(rect.x - start_pos[0]) > PROJECTILE_MAX_DISTANCE or abs(rect.y - start_pos[1]) > PROJECTILE_MAX_DISTANCE):
                projectiles.remove(projectile)

        # Move enemies towards the player
        for enemy in enemies:
            dx, dy = character_rect.centerx - enemy.centerx, character_rect.centery - enemy.centery
            dist = (dx**2 + dy**2) ** 0.5
            if dist > 0:
                dx, dy = dx / dist, dy / dist
                enemy.x += int(dx * SPEED / 2)
                enemy.y += int(dy * SPEED / 2)

            # Check if enemy is very close to the player
            if enemy.colliderect(character_rect.inflate(-character_rect.width // 2, -character_rect.height // 2)):
                health -= 1
                hurt = True
                enemies.remove(enemy)
                spawn_enemy()
                if health <= 0:
                    running = False
                    game_over_menu()

        # Regenerate health
        if health < MAX_HEALTH:
            health_regen_time += 1
            if health_regen_time >= FPS * 5:  # 5 seconds
                health += 1
                health_regen_time = 0

        # Update enemy animation frame
        enemy_current_frame = (enemy_current_frame + 1) % len(enemy_frames)

        # Check for collisions
        if attacking:
            attack_rect = attack_frames[attack_current_frame].get_rect(center=character_rect.center)
            for enemy in enemies[:]:
                if attack_rect.colliderect(enemy):
                    enemies.remove(enemy)
                    enemies_killed += 1
                    spawn_enemy()

        # Draw background
        screen.blit(bg, (0, 0))
        
        # Draw character
        if hurt:
            screen.blit(hurt_frames[hurt_current_frame], character_rect)
        elif attacking:
            if direction == LEFT:
                screen.blit(pygame.transform.flip(attack_frames[attack_current_frame], True, False), character_rect)
            else:
                screen.blit(attack_frames[attack_current_frame], character_rect)
        else:
            if direction == LEFT:
                screen.blit(pygame.transform.flip(character_frames[current_frame], True, False), character_rect)
            else:
                screen.blit(character_frames[current_frame], character_rect)

        # Draw enemies
        for enemy in enemies:
            screen.blit(enemy_frames[enemy_current_frame], enemy.topleft)

        # Draw projectiles
        for projectile in projectiles:
            pygame.draw.rect(screen, PROJECTILE_COLOR, projectile[0])

        # Draw health bar above the player's head
        for i in range(health):
            pygame.draw.rect(screen, (255, 0, 0), (character_rect.left + i * 40, character_rect.top - 40, 30, 30))

        # Draw enemy kill tally
        tally_text = font.render(f'Enemies killed: {enemies_killed}', True, (0, 0, 0))  # Black color
        screen.blit(tally_text, (10, 10))

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
