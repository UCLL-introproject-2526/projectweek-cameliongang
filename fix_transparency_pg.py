import pygame as pg
import os

def force_transparency(path):
    try:
        pg.display.init() # Need display for convert
        pg.display.set_mode((1,1), pg.HIDDEN)
        
        img = pg.image.load(path).convert_alpha()
        w, h = img.get_size()
        
        # Pixel Array access
        for x in range(w):
            for y in range(h):
                color = img.get_at((x, y))
                # Check for Magenta (255, 0, 255) exact or close
                if color.r > 240 and color.g < 20 and color.b > 240:
                    img.set_at((x, y), (255, 255, 255, 0))
        
        pg.image.save(img, path)
        print(f"Fixed transparency for {path}")
    except Exception as e:
        print(f"Failed to fix {path}: {e}")

if __name__ == "__main__":
    force_transparency("resources/mute_icon_on.png")
    force_transparency("resources/mute_icon_off.png")
