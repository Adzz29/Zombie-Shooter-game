try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

# Define constants for screen size
WIDTH = 400
HEIGHT = 300
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_PADDING = 20
BUTTON_SPACING = 50  # Spacing between buttons
BACK_BUTTON_WIDTH = 100
BACK_BUTTON_HEIGHT = 50
BACK_BUTTON_POSITION = (50, HEIGHT - BACK_BUTTON_HEIGHT - 20)  # Example position, adjust as needed
PAUSE_image_url = 'https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-pause-512.png'  # Replace this with the actual URL
PAUSE_image = simplegui.load_image(PAUSE_image_url)
PAUSE_WIDTH = 40  # Smaller width
PAUSE_HEIGHT = 40  # Smaller height
PAUSE_POSITION = (0, 0)  # Slightly away from the corner for visibility
current_screen = 'main'  # Default screen when the program starts
last_screen = None  # Initialize with the main menu draw handler as the default last screen
in_game = False
show_menu = False  # Initially, do not show the menu
menu_music = simplegui.load_sound('Menu_Music.mp3')
is_music_playing = False
menu_music.set_volume(1.0)

# Define text for buttons
start_game_text = "Start Game"
settings_text = "Settings"
exit_text = "Exit"

# Function to handle playing music
def play_music():
    global is_music_playing
    if not is_music_playing:
        menu_music.play()
        is_music_playing = True
        
# Function to handle pausing music
def pause_music():
    global is_music_playing
    if is_music_playing:
        menu_music.pause()  # or menu_music.rewind() to stop and reset its position
        is_music_playing = False


# Handler to draw on canvas
def draw(canvas):
    global current_screen, is_music_playing
    # Define text sizes and vertical adjustment
    text_size = 18
    text_vertical_adjust = -5  # Adjust this value to move text higher up

    # Calculate the vertical text position (adjusted)
    text_vertical_pos = HEIGHT/2 - BUTTON_PADDING - BUTTON_HEIGHT/2 + text_size / 2 + text_vertical_adjust

    # Get the width of the text for centering calculation
    text_width_start_game = frame.get_canvas_textwidth(start_game_text, text_size)
    text_width_settings = frame.get_canvas_textwidth(settings_text, text_size)
    text_width_exit = frame.get_canvas_textwidth(exit_text, text_size)

    # Draw Start Game button
    start_game_text_pos = ((WIDTH/2 - BUTTON_WIDTH - BUTTON_SPACING) + (BUTTON_WIDTH - text_width_start_game) / 2,
                        text_vertical_pos)
    canvas.draw_polygon([(WIDTH/2 - BUTTON_WIDTH - BUTTON_SPACING, HEIGHT/2 - BUTTON_PADDING),
                        (WIDTH/2 - BUTTON_SPACING, HEIGHT/2 - BUTTON_PADDING),
                        (WIDTH/2 - BUTTON_SPACING, HEIGHT/2 - BUTTON_PADDING - BUTTON_HEIGHT),
                        (WIDTH/2 - BUTTON_WIDTH - BUTTON_SPACING, HEIGHT/2 - BUTTON_PADDING - BUTTON_HEIGHT)],
                        2, 'White', 'Green')
    canvas.draw_text(start_game_text, start_game_text_pos, text_size, 'White')
    
    # Draw Settings button
    settings_text_pos = ((WIDTH/2 - BUTTON_WIDTH/2) + (BUTTON_WIDTH - text_width_settings) / 2,
                        text_vertical_pos)
    canvas.draw_polygon([(WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 - BUTTON_PADDING),
                        (WIDTH/2 + BUTTON_WIDTH/2, HEIGHT/2 - BUTTON_PADDING),
                        (WIDTH/2 + BUTTON_WIDTH/2, HEIGHT/2 - BUTTON_PADDING - BUTTON_HEIGHT),
                        (WIDTH/2 - BUTTON_WIDTH/2, HEIGHT/2 - BUTTON_PADDING - BUTTON_HEIGHT)],
                        2, 'White', 'Blue')
    canvas.draw_text(settings_text, settings_text_pos, text_size, 'White')
    
    # Draw Exit button
    exit_text_pos = ((WIDTH/2 + BUTTON_SPACING) + (BUTTON_WIDTH - text_width_exit) / 2,
                    text_vertical_pos)
    canvas.draw_polygon([(WIDTH/2 + BUTTON_SPACING, HEIGHT/2 - BUTTON_PADDING),
                        (WIDTH/2 + BUTTON_WIDTH + BUTTON_SPACING, HEIGHT/2 - BUTTON_PADDING),
                        (WIDTH/2 + BUTTON_WIDTH + BUTTON_SPACING, HEIGHT/2 - BUTTON_PADDING - BUTTON_HEIGHT),
                        (WIDTH/2 + BUTTON_SPACING, HEIGHT/2 - BUTTON_PADDING - BUTTON_HEIGHT)],
                        2, 'White', 'Red')
    canvas.draw_text(exit_text, exit_text_pos, text_size, 'White')
    if current_screen == 'main':
        if not is_music_playing:
            menu_music.play()
            is_music_playing = True
    else:
        if is_music_playing:
            menu_music.pause()  # or menu_music.rewind() to stop and reset its position
            is_music_playing = False

