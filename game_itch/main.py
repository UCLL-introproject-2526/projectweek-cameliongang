import sys
import os
import asyncio

# Add the 'Game' directory to sys.path to allow imports from inside 'Game' to work
# This makes 'player', 'initial', etc. importable as top-level modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'Game'))

from initial import main

if __name__ == "__main__":
    print("Starting main.py...")
    asyncio.run(main())
