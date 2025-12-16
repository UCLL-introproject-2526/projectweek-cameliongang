import pygame
import os

def process_blocks(sheet_path, output_dir):
    pygame.init()
    pygame.display.set_mode((1,1))
    
    try:
        sheet = pygame.image.load(sheet_path).convert()
        sheet_w, sheet_h = sheet.get_size()
        
        # Determine layout. 
        # Usually user prompt "side by side" -> 2 columns, 1 row.
        # But generator output might vary.
        # Let's assume 2 cols, 1 or 2 rows.
        # The generated image looks like 2 distinct blocks.
        
        # Strategy: Simply split in half horizontally?
        # Or manually select if they are clearly separated.
        # Assuming 2 blocks side-by-side. 
        
        cols = 2
        rows = 1 # Or 2 if it generated variants.
        # Let's start with simple 2 columns.
        
        sprite_w = sheet_w // cols
        sprite_h = sheet_h # Full height
        
        # Target Size: 64x64
        target_size = (64, 64)
        
        filenames = {
            0: "dirt_block.png",
            1: "slime_block.png"
        }
        
        for idx, filename in filenames.items():
            rect = pygame.Rect(idx * sprite_w, 0, sprite_w, sprite_h)
            sprite = sheet.subsurface(rect).copy()
            
            # 1. Remove Magenta (#FF00FF and friends)
            new_sprite = pygame.Surface((sprite_w, sprite_h), pygame.SRCALPHA)
            new_sprite.fill((0,0,0,0))
            
            # Simple bounding box cropping might be needed if the generator put them in center of big cells.
            min_x, min_y, max_x, max_y = sprite_w, sprite_h, 0, 0
            has_pixels = False
            
            for x in range(sprite_w):
                for y in range(sprite_h):
                    r, g, b, *_ = sprite.get_at((x, y))
                    
                    # Magenta Filter
                    is_bg = False
                    if r > 150 and b > 150 and g < 100: is_bg = True
                    
                    if not is_bg:
                        new_sprite.set_at((x, y), (r, g, b, 255))
                        min_x = min(min_x, x)
                        min_y = min(min_y, y)
                        max_x = max(max_x, x)
                        max_y = max(max_y, y)
                        has_pixels = True
            
            # 2. Crop to Content
            if has_pixels:
                crop_rect = pygame.Rect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
                final_sprite = new_sprite.subsurface(crop_rect).copy()
            else:
                final_sprite = new_sprite
            
            # 3. Resize to 64x64 (Full Tile Fill)
            # Since these are building blocks, they MUST fill the 64x64 tile.
            # We use scale (not smoothscale) to preserve pixel art look if resolution is close, 
            # but usually smoothscale is better if downscaling huge images.
            # Let's use scale for "crispness" if it's pixel art.
            
            scaled_sprite = pygame.transform.scale(final_sprite, target_size)
            
            save_path = os.path.join(output_dir, filename)
            pygame.image.save(scaled_sprite, save_path)
            print(f"Saved {filename} {target_size}")
            
    except Exception as e:
        print(f"Error: {e}")
        
    pygame.quit()

if __name__ == '__main__':
    sheet_path = r"C:/Users/seppi/.gemini/antigravity/brain/a0a66a42-5b19-4ab6-a366-ca317f995b8d/block_sprites_flat_1765914527748.png"
    out_dir = r"c:/Users/seppi/Desktop/pygame week/projectweek-cameliongang/resources"
    process_blocks(sheet_path, out_dir)
