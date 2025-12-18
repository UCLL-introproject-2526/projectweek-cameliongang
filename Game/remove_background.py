
import pygame
import os

def remove_background(filepath):
    pygame.display.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME) 

    try:
        image = pygame.image.load(filepath).convert()
        # Get color at (0,0) assuming it is the background
        bg_color = image.get_at((0, 0))
        print(f"Detected background color at (0,0): {bg_color}")
        
        # Set colorkey
        image.set_colorkey(bg_color)
        
        # Create a new surface with alpha channel
        new_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        new_image.blit(image, (0, 0))
        
        # Save overwrite
        pygame.image.save(new_image, filepath)
        print(f"Successfully processed and saved: {filepath}")
        
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    target = os.path.join(os.path.dirname(__file__), '..', 'resources', 'slime_block.png')
    target = os.path.abspath(target)
    print(f"Targeting: {target}")
    remove_background(target)
    pygame.quit()
