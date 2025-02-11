# Task 1 and 2

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Canvas 
WIDTH = 500
HEIGHT = 500

# Spritesheet
SHEET_WIDTH = 1440
SHEET_HEIGHT = 1480
SHEET_COLUMNS = 6
SHEET_ROWS = 5
IMG = "http://www.cs.rhul.ac.uk/courses/CS1830/sprites/runnerSheet.png"
# IMG = "https://www.cs.rhul.ac.uk/courses/CS1830/sprites/explosion-spritesheet.png"
# (Explosion):
# Change rows and cols ==> 9
# Change width and heights ==> 900

class Spritesheet:
    def __init__(self, img, height, width, columns, rows):
        self.img = img
        self.height = height
        self.width = width
        self.columns = columns
        self.rows = rows
        
        
        # Calculate frame dimension
        self._init_dimensions()
        
        # Set up frame index
        self.frame_index = [0, 0]
        
    def _init_dimensions(self):
        self.frame_width = self.width / self.columns
        self.frame_height = self.height / self.rows
        self.frame_centre_x = self.frame_width / 2
        self.frame_centre_y = self.frame_height/ 2

    def next_frame(self): # Acting as the update method
        self.frame_index[0] = (self.frame_index[0] + 1) % self.columns # if reach end of columns then it resets
        if self.frame_index[0] == 0:
            self.frame_index[1] = (self.frame_index[1] + 1) % self.rows # continues changing row when 0 reached in columns
                           
    def draw(self, canvas):    	
        source_centre = (
            self.frame_width * self.frame_index[0] + self.frame_centre_x, 
            self.frame_height * self.frame_index[1] + self.frame_centre_y # selects frame centre
        )        
        source_size = (self.frame_width, self.frame_height)
        dest_centre = (250, 250)
        
        dest_size = (80, 80)
        img = simplegui.load_image(self.img)

        canvas.draw_image(img, source_centre, source_size, dest_centre, dest_size)   # draws frame selected
        
class Clock:
    def __init__(self):
        self.time = 0
                
    def tick(self):
        self.time += 1
        
    def transition(self, frame_duration):  # every second it changes frame to desired amount of the time (10)
        return self.time % frame_duration == 0
            

frame = simplegui.create_frame('Sprites', WIDTH, HEIGHT)
sheet = Spritesheet(IMG, SHEET_WIDTH, SHEET_HEIGHT, SHEET_COLUMNS, SHEET_ROWS)

clock = Clock()
      
def draw(canvas):
    clock.tick()
    if clock.transition(1): # draw_handler handles the duration of each frame screentime
        sheet.next_frame()
    sheet.draw(canvas)

frame.set_draw_handler(draw)
frame.start()