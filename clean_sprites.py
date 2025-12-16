import pygame
import os

# Function to remove background
def remove_background(image_path, output_path):
    print(f"Processing {image_path}...")
    try:
        img = pygame.image.load(image_path).convert() # Load without alpha first to see colors
        width, height = img.get_size()
        
        # Detect background colors from corners
        # Assuming checkerboard, top-left 10x10 area has both colors
        bg_colors = set()
        for x in range(min(20, width)):
            for y in range(min(20, height)):
                bg_colors.add(img.get_at((x, y))[:3])
        
        # Heuristic: If we have 2 dominant colors in corner, they are BG.
        # Or simply, take top-left and a neighbor that is different.
        c1 = img.get_at((0, 0))[:3]
        bg_colors_list = [c1]
        
        # Look for a second color in the top row
        c2 = None
        for x in range(1, min(50, width)):
             c = img.get_at((x, 0))[:3]
             if c != c1:
                 c2 = c
                 bg_colors_list.append(c2)
                 break
        
        print(f"Detected BG colors: {bg_colors_list}")
        
        # Create new surface with alpha
        new_img = pygame.Surface((width, height), pygame.SRCALPHA)
        new_img.fill((0,0,0,0))
        
        for x in range(width):
            for y in range(height):
                color = img.get_at((x, y))[:3]
                is_bg = False
                for bg_c in bg_colors_list: # Check approximate match
                    if sum([abs(c-b) for c,b in zip(color, bg_c)]) < 10: # Tolerance
                        is_bg = True
                        break
                
                if not is_bg:
                    new_img.set_at((x, y), img.get_at((x, y)))
        
        pygame.image.save(new_img, output_path)
        print(f"Saved clean image to {output_path}")
        return True
    
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return False

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1,1)) # Required for convert()
    # Paths
    raw_sprite_path = r"C:/Users/seppi/.gemini/antigravity/brain/a0a66a42-5b19-4ab6-a366-ca317f995b8d/camelion_sprites_1765911465776.png"
    clean_sprite_path = r"C:/Users/seppi/.gemini/antigravity/brain/a0a66a42-5b19-4ab6-a366-ca317f995b8d/camelion_sprites_clean.png"
    
    remove_background(raw_sprite_path, clean_sprite_path)
    pygame.quit()