def show_main_menu():
    global show_menu
    show_menu = False  # Ensure the menu is hidden when showing the main menu
    frame.set_draw_handler(draw)  # Set the draw handler back to the main menu

def draw_settings(canvas):
    canvas.draw_text("Settings Page", (WIDTH / 4, HEIGHT / 4), 24, 'White')
    # Draw "Back" button
    back_button_center = (WIDTH / 2, HEIGHT - 50)
    canvas.draw_polygon(
        [(back_button_center[0] - BACK_BUTTON_WIDTH / 2, back_button_center[1] - BACK_BUTTON_HEIGHT / 2),
         (back_button_center[0] + BACK_BUTTON_WIDTH / 2, back_button_center[1] - BACK_BUTTON_HEIGHT / 2),
         (back_button_center[0] + BACK_BUTTON_WIDTH / 2, back_button_center[1] + BACK_BUTTON_HEIGHT / 2),
         (back_button_center[0] - BACK_BUTTON_WIDTH / 2, back_button_center[1] + BACK_BUTTON_HEIGHT / 2)],
        1, 'Black', 'LightGray')
    canvas.draw_text("Back", 
                     (back_button_center[0] - frame.get_canvas_textwidth("Back", 24) / 2, back_button_center[1] + 6), 
                     24, 'Black')



