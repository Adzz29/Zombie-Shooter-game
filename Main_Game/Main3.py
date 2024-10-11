try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import math
import random
import time

# Game settings
WIDTH = 850
HEIGHT = 500
gravity = 0.5
bullet_speed = 10
current_screen = 'menu'

# Menu music
menu_music_path = "Menu_Music.wav"

# Add a global variable to track menu music status
menu_music_playing = False

# Load the menu music
menu_music = simplegui.load_sound(menu_music_path)

# Load game_over image
game_over_image = simplegui.load_image('https://pressstart.vip/images/uploads/assets/foggy.png')

# Load menu background image
menu_background_image = simplegui.load_image('https://pressstart.vip/images/uploads/assets/graveyard.png')

# Load background sprite
background_sprite = simplegui.load_image('Main_Game\Screens\Presentation1.pptx')

# End screen buttons
game_over_button_positions = {
    'restart': ((WIDTH / 2, HEIGHT / 2 + 55), (200, 40)),
    'exit': ((WIDTH / 2, HEIGHT / 2 + 100), (200, 40))
}

# Menu button positions and sizes
button_positions = {
    'start': ((WIDTH / 2, HEIGHT / 2 - 30), (200, 40)),
    'settings': ((WIDTH / 2, HEIGHT / 2 + 20), (200, 40)),
    'exit': ((WIDTH / 2, HEIGHT / 2 + 70), (200, 40))
}

# Function to play menu music
def play_menu_music():
    global menu_music
    if menu_music:
        menu_music.set_volume(1.0)  # Set the volume to 1
        menu_music.rewind()  # Rewind the music to the beginning
        menu_music.play()
        print("Menu music is playing...")
    else:
        print("Menu music is not loaded or initialized properly.")

# Function to stop menu music
def stop_menu_music():
    menu_music.stop()

# Function to draw buttons
def draw_button(canvas, position, size, text, button_color):
    canvas.draw_polygon(
        [(position[0] - size[0] / 2, position[1] - size[1] / 2),
         (position[0] + size[0] / 2, position[1] - size[1] / 2),
         (position[0] + size[0] / 2, position[1] + size[1] / 2),
         (position[0] - size[0] / 2, position[1] + size[1] / 2)], 2, 'White', button_color)
    text_width = frame.get_canvas_textwidth(text, 24)
    canvas.draw_text(text, [position[0] - text_width / 2, position[1] + 6], 24, 'White')

# Mouse click handler
def mouseclick(pos):
    global current_screen, game_over
    if current_screen == 'menu':
        # Handle clicks on buttons only if on the menu screen
        for button, (position, size) in button_positions.items():
            if position[0] - size[0] / 2 <= pos[0] <= position[0] + size[0] / 2 and \
                position[1] - size[1] / 2 <= pos[1] <= position[1] + size[1] / 2:
                if button == 'start':
                    current_screen = 'game'
                    # Further code to start the game
                elif button == 'settings':
                    # Handle settings
                    current_screen = 'settings'
                elif button == 'exit':
                    frame.stop()  # Stop the game/frame
    elif current_screen == 'settings':
        # Handle clicks on buttons only if on the settings screen
        button_width = 100
        button_height = 40
        button_pos = (WIDTH / 2, HEIGHT - 30)
        if button_pos[0] - button_width / 2 <= pos[0] <= button_pos[0] + button_width / 2 and \
            button_pos[1] - button_height / 2 <= pos[1] <= button_pos[1] + button_height / 2:
            current_screen = 'menu'  # Switch back to the menu screen
    elif game_over:
        # Handle clicks on buttons only if on the game over screen
        restart_pos, restart_size = game_over_button_positions['restart']
        if restart_pos[0] - restart_size[0] / 2 <= pos[0] <= restart_pos[0] + restart_size[0] / 2 and \
           restart_pos[1] - restart_size[1] / 2 <= pos[1] <= restart_pos[1] + restart_size[1] / 2:
            # Reset game state as needed
            game_over = False
            current_screen = 'menu'  # Change current_screen back to 'menu' to go back to the main menu
            # Reset other game elements to their initial state as needed
            player.player_health = 5
            player.pos = Vector(WIDTH / 2, HEIGHT - 80)
            player.vel = Vector()
            player.bullets = []
            for enemy in enemies:
                enemy.pos = Vector(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 200))
            return
        exit_pos, exit_size = game_over_button_positions['exit']
        if exit_pos[0] - exit_size[0] / 2 <= pos[0] <= exit_pos[0] + exit_size[0] / 2 and \
           exit_pos[1] - exit_size[1] / 2 <= pos[1] <= exit_pos[1] + exit_size[1] / 2:
            frame.stop()  # Stop the game/frame


