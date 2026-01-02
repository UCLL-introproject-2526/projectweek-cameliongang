import pygame as pg

class MobileInterface:
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        
        # Colors (Semi-transparent)
        # 0 is transparent, 255 opaque. 
        # Using a dark tint for better contrast on colorful backgrounds
        self.color_base = (0, 0, 0, 100) 
        self.color_press = (255, 255, 255, 100)
        self.icon_color = (255, 255, 255)
        
        # Layout
        # Left Side: Movement (Arrows)
        y_nav = self.height - 180
        # Increased size for better touch area
        self.btn_left = pg.Rect(20, y_nav, 110, 110)
        self.btn_right = pg.Rect(160, y_nav, 110, 110)
        
        # Up/Down (D-Pad Style)
        # Tighter D-Pad:
        pad_size = 90
        base_x = 50
        base_y = self.height - 250
        
        self.btn_up = pg.Rect(base_x + pad_size, base_y, pad_size, pad_size)
        self.btn_down = pg.Rect(base_x + pad_size, base_y + pad_size*2, pad_size, pad_size)
        
        # Adjust Left/Right to fit D-Pad if needed, OR keep separate.
        # Current Left/Right are at y_nav. 
        # Up/Down are at base_y.
        # Let's align them to form a cross if possible, OR keep logical separation.
        # User requested D-Pad.
        # Let's align Left/Right to the cross.
        self.btn_left = pg.Rect(base_x, base_y + pad_size, pad_size, pad_size)
        self.btn_right = pg.Rect(base_x + pad_size*2, base_y + pad_size, pad_size, pad_size)
        
        # Right Side: Actions
        # Jump (Big button)
        self.btn_jump = pg.Rect(self.width - 180, y_nav, 130, 130)
        
        # Tongue (Smaller, Top-Left of Jump group)
        self.btn_tongue = pg.Rect(self.width - 320, y_nav + 20, 100, 100)
        
        # Grapple (Above Jump)
        self.btn_grapple = pg.Rect(self.width - 180, y_nav - 140, 100, 100)
        
        # Pause (Top Left - BELOW Health Bar which is at 20,20 h=40)
        self.btn_pause = pg.Rect(20, 80, 60, 60)
        
        # State
        self.state = {
            'left': False,
            'right': False,
            'up': False,
            'down': False,
            'jump': False, 
            'grapple': False, 
            'tongue': False,
            'pause': False
        }
        
        # Touch Tracking
        self.active_touches = {} # id -> rect_name

    def draw(self, surface):
        def draw_btn(rect, name, pressed):
            # Create surf for alpha
            s = pg.Surface((rect.width, rect.height), pg.SRCALPHA)
            color = self.color_press if pressed else self.color_base
            
            # Rounded Rect background
            pg.draw.rect(s, color, s.get_rect(), border_radius=20)
            
            # Draw Icon
            c = s.get_rect().center
            ic = self.icon_color
            
            if name == 'left':
                pg.draw.polygon(s, ic, [(c[0]+15, c[1]-20), (c[0]-25, c[1]), (c[0]+15, c[1]+20)])
            elif name == 'right':
                pg.draw.polygon(s, ic, [(c[0]-15, c[1]-20), (c[0]+25, c[1]), (c[0]-15, c[1]+20)])
            elif name == 'up':
                pg.draw.polygon(s, ic, [(c[0]-20, c[1]+15), (c[0], c[1]-25), (c[0]+20, c[1]+15)])
            elif name == 'down':
                pg.draw.polygon(s, ic, [(c[0]-20, c[1]-15), (c[0], c[1]+25), (c[0]+20, c[1]-15)])
            elif name == 'jump':
                 # Up Arrow / Jump Icon
                 pg.draw.line(s, ic, (c[0], c[1]-25), (c[0], c[1]+25), 6)
                 pg.draw.line(s, ic, (c[0]-20, c[1]), (c[0], c[1]-25), 6)
                 pg.draw.line(s, ic, (c[0]+20, c[1]), (c[0], c[1]-25), 6)
            elif name == 'grapple':
                 # Hook shape
                 pg.draw.circle(s, ic, c, 15, 3)
                 pg.draw.line(s, ic, c, (c[0]+20, c[1]-20), 4)
                 # Chain
                 pg.draw.line(s, ic, (c[0]+20, c[1]-20), (c[0]+30, c[1]-30), 2)
            elif name == 'tongue':
                 # Tongue line
                 pg.draw.line(s, (255, 100, 100), (c[0]-20, c[1]), (c[0]+20, c[1]), 6)
                 pg.draw.circle(s, (255, 100, 100), (c[0]+20, c[1]), 8)
            elif name == 'pause':
                 # Pause bars
                 pg.draw.line(s, ic, (c[0]-8, c[1]-10), (c[0]-8, c[1]+10), 6)
                 pg.draw.line(s, ic, (c[0]+8, c[1]-10), (c[0]+8, c[1]+10), 6)

            surface.blit(s, rect.topleft)

        draw_btn(self.btn_left, 'left', self.state['left'])
        draw_btn(self.btn_right, 'right', self.state['right'])
        draw_btn(self.btn_up, 'up', self.state['up'])
        draw_btn(self.btn_down, 'down', self.state['down'])
        draw_btn(self.btn_jump, 'jump', self.state['jump'])
        draw_btn(self.btn_grapple, 'grapple', self.state['grapple'])
        draw_btn(self.btn_tongue, 'tongue', self.state['tongue'])
        draw_btn(self.btn_pause, 'pause', self.state['pause'])


    def handle_event(self, event):
        # Support Mouse for testing, FINGER for mobile
        if event.type == pg.FINGERDOWN:
            x = event.x * self.width
            y = event.y * self.height
            self._check_hit(x, y, event.finger_id)
            
        elif event.type == pg.FINGERUP:
            if event.finger_id in self.active_touches:
                btn_name = self.active_touches.pop(event.finger_id)
                self.state[btn_name] = False
                
        # Mouse Fallback (Single Pointer)
        elif event.type == pg.MOUSEBUTTONDOWN:
            self._check_hit(event.pos[0], event.pos[1], 'mouse')
            
        elif event.type == pg.MOUSEBUTTONUP:
            if 'mouse' in self.active_touches:
                btn_name = self.active_touches.pop('mouse')
                self.state[btn_name] = False

    def _check_hit(self, x, y, touch_id):
        # Check all buttons
        buttons = {
            'left': self.btn_left,
            'right': self.btn_right,
            'up': self.btn_up,
            'down': self.btn_down,
            'jump': self.btn_jump,
            'grapple': self.btn_grapple,
            'tongue': self.btn_tongue,
            'pause': self.btn_pause
        }
        
        for name, rect in buttons.items():
            if rect.collidepoint(x, y):
                self.state[name] = True
                self.active_touches[touch_id] = name
                return

    def get_state(self):
        return self.state

    def hit_test(self, pos):
        x, y = pos
        # Check all UI buttons
        buttons = [self.btn_left, self.btn_right, self.btn_up, self.btn_down, 
                   self.btn_jump, self.btn_grapple, self.btn_tongue, self.btn_pause]
        for btn in buttons:
            if btn.collidepoint(x, y):
                return True
        return False
