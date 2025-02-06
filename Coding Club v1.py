import pygame
import sys

def main():
    # Initialize pygame
    pygame.init()

    # Constants
    SPEED = 5
    FPS = 30  # Frames per second

    # Screen setup
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Simple Character Game")

    # Load background image
    bg = pygame.image.load('/Users/jamiegrantham/Downloads/pikaso-creations/freepik__expand__3427.jpeg').convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    # Load character sprite sheet
    sprite_sheet = pygame.image.load('/Users/jamiegrantham/Downloads/craftpix-net-622999-free-pixel-art-tiny-hero-sprites/1 Pink_Monster/Pink_Monster_Run_6.png').convert_alpha()

    # Define function to extract frames from sprite sheet
    def get_sprite_frames(sheet, rows, cols, scale_factor=2):
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

    # Extract frames from sprite sheet (assuming 1 row, 6 columns)
    character_frames = get_sprite_frames(sprite_sheet, 1, 6)
    current_frame = 0

    # Create character rect
    character_rect = character_frames[0].get_rect(center=(WIDTH//2, HEIGHT//2))

    # Main game loop
    clock = pygame.time.Clock()
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get keys pressed
        keys = pygame.key.get_pressed()

        # Determine movement direction
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            character_rect.x -= SPEED
            moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            character_rect.x += SPEED
            moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            character_rect.y -= SPEED
            moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            character_rect.y += SPEED
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


        # Draw background
        screen.blit(bg, (0, 0))
        
        # Draw character
        screen.blit(character_frames[current_frame], character_rect)
        
        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
