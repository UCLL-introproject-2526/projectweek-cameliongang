import pygame
import os

def fix_emote():
    pygame.init()
    path = "./game_itch/resources/emote_67.png"
    
    if not os.path.exists(path):
        print(f"File not found at {path}")
        return

    # Load without convert() to be headless
    raw_img = pygame.image.load(path)
    width, height = raw_img.get_size()
    print(f"Image Dimensions: {width}x{height}")
    
    # Create new surface with alpha support
    img = pygame.Surface((width, height), pygame.SRCALPHA)
    img.blit(raw_img, (0, 0))
    
    # Pixel access
    pixels = pygame.PixelArray(img)
    
    replaced_count = 0
    # Replace magenta-ish colors
    # Iterating heavily might be slow in python but 500kb image is small enough (approx 500x500 = 250k pixels)
    for x in range(width):
        for y in range(height):
            c = img.get_at((x, y))
            r, g, b, a = c
            
            # Check for generic magenta/pink range
            if r > 180 and g < 100 and b > 180:
                img.set_at((x, y), (0, 0, 0, 0))
                replaced_count += 1
                
    del pixels
    
    print(f"Replaced {replaced_count} pixels with transparency.")
    
    # Save back
    pygame.image.save(img, path)
    print("Saved fixed image.")
    pygame.quit()

if __name__ == "__main__":
    if not os.path.exists("game_itch"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
    fix_emote()
