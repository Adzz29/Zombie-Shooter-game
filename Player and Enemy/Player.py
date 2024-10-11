try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

from Enemy import Enemy

# CANVAS 
WIDTH = 500
HEIGHT = 500
                
"""# SPRITESHEET
SHEET_WIDTH = 1440
SHEET_HEIGHT = 1480
SHEET_COLUMNS = 6
SHEET_ROWS = 5
IMG = "Player and Player\TopDown_zombies.pdf"""

# Controls vector scaling for player
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def get_p(self):
        return (self.x, self.y)
    
    
    def add(self, other):
        self.x += other.x
        self.y += other.y
        
    # Multiplies the vector by a scalar
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def __mul__(self, k):
        return self.copy().multiply(k)
    

# class construct for player instance
class Player:
    def __init__(self, pos, radius=10):
        self.player_health = 5
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
        self.colour = 'White'

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, self.colour, self.colour)
        
    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)

class Mouse:
    def __init__(self):
        self.mouse_pos = None

    def current_pos(self):
        return self.mouse_pos
        
    def mouse_handler(self, canvas_pos):
        self.mouse_pos = canvas_pos
    
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False
        self.up = False
        self.down = False

    def keyDown(self, key):
        if key == simplegui.KEY_MAP['d']:
            self.right = True
        elif key == simplegui.KEY_MAP['a']:
            self.left = True
        elif key == simplegui.KEY_MAP['w']:
            self.up = True
        elif key == simplegui.KEY_MAP['s']:
            self.down = True

    def keyUp(self, key):
        if key == simplegui.KEY_MAP['d']:
            self.right = False
        elif key == simplegui.KEY_MAP['a']:
            self.left = False
        elif key == simplegui.KEY_MAP['w']:
            self.up = False
        elif key == simplegui.KEY_MAP['s']:
            self.down = False

# class contruct for player interaction and animation control
class Interaction:
    def __init__(self, player, keyboard, mouse):
        self.player = player
        self.keyboard = keyboard
        self.mouse = mouse

    def update(self):
        if self.player.pos.x > WIDTH:
            self.player.pos.x = 1
        elif self.player.pos.x < 0:
            self.player.pos.x = WIDTH - 1
        elif self.player.pos.y > HEIGHT:
            self.player.pos.y = 0
        elif self.player.pos.y < 0:
            self.player.pos.y = HEIGHT - 1 
        
        self.player.vel = Vector()  # Reset velocity before calculating new velocity
        
        if self.keyboard.right:
            self.player.vel.add(Vector(4, 0))
        if self.keyboard.left:
            self.player.vel.add(Vector(-4, 0))
        if self.keyboard.up: 
            self.player.vel.add(Vector(0, -4))
        if self.keyboard.down:
            self.player.vel.add(Vector(0, 4))

        # Diagonal movement
        if self.keyboard.up and self.keyboard.right:
            self.player.vel = Vector(4, -3)
        elif self.keyboard.up and self.keyboard.left:
            self.player.vel = Vector(-4, -3)
        elif self.keyboard.down and self.keyboard.right:
            self.player.vel = Vector(4, 3)
        elif self.keyboard.down and self.keyboard.left:
            self.player.vel = Vector(-4, 3)

        current_mouse = self.mouse.current_pos()

        player_hit = False
        # Avoid enemy overlap
        for i, enemy1 in enumerate(Enemy.enemy_list):
            for j, enemy2 in enumerate(Enemy.enemy_list):
                if i != j:  # Avoid checking the same enemy against itself
                    enemy1.avoid_overlap(enemy2)

        # Check collision between player and enemies
        for enemy in Enemy.enemy_list:
            if enemy.check_collision(self.player):
                # Handle collision here
                player_hit = True

        if player_hit:
                print("Player collided with enemy!")



mse = Mouse()
kbd = Keyboard()
player = Player(Vector(WIDTH/2, HEIGHT/2), 40)
inter = Interaction(player, kbd, mse)

# Enemies objects / balls
enemy1 = Enemy(Vector(WIDTH/3, HEIGHT/3))
enemy2 = Enemy(Vector(2 * WIDTH/3, HEIGHT/3))
enemy3 = Enemy(Vector(WIDTH/2, 2 * HEIGHT/3))

def draw(canvas):
    inter.update()
    player.update()
    player.draw(canvas)

    enemy1.update(player.pos)
    enemy1.draw(canvas)
    enemy2.update(player.pos)
    enemy2.draw(canvas)
    enemy3.update(player.pos)
    enemy3.draw(canvas)


frame = simplegui.create_frame('Player', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(kbd.keyDown)
frame.set_keyup_handler(kbd.keyUp)
frame.start()