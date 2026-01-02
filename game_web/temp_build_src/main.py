import sys
import os
import asyncio

# Add the 'Game' directory to sys.path to allow imports from inside 'Game' to work
# This makes 'player', 'initial', etc. importable as top-level modules
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    script_dir = sys._MEIPASS
else:
    # Running from source
    script_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(script_dir) # Fix resource loading
sys.path.append(os.path.join(script_dir, 'Game'))

from initial import main

try:
    if __name__ == "__main__":
        print("Starting main.py...")
        if sys.platform == "emscripten":
            asyncio.run(main())
        else:
            asyncio.run(main())
except Exception as e:
    import traceback
    err = traceback.format_exc()
    print(err)
    # Attempt to show error on Web Page
    try:
        if sys.platform == "emscripten":
            import platform
            platform.window.document.body.innerHTML = f"<div style='color:red; font-size: 16px; font-family: monospace; white-space: pre-wrap; padding: 20px; background: #220000;'><h1>Python Error</h1>{err}</div>"
    except:
        pass
