import pygame # connect pygame library
import sys # python library which allows programme to start and end correctly 
import random # library 


# Insilizzation Pygame 
pygame.init() #always start in the beginning to start all the neccessary function Pygame

# Set up screen 
screen_width = 800   
screen_height = 600 
screen = pygame.display.set_mode((screen_width, screen_height)) # that's command create a visable screen with previous set up and we save it in variables screen 
pygame.display.set_caption("Eco-sorter") # create a title for game screen 
pygame.display.set_caption("Eco-sorter") # create a title for game screen 
clock = pygame.time.Clock() # clock watching that game work with the same speed 
FPS = 60 # limit frames 



# - - - - Settings of difficulty - - - -   
# - - - - Settings of difficulty - - - -   
# Trash Speed 
current_trash_speed_base = 4 # core of speed for all the squares  
current_trash_speed_variance = 0 # diversity of speed, change to 1 will change the speed to +-1, now 0 means all squarels fall with the same speed 
trash_speed_base_cap = 14 # limit for max speed 
level_speed_cap = 6 # Level till which speed is growing 

# Level speed step   
level_speed_step = 1 
level_speed_every = 2

# Spawn Control 
trash_spawn_time = 0 # timer, which count frames before new trash appear 
trash_spawn_interval = 100 # The lower the faster if falling. Interval of apperance, new trash appear each 150 frames
trash_spawn_interval_min = 60 # minimal line of interval, trash will not appear more often than this number of frames  
trash_spawn_interval_step = 5 # step dicreasing of spawn, with each level trash_spawn_interval will decrease to this number 

# Initial limits of objects 
max_trash_on_screen = 2 # how many trash can be on the start of the game 
max_trash_on_screen_cap = 8 # max limit of trash on the screen 



# Downloading Sounds and Sprites 
# downloading background and make it suitable with screen size 
background_image = pygame.image.load('assets/background.png').convert()
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# player settings
player_width = 88
player_height = 88

# downloading sprites of containers and scale them 
green_bin_img = pygame.transform.scale(pygame.image.load('assets/trash_can_green.png').convert_alpha(), (player_width, player_height))
white_bin_img = pygame.transform.scale(pygame.image.load('assets/trash_can_white.png').convert_alpha(), (player_width, player_height))
orange_bin_img = pygame.transform.scale(pygame.image.load('assets/trash_can_orange.png').convert_alpha(), (player_width, player_height))

# downloading sprites of trash and scale them 
trash_width = 64  # Size sprites of trash 
trash_height = 64
food_img = pygame.transform.scale(pygame.image.load('assets/food.png').convert_alpha(), (trash_width, trash_height))
glass_img = pygame.transform.scale(pygame.image.load('assets/glass.png').convert_alpha(), (trash_width, trash_height))
plastic_img = pygame.transform.scale(pygame.image.load('assets/plastic.png').convert_alpha(), (trash_width, trash_height))



# sounds
# insialization mixer for sound
pygame.mixer.init()

# Downloading sounds effect 
correct_sound = pygame.mixer.Sound('assets/correct.wav')
wrong_sound = pygame.mixer.Sound('assets/error.wav')

# set up player 
# set up player 
player_x = (screen_width - player_width) // 2 # formula for centre objects. Width of screen - width of player and result / 2 and then player appear on the middle of the scrre horizontally 
player_y = screen_height - player_height - 10 # Formula to put player on the lowest border . Player staying so that his lower partw was on 10 pixels higher than lower part of the screen
player_rect = pygame.Rect(player_x, player_y, player_width, player_height) # rect it's like container of my object that contain 4 items x,y,width and height
player_speed = 16 # varibales that create setting for objects

# Sort Structure
recycling_categories = [
    {
        "name": "Food",
        "trash_image": food_img, # picture for trash
        "bin_image": green_bin_img, # certain container
    },
    {
        "name": "Glass",
        "trash_image": glass_img,
        "bin_image": white_bin_img,
    },
    {
        "name": "Plastic",
        "trash_image": plastic_img,
        "bin_image": orange_bin_img
    },
]

# trash settings 
# trash settings 
trash_width = 30
trash_height = 30

# function for creating new trash subject 
# function for creating new trash subject 
def spawn_trash(): # put code of creating the trash in seperate function, in conviniet purpose because it's neccessary to create new trash once we catch old trash or miss it, instead of repeating code we use spawn_trash()
    category_index = random.randint(0, len(recycling_categories) -1) # pick random index (0,1 or2)
    category = recycling_categories[category_index] # choose certain category for this index
    x = random.randint(0, screen_width - trash_width) # Set a random position horizontaly 
    rect = pygame.Rect(x, -trash_height, trash_width, trash_height) # Create rectangle appear above the screen: y = -trash_height)
    speed = current_trash_speed_base + random.randint(-current_trash_speed_variance, current_trash_speed_variance) # creating a speed for new cube it = the base speed +- diversity 
    speed = max(1, min(speed, trash_speed_base_cap)) # double protection. min doesn't let speed be higher than limits and max doesn't let it be lower than 1 so trash do not stop 
    return {"rect": rect, "image": category["trash_image"], "speed": speed, "correct_index": category_index} # return dictionary which contains rectange and information type. Each trash object it's dictionary which knows not only it's geometry and type but personal speed
    
def load_high_score(): # read score from file highscore.txt if no file or emty return
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0 
    
def save_high_score(new_high_score): # note record score in the same file 
    with open("highscore.txt", "w") as f:
        f.write(str(new_high_score))
