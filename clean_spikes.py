import pygame
import os

def clean_spikes():
    pygame.init()
    pygame.display.set_mode((1,1))
    
    try:
        # Load magenta image
        path = r"resources\spikes_magenta.png"
        img = pygame.image.load(path).convert()
        width, height = img.get_size()
        
        # Create new surface with alpha
        new_img = pygame.Surface((width, height), pygame.SRCALPHA)
        new_img.fill((0, 0, 0, 0)) # Start transparent
        
        for x in range(width):
            for y in range(height):
                r, g, b, *_ = img.get_at((x, y))
                
                # Check for Magenta (255, 0, 255)
                # Allow slight variance if compression happened, but pixel art usually exact.
                # User prompted "pure magenta".
                if r > 200 and g < 100 and b > 200:
                    continue # Valid transparency
                
                # Copy pixel
                new_img.set_at((x, y), (r, g, b, 255))
        
        # Validate content (check if it's not empty)
        # Verify 1/4 layout? No need, just save.
        
        # Save to spikes.png
        out_path = r"resources\spikes.png"
        pygame.image.save(new_img, out_path)
        print("Successfully cleaned spikes and saved to resources/spikes.png")
        
    except Exception as e:
        print(f"Error: {e}")
    
    pygame.quit()

if __name__ == "__main__":
    clean_spikes()
