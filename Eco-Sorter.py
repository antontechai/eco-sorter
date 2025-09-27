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
clock = pygame.time.Clock() # clock watching that game work with the same speed 
FPS = 60 # limit frames 


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
player_width = 128
player_height = 120

# downloading sprites of containers and scale them 
blue_bin_img = pygame.transform.scale(pygame.image.load('assets/trash_can_blue.png').convert_alpha(), (player_width, player_height))
white_bin_img = pygame.transform.scale(pygame.image.load('assets/trash_can_white.png').convert_alpha(), (player_width, player_height))
yellow_bin_img = pygame.transform.scale(pygame.image.load('assets/trash_can_yellow.png').convert_alpha(), (player_width, player_height))

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
player_x = (screen_width - player_width) // 2 # formula for centre objects. Width of screen - width of player and result / 2 and then player appear on the middle of the scrre horizontally 
player_y = screen_height - player_height - 10 # Formula to put player on the lowest border . Player staying so that his lower partw was on 10 pixels higher than lower part of the screen
player_rect = pygame.Rect(player_x, player_y, player_width, player_height) # rect it's like container of my object that contain 4 items x,y,width and height
player_speed = 12 # varibales that create setting for objects

# Set up colors for sort
player_colors = [(0, 0, 255), (0,255, 0), (139, 69, 19)] # list with 3 different colors 
current_color_index = 0 # index of current active color from list of player_colors

# Iniitial container color 
player_color = player_colors[current_color_index] # get it from variable player_colors element with index current_color_index (0,1,2) and save it to variable player_color


# Sort Structure
recycling_categories = [
    {
        "name": "Food",
        "trash_image": food_img, # picture for trash
        "bin_image": blue_bin_img, # certain container
    },
    {
        "name": "Glass",
        "trash_image": glass_img,
        "bin_image": white_bin_img,
    },
    {
        "name": "Plastic",
        "trash_image": plastic_img,
        "bin_image": yellow_bin_img
    },
]

# trash settings 
trash_width = 30
trash_height = 30

# function for creating new trash subject 
def spawn_trash(): # put code of creating the trash in seperate function, in conviniet purpose because it's neccessary to create new trash once we catch old trash or miss it, instead of repeating code we use spawn_trash()
    category_index = random.randint(0, len(recycling_categories) -1) # pick random index (0,1 or2)
    category = recycling_categories[category_index] # choose certain category for this index
    x = random.randint(0, screen_width - trash_width) # Set a random position horizontaly 
    rect = pygame.Rect(x, -trash_height, trash_width, trash_height) # Create rectangle appear above the screen: y = -trash_height)
    speed = current_trash_speed_base + random.randint(-current_trash_speed_variance, current_trash_speed_variance) # creating a speed for new cube it = the base speed +- diversity 
    speed = max(1, min(speed, trash_speed_base_cap)) # double protection. min doesn't let speed be higher than limits and max doesn't let it be lower than 1 so trash do not stop 
    return {"rect": rect, "image": category["trash_image"], "speed": speed, "correct_index": category_index} # return dictionary which contains rectange and information type. Each trash object it's dictionary which knows not only it's geometry and type but personal speed
    
trash_list = [] # creating an open list to containt here all trash objects 
trash_list.append(spawn_trash()) # object to start being immideately on the screen 

score = 0 # variables for tracking state of the game 
lives = 3
font = pygame.font.SysFont(None, 28) # insialization of fonts for output text on the screen 

# Level Based Difficulty 
level = 1 
points_per_level = 50 # each 50 points increase scores 
last_applied_level = 1 # apply changes only per level 


# Main Game  
running = True # variable "flag" while it's true game is working ????
while running: # core of the game the code inside the cycle will run again and again 
    # Rendering input
    for event in pygame.event.get(): # this command check if player took any actions with keyboard or mouse 
        if event.type == pygame.QUIT: # checking if there was closing the screen with the game 
            running = False # if yes than close the game so we stop running process of the game 
        if event.type == pygame.KEYDOWN: # checking if there were any interaction with buttons
            if event.key == pygame.K_SPACE:# if yes checking if it was with SPACE updatePlayerColor()                
                current_color_index = (current_color_index + 1) % len(player_colors)
                player_color = player_colors[current_color_index]  # update variable player_color with new color from the list 
    

        # Level progression by score 
    level = max(1, score // points_per_level + 1)
    if level > last_applied_level:
        last_applied_level = level 
        print(f"Level Up!{level}") # ????????

        if level <= level_speed_cap:
            current_trash_speed_base = min(current_trash_speed_base + level_speed_step, trash_speed_base_cap) #trash_spawn_interval_step
            trash_spawn_interval = max(trash_spawn_interval_min, trash_spawn_interval - trash_spawn_interval_step)
            if (level % 3 == 0) and (max_trash_on_screen < max_trash_on_screen_cap):
                max_trash_on_screen += 1 
   
    # Spawn new trash objects 
    trash_spawn_time += 1 # that's timer ticking each frame. When it goes to trash_spawn_interval, it creates a new trash(if on the screen there are less than limits) and than reset timer to 0
    if trash_spawn_time >= trash_spawn_interval: 
        if len(trash_list) < max_trash_on_screen:
             trash_list.append(spawn_trash())
        trash_spawn_time = 0             

# Control movements (inside cycle)                    
    keys = pygame.key.get_pressed() # ????(why this) this command checking which buttons are holding in this moment, it's better for slight movements
    if keys[pygame.K_LEFT]: # checking if left button are holding if yes then
        player_rect.x -= player_speed # we decreasing coordinat x of container on meaning of speed moving it to the left
    if keys[pygame.K_RIGHT]: # the same for the right 
            player_rect.x += player_speed # the same for the right 
    player_rect.x = max(0, min(player_rect.x, screen_width - player_rect.width))   


# Logic of player and the trash objects 
    trash_to_remove = [] # list to store trash that should be removed 
    for i, trash in enumerate(trash_list):
        # Move trash down 
        trash["rect"].y += trash["speed"]
        # Check collision with player
        if trash["rect"].colliderect(player_rect):
            correct_index = trash["correct_index"]
            if current_color_index == correct_index:
                score += 10 
                correct_sound.play() # coorrect sound
            else: 
                lives -= 1
                wrong_sound.play() # wrong sound 
            trash_to_remove.append(i) # Mark for removal 

            # New Important if dindn't catch the trash 
        elif trash["rect"].top > screen_height:
            lives -= 1 # missed< loose life 
            trash_to_remove.append(i) # mark for delete

        # Remove caught & missed trash 
    for i in reversed(trash_to_remove): 
            trash_list.pop(i)                
    
     # Checking for gaming over 
    if lives <= 0:
        running = False


    # Design 
    screen.blit(background_image, (0, 0)) # draw background 

    current_player_image = recycling_categories[current_color_index]["bin_image"] # pick sprite of container in correct color
    screen.blit(current_player_image, player_rect) # draw conatiner 

    for trash in trash_list: # draw each trash from the list 
       screen.blit(trash["image"], trash["rect"])
           
    # new visualize score and lives HUD 
    hud_text_string = f"Score: {score}   Lives: {lives}  Level: {level}"
    hud_surface = font.render(hud_text_string, True, (255, 255, 255))
    screen.blit(hud_surface, (10, 10))

    # update the screen one time at the end of cycle 
    pygame.display.flip() # Show everything thaat were drawn 
    # control FPS
    clock.tick(FPS) 

# End of the game 
pygame.quit() # when cycle while finish this command turn off all the modules from Pygame
sys.exit() # This command fully close programme 

