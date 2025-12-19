import pygame
import os

def process_gui():
    pygame.init()
    
    # Process Button Assets (re-run to ensure consistency) + Health Bar Assets
    
    # 1. Pixel GUI Assets
    input_path = "pixel_gui_assets.png"
    if os.path.exists(input_path):
        sheet = pygame.image.load(input_path)
        w, h = sheet.get_size()
        mw = w // 2
        mh = h // 2
        
        # Approximate crops for generated 2x2 grid
        assets = {
            "button_normal.png": (0, 0, mw, mh),
            "button_pressed.png": (mw, 0, mw, mh),
            "loading_frame.png": (0, mh, mw, mh),
            "loading_fill.png": (mw + 50, mh + 50, 100, 100)
        }
        process_sheet(input_path, assets)

    # 2. Health Bar Assets
    input_path = "health_bar_ui_assets.png"
    if os.path.exists(input_path):
        sheet = pygame.image.load(input_path)
        w, h = sheet.get_size()
        
        # The prompt asked for: Long frame + Heart icon.
        # usually 1024x1024.
        # Let's assume they are laid out. I need to auto-detect or crop broadly.
        # But auto-cropping each transparent island is better.
        
        # Let's write a generic island extractor if possible, but hard without computer vision libs.
        # Manual crop strategy based on visual:
        # Prompt said: "Frame approx aspect ratio 10:1 (long), Heart separate."
        # Usually ImageGen puts them in center or grid.
        # Let's assume the Frame is the biggest object, Heart is smaller.
        
        # We will make the whole image transparent, then find islands using connected components? 
        # Too complex.
        # Let's just crop halves? Or crop by non-magenta bounds.
        
        # Let's assume 2 rows? Or simpler: Just save the whole thing as one for manual inspection? No user can't inspect.
        # Let's run the Hue Transparency on the whole image and save it as "health_ui_sheet.png"
        # AND try to split.
        
        # Simple split: Left half = Heart? Right half = Bar?
        # Actually usually it's Heart on left, Bar on right in one line.
        # Let's try splitting horizontally.
        
        mw = w // 5 # Heart is probably 1/5th width?
        
        assets = {
            "heart_icon.png": (0, 0, mw, h),
            "health_bar_frame.png": (mw, 0, w-mw, h)
        }
        process_sheet(input_path, assets)

def process_sheet(input_path, assets_dict):
    sheet = pygame.image.load(input_path)
    
    if not os.path.exists("resources"):
        os.makedirs("resources")

    for name, rect in assets_dict.items():
        sub = sheet.subsurface(pygame.Rect(rect))
        trans_surf = make_transparent(sub)
        bounding_rect = trans_surf.get_bounding_rect()
        
        if bounding_rect.width > 0 and bounding_rect.height > 0:
            final_surf = trans_surf.subsurface(bounding_rect)
            out_path = os.path.join("resources", name)
            pygame.image.save(final_surf, out_path)
            print(f"Saved {out_path}")

def make_transparent(surf):
    s_w, s_h = surf.get_size()
    new_surf = pygame.Surface((s_w, s_h), pygame.SRCALPHA)
    new_surf.blit(surf, (0,0))
    
    pixels = pygame.PixelArray(new_surf)
    for x in range(s_w):
        for y in range(s_h):
            c = new_surf.get_at((x, y))
            r, g, b, a = c
            
            rb_diff = abs(r - b)
            rb_avg = (r + b) / 2
            
            if rb_diff < 50 and g < (rb_avg - 40):
                 new_surf.set_at((x, y), (0, 0, 0, 0))
            elif r > 200 and g < 100 and b > 200:
                 new_surf.set_at((x, y), (0, 0, 0, 0))
                 
    del pixels
    return new_surf

if __name__ == "__main__":
    if not os.path.exists("resources"):
         # Try changing to script dir if resources not found
         script_dir = os.path.dirname(os.path.abspath(__file__))
         os.chdir(script_dir)
         
    process_gui()
