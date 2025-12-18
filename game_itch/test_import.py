
try:
    import pygame
    print("Pygame imported successfully")
except ImportError as e:
    print(f"Pygame import failed: {e}")

try:
    import asyncio
    print("Asyncio imported successfully")
except ImportError as e:
    print(f"Asyncio import failed: {e}")

try:
    from Game.initial import main
    print("Game.initial imported successfully")
except Exception as e:
    print(f"Game.initial import failed: {e}")
