import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.big_font = pygame.font.Font(None, 60)
        
        # Load Icons
        self.fire_icon = pygame.image.load(os.path.join(ASSETS_DIR, 'icon_fire.png')).convert_alpha()
        self.fire_icon = pygame.transform.scale(self.fire_icon, (48, 48))
        
        self.fire_rect = self.fire_icon.get_rect(topleft=(20, 20))

    def show_hud(self, player):
        # Background for HUD
        pygame.draw.rect(self.display_surface, (50, 50, 50), (10, 10, 150, 70), border_radius=10)
        pygame.draw.rect(self.display_surface, (200, 200, 200), (10, 10, 150, 70), 3, border_radius=10)

        # Show Power Icon if active
        if player.power == 'fire':
            self.display_surface.blit(self.fire_icon, self.fire_rect)
            text = self.font.render("Double Jump", True, (255, 100, 100))
            self.display_surface.blit(text, (80, 35))
        elif player.power == 'sticky':
            # Placeholder icon or same icon with different text for now
            # self.display_surface.blit(self.slime_icon, self.fire_rect) 
            text = self.font.render("Wall Jump", True, (100, 255, 100))
            self.display_surface.blit(text, (30, 35)) # Adjust position if no icon yet
        else:
            text = self.font.render("No Power", True, (200, 200, 200))
            self.display_surface.blit(text, (30, 35))

    def show_main_menu(self):
        self.display_surface.fill((30, 30, 30))
        
        title = self.big_font.render("Chameleon Platformer", True, (100, 255, 100))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.display_surface.blit(title, title_rect)
        
        info = self.font.render("Press ENTER to Start", True, (255, 255, 255))
        info_rect = info.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.display_surface.blit(info, info_rect)

        controls = self.font.render("WASD/Arrows to Move - Click to Grapple - Space to Jump", True, (150, 150, 150))
        controls_rect = controls.get_rect(center=(WIDTH // 2, HEIGHT * 0.8))
        self.display_surface.blit(controls, controls_rect)

    def show_pause_menu(self):
        # Transparent Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.display_surface.blit(overlay, (0, 0))
        
        text = self.big_font.render("PAUSED", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.display_surface.blit(text, rect)
        
    def show_level_select(self, levels):
        self.display_surface.fill((30, 30, 30))
        
        title = self.big_font.render("Select Level", True, (100, 255, 100))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT * 0.2))
        self.display_surface.blit(title, title_rect)

        for index, level in enumerate(levels):
            # Display level name (generic or specific if we had names)
            level_text = f"[{index + 1}] Level {index}"
            if index == 0: level_text += " (Tutorial)"
            
            text_surf = self.font.render(level_text, True, (255, 255, 255))
            rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT * 0.4 + index * 50))
            self.display_surface.blit(text_surf, rect)

    def show_loading_screen(self):
        self.display_surface.fill((0, 0, 0))
        text = self.big_font.render("Loading...", True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.display_surface.blit(text, rect)
        pygame.display.update()
