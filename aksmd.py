# Difficulty settings 
# difficulty_start_ms = pygame.time.get_ticks()
# difficulty_level = 0
# difficulty_increase_every_ms = 20000 # increase all the 15 seconds 

# Current settings of difficulty will increase 
# current_trash_speed_min = 2
# current_trash_speed_max = 4 
# trash_speed_max_cap = 9



# Spawn new trash objects 
# trash_spawn_timer += 1 
# if trash_spawn_timer >= trash_spawn_interval:
#     if len(trash_list) < max_trash_on_screen:
#         trash_list.append(spawn_trash())
#         trash_spawn_timer = 0 

# Limitation on number of at the same time objectivs 
# max_trash_on_screen = 3
# max_trash_on_screen = 7 



# Initial position random horizontaly, on the top vertically 
# trash_x = random.randint(0, screen_width - trash_width)
# trash_y = 0
# trash_rect = pygame.Rect(trash_x, trash_y, trash_width, trash_height)
# trash_color = (255, 0, 0) # red color 
# trash_speed = 8   



# def updatePlayerColor():
#     current_color_index = (current_color_index + 1) % len(player_colors)
#     # current_color_index += 1 # in that case we switch colro inxed from 0 to 1 
#     # if current_color_index >= len(player_colors): # ???? checking if index went through list limits len(player_colors) lenght of list = 3
#     #     current_color_index = 0 # if inxed went through limits than we restart it to 0 in order to make it work as a circle 
#     player_color = player_colors[current_color_index]  # update variable player_color with new color from the list 
    



# trash = spawn_trash() # Creating a first trash while starting game 
# trash_spawn_time = 0 # new timer to control when to spawn new trash 




    # current_color_index += 1 # in that case we switch colro inxed from 0 to 1 
    # if current_color_index >= len(player_colors): # ???? checking if index went through list limits len(player_colors) lenght of list = 3
    #     current_color_index = 0 # if inxed went through limits than we restart it to 0 in order to make it work as a circle 



    # # Level progression by score 
    # level = max(1, score // points_per_level + 1)
    # if level > last_applied_level:
    #     last_applied_level = level 



    # Each 2 levels slightly increase base speed 
    # !! if (level % level_speed_every == 0) and (current_trash_speed_base < trash_speed_base_cap):
        # !! current_trash_speed_base = min(current_trash_speed_base + level_speed_step, trash_speed_base_cap)
        # !! r trash in trash_list:
          # !! trash["speed"] = min(trash["speed"] + level_speed_step, trash_speed_base_cap)

    # trash_spawn_interval = max(trash_spawn_interval_min, trash_spawn_interval - trash_spawn_interval_step) # !!

    # if (level % 3 == 0) and (max_trash_on_screen < max_trash_on_screen_cap): # !!
    #     max_trash_on_screen += 1 # !!
    # decrease interval of spawn sliglty not lower than minimum 
  
    # !! trash_spawn_interval = max(trash_spawn_interval_min, trash_spawn_interval - trash_spawn_interval_step)

    # each third level allow +1 object at the same time                 
    # !! if (level % 3 == 0) and (max_trash_on_screen < max_trash_on_screen_cap):
    #    !! max_trash_on_screen += 1  

    # Slightly increase speed of new trash 
        # if current_trash_speed_max < trash_speed_max_cap:
        #     current_trash_speed_min = min(current_trash_speed_min + 1, trash_speed_max_cap - 1)
        #     current_trash_speed_max = min(current_trash_speed_max + 1, trash_speed_max_cap)



    # Difficulty progression 
    # elapsed_ms = pygame.time.get_ticks() - difficulty_start_ms
    # new_level = elapsed_ms // difficulty_increase_every_ms
    # if new_level > difficulty_level:
    #     difficulty_level = new_level    
    #     # increase range of trash speed 
    #     current_trash_speed_min += 1
    #     current_trash_speed_max += 1 
    #     # Often spawn 
    #     if max_trash_on_screen < max_trash_on_screen_cap: 
    #         max_trash_on_screen += 1
    #         # Spawn new trash pbjects 
    # trash_spawn_time += 1 
    # if trash_spawn_time >= trash_spawn_interval:
    #     if len(trash_list) < max_trash_on_screen:
    #         trash_list.append(spawn_trash()) # add new trash to the list 
    #     trash_spawn_time = 0 # reset timer 



# NEW CODE Garbage Logic 
# Move trash down 
    # trash_rect.y += trash_speed # If thrash flew after bottom screen 
    # if trash_rect.y > screen_height: # return it back to random place 
    #     trash_rect.y = 0
    #     trash_rect.x = random.randint(0, screen_width - trash_width)
    # trash["rect"].y += trash_speed # turn to key "rect" in "trash" dictionary
    # if trash["rect"].y > screen_height:
    #     # turning function of creating new trash 
    #     trash = spawn_trash()
    # if trash["rect"].colliderect(player_rect):
    #     correct_index = trash["type"]["bin_index"] # getting right answer from the object 
    #     if current_color_index == correct_index: # compare answers with current container color 
    #         score += 10 # increase score
    #     else:
    #         lives -= 1 # inncorect - lose life 
    #     trash = spawn_trash()

    # elif trash["rect"].top > screen_height:
    #     lives -= 1
    #     trash = spawn_trash()

    # # Logic of missing garbage # Delete Logic of missing garbage and note it 

    # if trash["rect"].top > screen_height:
    #     lives -= 1
    #     trash = spawn_trash()
        # if the top border of the trash (trash["rect"].top) is lower than than screen_height
        # means that player missed it. Lose life and create a new trash.



    # color_to_draw = trash["type"]["color"] # taking color from type of trash 
    # rect_to_draw = trash["rect"] # taking rectangle from trash 
    # pygame.draw.rect(screen, color_to_draw, rect_to_draw)
    # pygame.draw.rect(screen, player_color, player_rect) # After cleaning we draw rectangel on new place with new color 
    # pygame.draw.rect(screen, trash_color, trash_rect)

    # Update Screen 
    # pygame.display.flip() # get everything that we've drawn on "screen" and how it to player 



