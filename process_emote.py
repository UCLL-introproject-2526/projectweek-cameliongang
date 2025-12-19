import pygame
import os

def process_image(input_path, output_path):
    pygame.init()
    
    # Check if input exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    try:
        img = pygame.image.load(input_path)
        img = img.convert_alpha() # Ensure it handles alpha
        
        width, height = img.get_size()
        
        # Lock the surface for pixel access
        # However, for simply setting a generic colorkey, we can use set_colorkey if it's exact.
        # But the prompt mentioned "magenta background", usually used as a key.
        # Let's try explicit pixel manipulation to be safe with "approximate" magenta if needed,
        # or just set_colorkey if it's solid.
        # The previous script had a threshold. Let's stick to simple colorkey first as it's cleaner in pygame.
        # Magenta is (255, 0, 255).
        
        # Create a new surface with alpha
        new_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        new_surf.blit(img, (0,0))
        
        # Pixel array access
        pixels = pygame.PixelArray(new_surf)
        # Replace magenta with transparent
        # In integer color, Magenta (255, 0, 255) is roughly 0xFFFF00FF (ARGB) or similar depending on endianness.
        # Safer to iterate manually or use a mask.
        
        for x in range(width):
            for y in range(height):
                r, g, b, a = new_surf.get_at((x, y))
                # Check for magenta range (loose match like before)
                if r > 200 and g < 50 and b > 200:
                    new_surf.set_at((x, y), (0, 0, 0, 0))
        
        del pixels # Unlock
        
        pygame.image.save(new_surf, output_path)
        print(f"Processed {input_path} to {output_path}")
        
    except Exception as e:
        print(f"Failed to process image: {e}")
    
    pygame.quit()

if __name__ == "__main__":
    process_image("C:\\Users\\seppi\\.gemini\\antigravity\\brain\\160229ce-e240-4fb3-9e56-8d0497b60e81\\emote_67_magenta_bg_1766088751438.png", "C:\\Users\\seppi\\Desktop\\pygame week\\projectweek-cameliongang\\game_itch\\resources\\emote_67.png")
