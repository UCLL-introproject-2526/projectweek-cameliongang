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

if __name__ == "__main__":
    print("Starting main.py...")
    asyncio.run(main())
