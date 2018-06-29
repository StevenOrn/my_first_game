import libtcodpy as libtcod

from entity import Player,Enemy,create_player,create_enemy
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all
from random import randint


def main():


 
    #actual size of the window
    SCREEN_WIDTH = 80
    SCREEN_HEIGHT = 50
    
    #size of the map
    MAP_WIDTH = 80
    MAP_HEIGHT = 45
    
    LIMIT_FPS = 10  #Game speed
    SPAWN_RATE = 10 #percent chance of spawn

    #intialize score
    score = 0
    
    #Wall colors
    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150)
    }


    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'test tutorial', False)
    libtcod.sys_set_fps(LIMIT_FPS)
    con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

    
    #the Dict of List of Objects
    objects = {'players':[],'enemies':[],'bullets':[]}
    create_player(SCREEN_WIDTH, SCREEN_HEIGHT,objects['players'])


    
    #generate map (at this point it's not drawn to the screen)
    game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)




    while not libtcod.console_is_window_closed():
        
        

        #spawn rate
        if (randint(1,100) <= SPAWN_RATE):
            create_enemy(MAP_WIDTH,MAP_HEIGHT,objects)

        render_all(con, objects, game_map, SCREEN_WIDTH, SCREEN_HEIGHT, colors)

        libtcod.console_flush()


       
        if (len(objects['players']) != 0):
            clear_all(con, objects['players'])
        if (len(objects['enemies']) != 0):
            clear_all(con, objects['enemies'])
        if (len(objects['bullets']) !=0):
            clear_all(con, objects['bullets'])
    
        #handle keys and exit game if needed
        exit = handle_keys(objects)

        if(len(objects['players'])<1):
            #game_over()
            exit =True

        if exit:
            break


#def game_over()


if __name__ == '__main__':
     main()