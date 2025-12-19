
import re

def find_wasm():
    path = r"game_itch/build/web/cpython312/main.js"
    try:
        with open(path, 'rb') as f:
            content = f.read() 
            # Decode carefully or just search bytes
            content_str = content.decode('utf-8', errors='ignore')
            
            matches = re.findall(r'[\w\-\.]+\.wasm', content_str)
            print(f"Found .wasm matches: {matches}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_wasm()
