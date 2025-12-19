import pygame
import os

def fix_fly():
    pygame.init()
    input_path = "./resources/animated_fly_raw.png"
    output_path = "./resources/animated_fly.png"
    
    if not os.path.exists(input_path):
        print(f"File not found at {input_path}")
        return

    # Load without convert() to be headless compatible
    raw_img = pygame.image.load(input_path)
    width, height = raw_img.get_size()
    print(f"Image Dimensions: {width}x{height}")
    
    # Create new surface with alpha support
    img = pygame.Surface((width, height), pygame.SRCALPHA)
    img.blit(raw_img, (0, 0))
    
    # Pixel access
    pixels = pygame.PixelArray(img)
    
    replaced_count = 0
    # Replace magenta-ish colors
    for x in range(width):
        for y in range(height):
            c = img.get_at((x, y))
            r, g, b, a = c
            
            # Hue-based detection for "Magenta-ish" colors
            # Magenta has high Red and Blue, and low Green. Red and Blue are usually similar.
            
            # 1. Check if Red and Blue are relatively close (Hue is between Red and Blue)
            # 2. Check if Green is significantly lower than the average of Red and Blue (Saturation)
            
            rb_diff = abs(r - b)
            rb_avg = (r + b) / 2
            
            # If it's a purple/magenta hue (Red and Blue similiar, Green low)
            if rb_diff < 50 and g < (rb_avg - 40):
                 img.set_at((x, y), (0, 0, 0, 0))
                 replaced_count += 1
            # Also catch the pure generator output specific range just in case Hue misses edge cases (very dark)
            elif r > 100 and g < 60 and b > 100:
                img.set_at((x, y), (0, 0, 0, 0))
                replaced_count += 1
                
    del pixels
    
    print(f"Replaced {replaced_count} pixels with transparency.")
    
    # Save back
    pygame.image.save(img, output_path)
    print(f"Saved fixed image to {output_path}")
    pygame.quit()

if __name__ == "__main__":
    # Ensure correct CWD
    if not os.path.exists("resources"):
         # Try changing to script dir if resources not found
         script_dir = os.path.dirname(os.path.abspath(__file__))
         os.chdir(script_dir)
         
    fix_fly()
