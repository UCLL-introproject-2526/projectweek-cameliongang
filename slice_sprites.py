import pygame
import os

# Path to the generated sprite sheet
sprite_sheet_path = r"C:/Users/seppi/.gemini/antigravity/brain/a0a66a42-5b19-4ab6-a366-ca317f995b8d/camelion_sprites_clean.png"
output_dir = r"c:/Users/seppi/Desktop/pygame week/projectweek-cameliongang/resources"

# Load the sprite sheet
try:
    sheet = pygame.image.load(sprite_sheet_path)
    sheet_width, sheet_height = sheet.get_size()
    print(f"Sheet size: {sheet_width}x{sheet_height}")
    
    # Assuming 3x2 grid
    sprite_width = sheet_width // 3
    sprite_height = sheet_height // 2
    
    sprites = []
    for y in range(2):
        for x in range(3):
            rect = pygame.Rect(x * sprite_width, y * sprite_height, sprite_width, sprite_height)
            sprite = sheet.subsurface(rect)
            sprites.append(sprite)
            
    # Mapping Fixed:
    # 4: Wall Right (Facing Right) -> Use for 'camelion_left_wall.png' (because code uses left_wall for wall_side > 0)
    # 5: Wall Left (Facing Left) -> Use for 'camelion_right_wall.png' (because code uses right_wall for wall_side < 0)
    
    mapping = {
        0: "camelion.png",
        1: "camelion_left.png",
        2: "camelion_ceiling.png",
        3: "camelion_ceiling_left.png",
        4: "camelion_left_wall.png",
        5: "camelion_right_wall.png"
    }
    
    for i, filename in mapping.items():
        save_path = os.path.join(output_dir, filename)
        pygame.image.save(sprites[i], save_path)
        print(f"Saved {filename}")
        
except Exception as e:
    print(f"Error: {e}")

pygame.quit()
