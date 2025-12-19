import pygame
import os

def fix_transparency():
    pygame.init()
    # Dummy display for convert_alpha
    pygame.display.set_mode((1, 1), pygame.NOFRAME)
    
    path = "resources/health_bar_frame.png"
    if not os.path.exists(path):
        print("File not found.")
        return
        
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    
    # "Punch a hole" strategy
    # The frame is likely a border.
    # Let's preserve a 10% margin on top/bottom/left/right?
    # Or fixed pixels if we know the style (Reto chunky).
    # Assuming 1024x1024 source scaled down or chopped?
    # Based on the user's screenshot, the frame looks fairly thick.
    # Let's try removing the "Dark Color" specifically first, as that is safer for preserving irregular borders.
    
    pixels = pygame.PixelArray(img)
    
    # Target Color: The dark grey background of the bar.
    # From screenshot, it looks like (34, 32, 52) or similar dark grey.
    # Let's clear anything that is very dark and not "frame colored".
    # Frame is stone (grey/light grey).
    
    for x in range(w):
        for y in range(h):
            r, g, b, a = img.get_at((x, y))
            
            # Simple Dark Threshold
            # Be careful not to delete dark shadows of the frame.
            # But the fill is a solid dark block usually.
            # Let's use a spatial heuristic: If it's in the middle 80% AND dark.
            
            in_middle_x = (w * 0.05) < x < (w * 0.95)
            in_middle_y = (h * 0.1) < y < (h * 0.9)
            
            if in_middle_x and in_middle_y:
                 # Check darkness
                 if r < 60 and g < 60 and b < 60:
                     pixels[x, y] = (0, 0, 0, 0) # Transparent
    
    del pixels
    pygame.image.save(img, path)
    print(f"Fixed transparency for {path}")
    pygame.quit()

if __name__ == "__main__":
    fix_transparency()
