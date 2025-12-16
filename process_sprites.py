import pygame
import os

def process_sprites(sheet_path, output_dir):
    pygame.init()
    pygame.display.set_mode((1,1))
    
    try:
        sheet = pygame.image.load(sheet_path).convert()
        sheet_w, sheet_h = sheet.get_size()
        
        # Grid settings
        cols = 3
        rows = 2
        sprite_w = sheet_w // cols
        sprite_h = sheet_h // rows
        
        filenames = {
            0: "camelion.png",
            1: "camelion_left.png",
            2: "camelion_ceiling.png",
            3: "camelion_ceiling_left.png",
            4: "camelion_left_wall.png", 
            5: "camelion_right_wall.png" 
        }
        
        target_visual_height = 60 # Desired height in pixels
        
        for idx, filename in filenames.items():
            col = idx % cols
            row = idx // cols
            rect = pygame.Rect(col * sprite_w, row * sprite_h, sprite_w, sprite_h)
            sprite = sheet.subsurface(rect).copy()
            
            # 1. Remove Magenta Background (Aggressive)
            new_sprite = pygame.Surface((sprite_w, sprite_h), pygame.SRCALPHA)
            new_sprite.fill((0,0,0,0))
            
            min_x, min_y, max_x, max_y = sprite_w, sprite_h, 0, 0
            has_pixels = False
            
            for x in range(sprite_w):
                for y in range(sprite_h):
                    r, g, b, *_ = sprite.get_at((x, y))
                    
                    # Target Magenta: 255, 0, 255
                    # Euclidean distance or simple threshold
                    # If it's "purple-ish" -> remove
                    # R high, B high, G low.
                    
                    # Original check: r > 200 and b > 200 and g < 50
                    # The "lingering" was likely anti-aliasing blending green and magenta -> becoming dark purple/grey.
                    # Dark purple: R~100, B~100, G~0 ?
                    
                    # Expanded removal:
                    is_bg = False
                    
                    # Pure/Almost Magenta
                    if r > 150 and b > 150 and g < 100: is_bg = True
                    
                    # Dark Purple edges (Transition form Black/Green to Magenta)
                    # If G is very low, and R/B are somewhat close and > G?
                    # Be careful not to remove black eyes or dark green scales.
                    
                    if not is_bg:
                        new_sprite.set_at((x, y), (r, g, b, 255))
                        min_x = min(min_x, x)
                        min_y = min(min_y, y)
                        max_x = max(max_x, x)
                        max_y = max(max_y, y)
                        has_pixels = True
            
            # 2. Crop
            if has_pixels:
                crop_rect = pygame.Rect(min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)
                final_sprite = new_sprite.subsurface(crop_rect).copy()
            else:
                final_sprite = new_sprite # Empty
            
            # 3. Resize
            # Scale so height is target_visual_height. Keep aspect ratio.
            orig_w, orig_h = final_sprite.get_size()
            if orig_h > 0:
                scale_ratio = target_visual_height / orig_h
                new_w = int(orig_w * scale_ratio)
                new_h = target_visual_height
                
                # Use smoothscale for quality if possible, otherwise scale
                try:
                    scaled_sprite = pygame.transform.smoothscale(final_sprite, (new_w, new_h))
                except:
                    scaled_sprite = pygame.transform.scale(final_sprite, (new_w, new_h))
            else:
                scaled_sprite = final_sprite

            save_path = os.path.join(output_dir, filename)
            pygame.image.save(scaled_sprite, save_path)
            print(f"Saved {filename} (Resized to: {scaled_sprite.get_size()})")
            
    except Exception as e:
        print(f"Error: {e}")
        
    pygame.quit()

if __name__ == '__main__':
    sheet_path = r"C:/Users/seppi/.gemini/antigravity/brain/a0a66a42-5b19-4ab6-a366-ca317f995b8d/camelion_sprites_magenta_1765912561407.png"
    out_dir = r"c:/Users/seppi/Desktop/pygame week/projectweek-cameliongang/resources"
    process_sprites(sheet_path, out_dir)
