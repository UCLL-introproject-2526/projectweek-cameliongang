
import pygame
import os
import math

def distance(c1, c2):
    return math.sqrt(sum([(a - b) ** 2 for a, b in zip(c1, c2)]))

def remove_background(filepath):
    pygame.display.init()
    pygame.display.set_mode((1, 1), pygame.NOFRAME) 

    try:
        image = pygame.image.load(filepath).convert()
        width, height = image.get_size()
        
        # Create a new surface with alpha channel
        new_image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # Target Magenta
        target_color = (255, 0, 255)
        # Tolerance usually needed for generated images (compression artifacts)
        threshold = 100 

        for x in range(width):
            for y in range(height):
                p_color = image.get_at((x, y))
                # Compare RGB only, ignore Alpha of original if present
                if distance(p_color[:3], target_color) < threshold:
                    # Make transparent
                    new_image.set_at((x, y), (0, 0, 0, 0))
                else:
                    # Copy pixel
                    new_image.set_at((x, y), p_color)
        
        # Save overwrite
        pygame.image.save(new_image, filepath)
        print(f"Successfully processed (with tolerance) and saved: {filepath}")
        
    except Exception as e:
        print(f"Error processing image: {e}")

if __name__ == "__main__":
    # Process both locations
    targets = [
        os.path.join(os.getcwd(), 'resources', 'settings_icon.png'),
        os.path.join(os.getcwd(), '..', 'resources', 'settings_icon.png')
    ]
    for target in targets:
        target = os.path.abspath(target)
        if os.path.exists(target):
            print(f"Targeting: {target}")
            remove_background(target)
        else:
            print(f"Target not found: {target}")
    pygame.quit()
