from PIL import Image
import os
import sys

def remove_magenta_background(image_path):
    """
    Opens an image, replaces Magenta (255, 0, 255) with transparency,
    and saves it back (or as a new file).
    """
    try:
        img = Image.open(image_path).convert("RGBA")
        datas = img.getdata()

        new_data = []
        for item in datas:
            # Magenta is (255, 0, 255)
            if item[0] == 255 and item[1] == 0 and item[2] == 255:
                new_data.append((255, 255, 255, 0)) # Transparent
            else:
                new_data.append(item)

        img.putdata(new_data)
        
        # Save as png to preserve transparency
        filename, ext = os.path.splitext(image_path)
        output_path = f"{filename}_transparent.png"
        img.save(output_path, "PNG")
        print(f"Successfully saved to {output_path}")

    except Exception as e:
        print(f"Error processing {image_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_background.py <path_to_image>")
        # Default behavior: Look for any "raw" named files or just prompt
        input("Press Enter to exit...")
    else:
        file_path = sys.argv[1]
        remove_magenta_background(file_path)