# Drawing handler
def draw(canvas):
    if current_screen == 'menu':
        draw_menu(canvas)
    elif current_screen == 'game':
        draw_game(canvas)
    elif current_screen == 'settings':
        draw_settings(canvas)

def draw_settings(canvas):
    # Draw black background
    canvas.draw_polygon([(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)], 1, 'Black', 'Black')

    # Draw purple box at the top
    box_width = WIDTH - 20  # Adjust the box width as needed
    box_height = 50
    box_top_left = (10, 10)
    box_bottom_right = (box_top_left[0] + box_width, box_top_left[1] + box_height)
    canvas.draw_polygon([box_top_left, (box_bottom_right[0], box_top_left[1]),
                         box_bottom_right, (box_top_left[0], box_bottom_right[1])],
                        2, 'White', 'Purple')

    # Draw white text inside the box
    text = "Settings"
    text_width = frame.get_canvas_textwidth(text, 24)
    canvas.draw_text(text, ((WIDTH - text_width) / 2, box_top_left[1] + box_height * 0.7), 24, 'White')

    # Draw return button at the bottom
    button_width = 100
    button_height = 40
    button_pos = (WIDTH / 2, HEIGHT - 30)
    canvas.draw_polygon([(button_pos[0] - button_width / 2, button_pos[1] - button_height / 2),
                         (button_pos[0] + button_width / 2, button_pos[1] - button_height / 2),
                         (button_pos[0] + button_width / 2, button_pos[1] + button_height / 2),
                         (button_pos[0] - button_width / 2, button_pos[1] + button_height / 2)],
                        2, 'White', 'Red')
    text = "Return"
    text_width = frame.get_canvas_textwidth(text, 24)
    canvas.draw_text(text, (button_pos[0] - text_width / 2, button_pos[1] + 6), 24, 'White')


def draw_menu(canvas):
    global menu_music_playing
    canvas.draw_image(menu_background_image, 
                      (menu_background_image.get_width() / 2, menu_background_image.get_height() / 2), 
                      (menu_background_image.get_width(), menu_background_image.get_height()), 
                      (WIDTH / 2, HEIGHT / 2), 
                      (WIDTH, HEIGHT))
    draw_button(canvas, button_positions['start'][0], button_positions['start'][1], 'Start', 'Green')
    draw_button(canvas, button_positions['settings'][0], button_positions['settings'][1], 'Settings', 'Purple')
    draw_button(canvas, button_positions['exit'][0], button_positions['exit'][1], 'Exit', 'Red')
    
    # Play menu music only if it's not already playing
    if not menu_music_playing:
        menu_music.set_volume(1.0)  # Set the volume to 1
        menu_music.play()
        menu_music_playing = True

    # Stop menu music if it's playing when exiting the menu screen
    if current_screen != 'menu' and menu_music_playing:
        menu_music.stop()
        menu_music_playing = False


# Vector class for position and velocity
class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def get_p(self):
        return (self.x, self.y)
    
    def add(self, other):
        self.x += other.x
        self.y += other.y
        
    def multiply(self, k):
        self.x *= k
        self.y *= k
        return self

    def copy(self):
        return Vector(self.x, self.y)

# Bullet class for player shooting
class Bullet:
    def __init__(self, position, direction):
        self.position = position.copy()
        self.direction = direction

    def update(self):
        self.position.x += bullet_speed * self.direction

    def draw(self, canvas):
        canvas.draw_circle(self.position.get_p(), 5, 1, 'White', 'White')

# Player class including jump and shoot
class Player:
    def __init__(self, pos, radius=10):
        self.player_health = 5
        self.immune_timer = 0  # Initialize immune timer
        self.pos = pos
        self.vel = Vector()
        self.radius = max(radius, 10)
        self.colour = 'White'
        self.bullets = []
        self.on_ground = True


    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, self.colour, self.colour)
        for bullet in self.bullets:
            bullet.draw(canvas)

    def update(self):
        self.pos.add(self.vel)
        self.vel.multiply(0.85)
        self.vel.y += gravity
        
        if self.pos.y >= HEIGHT - self.radius:
            self.pos.y = HEIGHT - self.radius
            self.vel.y = 0
            self.on_ground = True

        for bullet in list(self.bullets):
            bullet.update()
            if bullet.position.x < 0 or bullet.position.x > WIDTH:
                self.bullets.remove(bullet)

    def jump(self):
        if self.on_ground:
            self.vel.y = -10
            self.on_ground = False

    def shoot(self):
        direction = -1 if kbd.left else 1
        bullet_position = Vector(self.pos.x + direction * 20, self.pos.y)
        self.bullets.append(Bullet(bullet_position, direction))

    def respawn(self):
        self.pos = Vector(WIDTH / 2, HEIGHT - 80)  # Set spawn point