trash_list = [] # creating an open list to containt here all trash objects 
trash_list.append(spawn_trash()) # object to start being immideately on the screen 

score = 0 # variables for tracking state of the game 
lives = 3
font = pygame.font.SysFont(None, 36) # insialization of fonts for output text on the screen
font_large = pygame.font.SysFont(None, 72) # text for game over screen 
font_medium = pygame.font.SysFont(None, 48) # for buttons and text 

# Level Based Difficulty 
level = 1 
points_per_level = 50 # each 50 points increase scores 
last_applied_level = 1 # apply changes only per level 


# Main Game  
def draw_text(text, font, color, surface, x, y):
    # support function to draw text
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def main_menu():
    # function of main menu
    while True:
        screen.blit(background_image, (0, 0))
        draw_text("Eco-Sorter", font_large, (255, 255, 255), screen, screen_width / 2, screen_height / 4)
        
        mx, my = pygame.mouse.get_pos()

        # Draw button Start
        button_start = pygame.Rect(screen_width / 2 - 100, screen_height / 2 - 25, 200, 50)
        pygame.draw.rect(screen, (0, 150, 0), button_start)
        draw_text("Start Game", font_medium, (255, 255, 255), screen, screen_width / 2, screen_height / 2)

        # Checking pressing the button 
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked = True
        
        if button_start.collidepoint((mx, my)):
            if clicked:
                return # Leave the menu and start again 

        pygame.display.update()
        clock.tick(FPS)

def game_over_screen(final_score, high_score):
    # function of the screen "Game over"
    while True:
        screen.blit(background_image, (0, 0))
        draw_text("Game Over", font_large, (200, 0, 0), screen, screen_width / 2, screen_height / 4)
        draw_text(f"Your Score: {final_score}", font_medium, (255, 255, 255), screen, screen_width / 2, screen_height / 2)
        draw_text(f"High Score: {high_score}", font_medium, (255, 255, 0), screen, screen_width / 2, screen_height / 2 + 60)
        draw_text("Press any key to return to menu", font, (255, 255, 255), screen, screen_width / 2, screen_height * 3 / 4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return # Leave to the main menu 

        pygame.display.update()
        clock.tick(FPS)

def game_loop():
    # Main game loop
    # Reset all game variables at the start of a new game
    score = 0
    lives = 3
    level = 1
    last_applied_level = 1
    trash_list.clear()
    trash_list.append(spawn_trash())
    current_color_index = 0 
    
    # Variables for pause 
    paused = False
    
    running = True
    while running:
        # BLOCK 1: EVENT PROCESSING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_color_index = (current_color_index + 1) % len(recycling_categories)
                if event.key == pygame.K_ESCAPE: # Letter ESC for exit
                    paused = not paused

        # If game on pause skip all game logic 
        if paused:
            # Drawing screen of pause and move to the next frame 
            draw_text("PAUSED", font_large, (255, 255, 0), screen, screen_width / 2, screen_height / 2)
            pygame.display.update()
            clock.tick(FPS)
            continue # Skip the rest of the cycle 

        # BLOCK 2: GAME LOGIC
        # here's main code of difficulty, spawn movement and collisisons
        level = max(1, score // points_per_level + 1)
        if level > last_applied_level:
            last_applied_level = level
            if level <= level_speed_cap:
                globals()['current_trash_speed_base'] = min(current_trash_speed_base + level_speed_step, trash_speed_base_cap)
            globals()['trash_spawn_interval'] = max(trash_spawn_interval_min, trash_spawn_interval - trash_spawn_interval_step)
            if (level % 3 == 0) and globals()['max_trash_on_screen'] < max_trash_on_screen_cap:
                globals()['max_trash_on_screen'] += 1
        
        globals()['trash_spawn_time'] += 1
        if trash_spawn_time >= trash_spawn_interval:
            if len(trash_list) < max_trash_on_screen:
                trash_list.append(spawn_trash())
            globals()['trash_spawn_time'] = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]: player_rect.x += player_speed
        player_rect.x = max(0, min(player_rect.x, screen_width - player_rect.width))

        trash_to_remove = []
        for i, trash in enumerate(trash_list):
            trash["rect"].y += trash["speed"]
            if trash["rect"].colliderect(player_rect):
                if current_color_index == trash["correct_index"]:
                    score += 10
                    correct_sound.play()
                else:
                    lives -= 1
                    wrong_sound.play()
                trash_to_remove.append(i)
            elif trash["rect"].top > screen_height:
                lives -= 1
                trash_to_remove.append(i)

        for i in reversed(trash_to_remove):
            trash_list.pop(i)

        if lives <= 0:
            running = False # End of game cycle 
        # BLOCK 3: DRAWING
        screen.blit(background_image, (0, 0))
        current_player_image = recycling_categories[current_color_index]["bin_image"]
        screen.blit(current_player_image, player_rect)
        for trash in trash_list:
            screen.blit(trash["image"], trash["rect"])

        hud_text_string = f"Score: {score}   Lives: {lives}   Level: {level}"
        hud_surface = font.render(hud_text_string, True, (255, 255, 255))
        screen.blit(hud_surface, (10, 10))
        
        pygame.display.update()
        clock.tick(FPS)
        
    return score # return final score when the game is over 


# THE GAME'S MAIN "CONTROLLER"
high_score = load_high_score()
while True:
    main_menu() # show menu, wait for start 
    final_score = game_loop() # Start the game and when finished get the score 
    
    if final_score > high_score:
        high_score = final_score
        save_high_score(high_score)
        
    game_over_screen(final_score, high_score) # Show the screen of end of the game 