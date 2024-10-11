# Controls vector scaling for player
import math


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


class Enemy:
    enemy_list = []

    def __init__(self, pos, radius=8):
        self.pos = pos
        self.vel = Vector()
        self.radius = radius
        self.colour = 'Red'

        self.enemy_list.append(self)

    def draw(self, canvas):
        canvas.draw_circle(self.pos.get_p(), self.radius, 1, self.colour, self.colour)
        
    def update(self, player_pos):
        direction = Vector(player_pos.x - self.pos.x, player_pos.y - self.pos.y)
        direction.multiply(0.02)  # Adjust the speed of the enemy
        self.vel = direction
        self.pos.add(self.vel)

    def check_collision(self, other):
        distance = math.sqrt((self.pos.x - other.pos.x)**2 + (self.pos.y - other.pos.y)**2)
        if distance <= self.radius + other.radius:
            return True
        else:
            return False

    def avoid_overlap(self, other):
        distance = math.sqrt((self.pos.x - other.pos.x)**2 + (self.pos.y - other.pos.y)**2)
        min_distance = self.radius + other.radius
        if distance < min_distance:
            # Calculate the direction away from the other enemy
            direction = Vector(self.pos.x - other.pos.x, self.pos.y - other.pos.y)
            direction.multiply((min_distance - distance) / distance)
            self.pos.add(direction)
    

        