# Keyboard input handling
class Keyboard:
    def __init__(self):
        self.right = False
        self.left = False

    def key_down(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = True
        elif key == simplegui.KEY_MAP['left']:
            self.left = True

    def key_up(self, key):
        if key == simplegui.KEY_MAP['right']:
            self.right = False
        elif key == simplegui.KEY_MAP['left']:
            self.left = False

# Enemy class
class Enemy:
    def __init__(self, pos, radius=8):
        self.pos = pos
        self.enemy_health = 3
        self.vel = Vector()
        self.radius = radius
        self.colour = 'Red'

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, self.colour, self.colour)
        
    def update(self):
        direction = Vector(player.pos.x - self.pos.x, player.pos.y - self.pos.y)
        direction.multiply(0.01) # Control Enemy Speed
        self.vel = direction
        self.pos.add(self.vel)
    
    def check_collision(self, other):
        distance = math.sqrt((self.pos.x - other.pos.x)**2 + (self.pos.y - other.pos.y)**2)
        return distance <= self.radius + other.radius

# Interaction class to manage interactions between game objects
class Interaction:
    def respawn(player):
        player.pos = Player(Vector(WIDTH / 2, HEIGHT - 80), 40)

    # Spawn Point, Enemy collision and Immunity Func
    def handle_player_enemy_collision(player, enemy, spawn_point):
        if player.immune_timer > 0:  # Check if player is immune
            player.immune_timer -= 1  
            return False  # Player survives and can't be hit by enemies
        
        if player.player_health > 0 and enemy.check_collision(player):
            player.player_health -= 1
            player.pos = spawn_point  # Reset player pos to spawn point
            print("Player Health:", player.player_health)
            
            if player.player_health <= 0:
                # Player dies
                player.immune_timer = 200
                return True
            else:
                player.immune_timer = 200  
                return False

        return False 


    def handle_bullet_enemy_collision(bullet, enemy):
        for enemy in enemies:
            if enemy.check_collision(bullet):
                enemy.enemy_health -= 1
                if enemy.enemy_health <= 0:
                    enemies.remove(enemy)

# Game state
game_over = False

# List to manage all enemies
enemies = [Enemy(Vector(100, 100), 20), Enemy(Vector(700, 100), 20)]

# Initialize game objects
kbd = Keyboard()
player = Player(Vector(WIDTH / 2, HEIGHT - 80), 40)

def draw_game(canvas):
    global game_over
    if not game_over:
        canvas.draw_image(background_sprite, 
                          (background_sprite.get_width() // 2, background_sprite.get_height() // 2),  
                          (background_sprite.get_width(), background_sprite.get_height()),          
                          (WIDTH // 2, HEIGHT // 2),                                   
                          (WIDTH, HEIGHT))
        
        if kbd.right:
            player.vel.x = 2
        elif kbd.left:
            player.vel.x = -2
        else:
            player.vel.x = 0
        player.update()
        player.draw(canvas)
        
        for enemy in enemies:
            enemy.update()
            enemy.draw(canvas)
            spawn_point = Vector(WIDTH / 2, HEIGHT - 80)  
            if Interaction.handle_player_enemy_collision(player, enemy, spawn_point):
                game_over = True
                print("Game Over")
                return  # leaves loop to prevent further updating/drawing
            
            # Check for bullet-enemy collisions
            for bullet in player.bullets:
                if Interaction.handle_bullet_enemy_collision(bullet, enemy):
                    # Handle collision if needed
                    pass
    else:
        # Draw game over image as background
        canvas.draw_image(game_over_image, 
                          (game_over_image.get_width() // 2, game_over_image.get_height() // 2),  
                          (game_over_image.get_width(), game_over_image.get_height()),          
                          (WIDTH // 2, HEIGHT // 2),                                   
                          (WIDTH, HEIGHT))
        
        # Draw game over text
        canvas.draw_text('Game Over', (WIDTH / 2 - 100, HEIGHT / 2), 48, 'Red')
        # Draw restart and exit buttons
        draw_button(canvas, game_over_button_positions['restart'][0], game_over_button_positions['restart'][1], 'Restart', 'Green')
        draw_button(canvas, game_over_button_positions['exit'][0], game_over_button_positions['exit'][1], 'Exit', 'Red')


# Keyboard event handlers
def key_down(key):
    kbd.key_down(key)
    if key == simplegui.KEY_MAP['up']:
        player.jump()
    elif key == simplegui.KEY_MAP['space']:
        player.shoot()

def key_up(key):
    kbd.key_up(key)

# Create the frame and set handlers
frame = simplegui.create_frame('Game', WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down)
frame.set_keyup_handler(key_up)
frame.set_mouseclick_handler(mouseclick)

# Start the game
frame.start()
play_menu_music()