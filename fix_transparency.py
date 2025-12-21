from PIL import Image
import os

def force_transparency(path):
    try:
        img = Image.open(path).convert("RGBA")
        datas = img.getdata()
        new_data = []
        for item in datas:
            # Check for Magenta (255, 0, 255) exact
            # Also maybe check for near-magenta?
            if item[0] > 240 and item[1] < 20 and item[2] > 240:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        img.save(path, "PNG")
        print(f"Fixed transparency for {path}")
    except Exception as e:
        print(f"Failed to fix {path}: {e}")

force_transparency("resources/mute_icon_on.png")
force_transparency("resources/mute_icon_off.png")
