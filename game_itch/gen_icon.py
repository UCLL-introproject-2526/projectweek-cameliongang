
import pygame
import os

def generate_icon(path):
    pygame.init()
    # 64x64 icon
    surf = pygame.Surface((64, 64), pygame.SRCALPHA)
    
    # Draw simple gear
    center = (32, 32)
    radius = 20
    
    # Teeth
    for i in range(8):
        angle = i * (360 / 8)
        # rotated rect logic is annoying, let's just draw lines
        # or just a circle with rects
        pass

    # Draw base circle
    pygame.draw.circle(surf, (100, 100, 100), center, radius)
    pygame.draw.circle(surf, (0, 0, 0), center, radius, 3) # Outline
    
    # Draw standard "Cog" teeth (simple rects)
    # 4 bars crossing
    rect_w = 54
    rect_h = 12
    
    # Horizontal
    r1 = pygame.Rect(0, 0, rect_w, rect_h)
    r1.center = center
    pygame.draw.rect(surf, (100, 100, 100), r1)
    pygame.draw.rect(surf, (0, 0, 0), r1, 3)

    # Vertical
    r2 = pygame.Rect(0, 0, rect_h, rect_w)
    r2.center = center
    pygame.draw.rect(surf, (100, 100, 100), r2)
    pygame.draw.rect(surf, (0, 0, 0), r2, 3)

    # Re-draw circle on top to blend
    pygame.draw.circle(surf, (100, 100, 100), center, radius)
    pygame.draw.circle(surf, (0, 0, 0), center, radius, 3)
    
    # Inner hole
    pygame.draw.circle(surf, (0, 0, 0), center, 8)
    
    pygame.image.save(surf, path)
    print(f"Generated icon at {path}")

if __name__ == "__main__":
    paths = [
        os.path.join(os.getcwd(), 'resources', 'settings_icon.png'),
        os.path.join(os.getcwd(), '..', 'resources', 'settings_icon.png')
    ]
    
    for p in paths:
        try:
            generate_icon(p)
        except Exception as e:
            print(f"Error generating {p}: {e}")
            
    pygame.quit()
