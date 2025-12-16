import pygame
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.big_font = pygame.font.Font(None, 60)
        
        # Load Icons
        self.fire_icon = pygame.image.load('assets/icon_fire.png').convert_alpha()
        self.fire_icon = pygame.transform.scale(self.fire_icon, (48, 48))
        
        self.fire_rect = self.fire_icon.get_rect(topleft=(20, 20))

    def show_hud(self, player):
        # Background for HUD
        # Ref: http://projectweek.leone.ucll.be/reference/python/clean-code/index.html#use-keyword-arguments
        pygame.draw.rect(
            surface=self.display_surface, 
            color=HUD_BG_COLOR, 
            rect=(*HUD_POS, *HUD_SIZE), 
            border_radius=HUD_BORDER_RADIUS
        )
        pygame.draw.rect(
            surface=self.display_surface, 
            color=HUD_BORDER_COLOR, 
            rect=(*HUD_POS, *HUD_SIZE), 
            width=HUD_BORDER_WIDTH, 
            border_radius=HUD_BORDER_RADIUS
        )

        # Show Power Icon if active
        if player.power == 'fire':
            self.display_surface.blit(source=self.fire_icon, dest=self.fire_rect)
            text = self.font.render("Double Jump", True, POWER_TEXT_COLOR_FIRE)
            self.display_surface.blit(source=text, dest=(80, 35))
        elif player.power == 'sticky':
            # Placeholder for sticky power UI
            text = self.font.render("Wall Jump", True, POWER_TEXT_COLOR_STICKY)
            self.display_surface.blit(source=text, dest=(30, 35))
        else:
            text = self.font.render("No Power", True, POWER_TEXT_COLOR_NONE)
            self.display_surface.blit(source=text, dest=(30, 35))

    def show_main_menu(self):
        self.display_surface.fill(BG_COLOR)
        
        title = self.big_font.render("Chameleon Platformer", True, TITLE_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.display_surface.blit(source=title, dest=title_rect)
        
        info = self.font.render("Press ENTER to Start", True, TEXT_COLOR)
        info_rect = info.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.display_surface.blit(source=info, dest=info_rect)

        controls = self.font.render("WASD/Arrows to Move - Click to Grapple - Space to Jump", True, INFO_COLOR)
        controls_rect = controls.get_rect(center=(WIDTH // 2, HEIGHT * 0.8))
        self.display_surface.blit(source=controls, dest=controls_rect)

    def show_pause_menu(self):
        # Transparent Overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        self.display_surface.blit(source=overlay, dest=(0, 0))
        
        text = self.big_font.render("PAUSED", True, TEXT_COLOR)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.display_surface.blit(source=text, dest=rect)
        
    def show_level_select(self, levels):
        self.display_surface.fill(BG_COLOR)
        
        title = self.big_font.render("Select Level", True, TITLE_COLOR)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT * 0.2))
        self.display_surface.blit(source=title, dest=title_rect)

        for index, level in enumerate(levels):
            # Display level name
            level_text = f"[{index + 1}] Level {index}"
            if index == 0: level_text += " (Tutorial)"
            
            text_surf = self.font.render(level_text, True, TEXT_COLOR)
            rect = text_surf.get_rect(center=(WIDTH // 2, HEIGHT * 0.4 + index * 50))
            self.display_surface.blit(source=text_surf, dest=rect)

    def show_loading_screen(self):
        self.display_surface.fill(BLACK)
        text = self.big_font.render("Loading...", True, LOADING_TEXT_COLOR)
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.display_surface.blit(source=text, dest=rect)
        pygame.display.update()
