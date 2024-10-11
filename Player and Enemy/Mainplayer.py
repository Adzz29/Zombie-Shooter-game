import pygame

pygame.init() # initialise pygame

SCREEN_WIDTH = 650
SCREEN_HEIGHT = 550

window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) #create game window
pygame.display.set_caption("Zombie Shooter") #create window title

#Set frame rate
clock = pygame.time.Clock()
FPS = 60

#define game variables
gravity = 0.85


#Defining player action variables
move_left = False
move_right = False
shoot = False

# load Bullet image
bullet_img = pygame.image.load('Icons/bullet.png').convert_alpha()


#Define colours
BG = (0, 255, 128)
BLACK = (0, 0, 0)

def draw_bg():
    window.fill(BG)
    pygame.draw.line(window, BLACK, (0, 370), (SCREEN_WIDTH, 370))


# Creating player class
class Sprites(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed): 
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed 
        self.scale = scale
        self.direction = 1 #direction player is facing (right)
        self.jump = False
        self.fall_count = 0 # vel y (how long players fall)
        self.in_air = True
        self.shot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Load all animations
        self.animations = {
            'idle': self.load_animation('Player/img/Idle', 1, self.scale),
            'run': self.load_animation('Player/img/Run', 6, self.scale),
            'jump': self.load_animation('Player/img/Jump', 2, self.scale), # Assuming you have 2 jump frames
            # ... Any other animations ...
        }
        self.action = 'idle'  # Starting action
        self.frame_index = 0
        self.image = self.animations[self.action][self.frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def load_animation(self, path, num_frames, scale):
        animation_frames = []
        for i in range(num_frames):
            img_path = f'{path}/{i}.png'
            img = pygame.image.load(img_path).convert_alpha()
            img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
            animation_frames.append(img)
        return animation_frames


    def movement(self, move_left, move_right):
        #reset movement variable
        dx = 0 #change in x coordinate of player
        dy = 0 # change in y

        #assign movement variable if moving left or rightr
        if move_left:
            dx = -self.speed #negative because moving left
            self.flip = True
            self.direction = -1 #facing left
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1 #facing right

        # Jump
        if self.jump == True and self.in_air == False: # prevents double jump
            self.fall_count = -13 
            self.jump = False
            self.in_air = True

        # Adding gravity
        self.fall_count += gravity
        if self.fall_count > 10:
            self.fall_count    
        dy += self.fall_count 

        # Check collision with floor
        if self.rect.bottom + dy > 370:
            dy = 370 - self.rect.bottom 
            self.in_air = False


        #update rect position
        self.rect.x += dx
        self.rect.y += dy


    def shoot(self):
        if self.shot_cooldown == 0:
            self.shot_cooldown = 20
            bullet = Bullet(player.rect.centerx + (0.66 * player.rect.size[0] * player.direction), player.rect.centery, player.direction)
            bullet_group.add(bullet)


        
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animations[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animations[self.action]):
            self.frame_index = 0
        
        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
    
        
        
    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
    
# Animation for when dead
   # def check_alive(self):
    #    if self.health <= 0: # if health is 0 or below
     #       self.health = 0 # min health is 0, cant go lower
      #      self.speed = 0 # stop moving 
       #     self.alive = False
       ### NEED TO ADD SPRITE OF PLAYER DYING 



    def draw(self):                       #player img,   #x       #y
        window.blit(pygame.transform.flip(self.image, self.flip, False), self.rect) #Flips image in x (left and right), y axis not flip so false


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 9
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # move bullet
        self.rect.x += (self.direction * self.speed)

        # Check collision with enemy
        if pygame.sprite.spritecollide(player, bullet_group, False):
           if player.alive:
               player.health -= 10
               
               
        
        if pygame.sprite.spritecollide(enemy, bullet_group, False):
           if enemy.alive:
               enemy.health -= 20
               print(enemy.health)
               self.kill()
            



# create sprite group
bullet_group = pygame.sprite.Group()


player = Sprites(50, 250, 0.48, 3.5) #Players x,y cordinates, scale and speed
enemy = Sprites(50, 340, 0.49, 4) #Players x,y cordinates, scale and speed



run = True
while run:

    clock.tick(FPS)

    draw_bg()

    player.update_animation()
   # player.check_alive()
    player.draw()

    enemy.draw()

    #update and draw groups
    bullet_group.update()
    bullet_group.draw(window)


    #update player actions
    if player.alive:
        #Shooting bullets
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action('jump') # changes action to jumping 
        elif move_left or move_right:
            player.update_action('run') #Changes action to run(1)
        else:
            player.update_action('idle') #Changes action to idle(0)
        player.movement(move_left, move_right)

    #Event handler
    for event in pygame.event.get(): # Gets all the events happening(mouse click etc)
        if event.type == pygame.QUIT: # Quits game
            run = False

        #Keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #press left key to move left
                move_left = True
            if event.key == pygame.K_RIGHT: #press right key to move right
                move_right = True
            if event.key == pygame.K_UP and player.alive: #press up key to jump
                player.jump = True
            if event.key == pygame.K_SPACE: #press Spacebar to shoot
                shoot = True

        #Key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: #release left key
                move_left = False
            if event.key == pygame.K_RIGHT: #release right key
                move_right = False    
            if event.key == pygame.K_SPACE: #release right key
                shoot = False        
            



    pygame.display.update()

pygame.quit()