def draw_game(canvas):
    # Draw the game background
    canvas.draw_image(game_image, 
                      (game_image.get_width() / 2, game_image.get_height() / 2), 
                      (game_image.get_width(), game_image.get_height()), 
                      (WIDTH / 2, HEIGHT / 2), 
                      (WIDTH, HEIGHT))

    # Draw the smaller PAUSE with red background
    canvas.draw_polygon(
        [(PAUSE_POSITION[0], PAUSE_POSITION[1]),
         (PAUSE_POSITION[0] + PAUSE_WIDTH, PAUSE_POSITION[1]),
         (PAUSE_POSITION[0] + PAUSE_WIDTH, PAUSE_POSITION[1] + PAUSE_HEIGHT),
         (PAUSE_POSITION[0], PAUSE_POSITION[1] + PAUSE_HEIGHT)],
        1, 'Black', 'Red')

    canvas.draw_image(PAUSE_image, 
                      (PAUSE_image.get_width() / 2, PAUSE_image.get_height() / 2), 
                      (PAUSE_image.get_width(), PAUSE_image.get_height()), 
                      (PAUSE_POSITION[0] + PAUSE_WIDTH / 2, PAUSE_POSITION[1] + PAUSE_HEIGHT / 2), 
                      (PAUSE_WIDTH, PAUSE_HEIGHT))

    # If show_menu is True, draw the menu buttons
    if show_menu:
        # Calculate center positions for the buttons
        menu_center_x = WIDTH / 2
        menu_center_y = HEIGHT / 2 - BUTTON_HEIGHT - BUTTON_SPACING / 2
        settings_center_y = HEIGHT / 2
        start_center_y = HEIGHT / 2 + BUTTON_HEIGHT + BUTTON_SPACING / 2

        # Menu button
        draw_centered_button(canvas, "Menu", menu_center_x, menu_center_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        # Settings button
        draw_centered_button(canvas, "Settings", menu_center_x, settings_center_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        # Start button
        draw_centered_button(canvas, "Start", menu_center_x, start_center_y, BUTTON_WIDTH, BUTTON_HEIGHT)

def draw_centered_button(canvas, text, center_x, center_y, width, height):
    canvas.draw_polygon(
        [(center_x - width / 2, center_y - height / 2),
         (center_x + width / 2, center_y - height / 2),
         (center_x + width / 2, center_y + height / 2),
         (center_x - width / 2, center_y + height / 2)],
        1, 'Black', 'LightGray')
    canvas.draw_text(text, 
                     (center_x - frame.get_canvas_textwidth(text, 24) / 2, center_y + 6), 
                     24, 'Black')


def transition_to_settings():
    global current_screen, last_screen, in_game
    if current_screen == 'game' and show_menu:
        # From the pause menu
        last_screen = 'game'
    else:
        # From the main menu
        last_screen = 'main'
    current_screen = 'settings'
    frame.set_draw_handler(draw_settings)




def click(pos):
    global current_screen, last_screen, show_menu, in_game

    x, y = pos
    
    # Assume back_button_clicked(x, y) is a function you've defined to check if the back button is clicked
    if current_screen == 'settings' and back_button_clicked(x, y):
        if last_screen == 'game':
            current_screen = 'game'
            show_menu = True  # Show the pause menu again if we're returning to the game
            frame.set_draw_handler(draw_game)
        else:
            current_screen = 'main'
            show_menu = False
            frame.set_draw_handler(draw)  # Assuming 'draw' is your main menu draw handler
        return
    
    # Toggle menu display if the PAUSE was clicked
    if PAUSE_POSITION[0] <= x <= PAUSE_POSITION[0] + PAUSE_WIDTH and PAUSE_POSITION[1] <= y <= PAUSE_POSITION[1] + PAUSE_HEIGHT:
        show_menu = not show_menu
        return  # Return early to prevent other click actions while toggling the menu

    
    # If the menu is shown, check if one of the menu buttons is clicked
    if show_menu:
        # Calculate button positions dynamically
        menu_center_x = WIDTH / 2
        menu_y_positions = {
            "Menu": HEIGHT / 2 - BUTTON_HEIGHT - BUTTON_SPACING / 2,
            "Settings": HEIGHT / 2,
            "Start": HEIGHT / 2 + BUTTON_HEIGHT + BUTTON_SPACING / 2,
        }
        
        # Check which button was clicked
        for button_text, button_y in menu_y_positions.items():
            if menu_center_x - BUTTON_WIDTH / 2 <= x <= menu_center_x + BUTTON_WIDTH / 2 and button_y - BUTTON_HEIGHT / 2 <= y <= button_y + BUTTON_HEIGHT / 2:
                print(f"{button_text} button clicked")
                if button_text == "Menu":
                    show_main_menu()
                elif button_text == "Start":
                    # Hide the menu and continue the game (or start it)
                    show_menu = False
                elif button_text == "Settings":
                    # Implement settings screen logic
                    frame.set_draw_handler(draw_settings)
                return  # Once a button click is handled, no need to check further
    # Original click logic for the main menu
    if not show_menu:  # Only check these if the menu overlay is not showing
        # Start Game button logic
        if (WIDTH / 2 - BUTTON_WIDTH - BUTTON_SPACING) <= x <= (WIDTH / 2 - BUTTON_SPACING) and (HEIGHT / 2 - BUTTON_PADDING - BUTTON_HEIGHT) <= y <= (HEIGHT / 2 - BUTTON_PADDING):
            print("Start game button clicked")
            frame.set_draw_handler(draw_game)
        # Settings button logic from the main menu
        elif (WIDTH / 2 - BUTTON_WIDTH / 2) <= x <= (WIDTH / 2 + BUTTON_WIDTH / 2) and (HEIGHT / 2 - BUTTON_PADDING - BUTTON_HEIGHT) <= y <= (HEIGHT / 2 - BUTTON_PADDING):
            print("Settings button clicked")
            frame.set_draw_handler(draw_settings)
        # Exit button logic
        elif (WIDTH / 2 + BUTTON_SPACING) <= x <= (WIDTH / 2 + BUTTON_WIDTH + BUTTON_SPACING) and (HEIGHT / 2 - BUTTON_PADDING - BUTTON_HEIGHT) <= y <= (HEIGHT / 2 - BUTTON_PADDING):
            print("Exit button clicked")
            # Implement exit functionality as needed

def back_button_clicked(x, y):
    back_button_center = (WIDTH / 2, HEIGHT - 50)  # Update if your back button's position differs
    return (back_button_center[0] - BACK_BUTTON_WIDTH / 2 <= x <= back_button_center[0] + BACK_BUTTON_WIDTH / 2) and \
           (back_button_center[1] - BACK_BUTTON_HEIGHT / 2 <= y <= back_button_center[1] + BACK_BUTTON_HEIGHT / 2)

    

game_image = simplegui.load_image('https://pixanna.nl/wp-content/uploads/2015/03/naturemap_14.png')

# Create a frame
frame = simplegui.create_frame("Start Screen", WIDTH, HEIGHT)

# Set background color of the frame
frame.set_canvas_background("Black")

# Assign draw handler to the frame
frame.set_draw_handler(draw)

# Assign mouse click handler to the frame
frame.set_mouseclick_handler(click)

# Start the frame
frame.start()
play_music()