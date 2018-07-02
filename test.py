import libtcodpy as libtcod
from random import randint
import math
 
#actual size of the window
SCREEN_WIDTH = 90
SCREEN_HEIGHT = 100
 
#size of the map
MAP_WIDTH = 90
MAP_HEIGHT = 90
 
LIMIT_FPS = 10  #Game speed

#intialize score
score = 0
 
 
color_dark_wall = libtcod.Color(0, 0, 100)
color_dark_ground = libtcod.Color(50, 50, 150)
 
 
class Tile:
    #a tile of the map and its properties
    def __init__(self, blocked, block_sight = None):
        self.blocked = blocked
 
        #by default, if a tile is blocked, it also blocks sight
        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight
 
class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.


    def __init__(self, x, y, char ,direction =(0,0),hp=1,hostile=False):

        self.x = x
        self.y = y
        self.char = char
        self.direction = direction
        self.hp = hp
        self.points = hp
        self.hostile = hostile
        self.player = False

        self.update_color()

    def isplayer(self):
        self.player = True


    def update_color(self):
        colors_dict = {3:libtcod.green,2:libtcod.yellow,1:libtcod.red}
        self.color = colors_dict[self.hp]
 
    def move(self, dx, dy):
        #move by the given amount, if the destination is not blocked
        if map[self.x + dx][self.y + dy].blocked:
            return True
        else:
            self.x += dx
            self.y += dy
            return False

    def objects_collide(self,other):
        if (self.hostile and other.hostile):
            return False
        
        elif (self.x == other.x and self.y == other.y):
            return True
        else:
            return False


    def check_hp(self):
  
        if (self.hp <= 0):
            global score
            #self.clear()
            self.char = ' '
            objects.remove(self)
            if self.player:
                gameover()
            elif self.hostile:
                score+= self.points
        else:
            self.update_color()
 
    def draw(self):
        #set the color and then draw the character that represents this object at its position
        libtcod.console_set_default_foreground(con, self.color)
        libtcod.console_put_char(con, int(self.x), int(self.y), self.char, libtcod.BKGND_NONE)
 
    def clear(self):
        #erase the character that represents this object
        libtcod.console_put_char(con, int(self.x), int(self.y), ' ', libtcod.BKGND_NONE)
 
 
 
def make_map(endgame = False):
    global map
 
    #fill map with "unblocked" tiles
    map = [[ Tile(endgame)
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]
 
    #place two pillars to test the map
    for y in range(MAP_HEIGHT):
        map[MAP_WIDTH-1][y].blocked = True
       # map[int(MAP_WIDTH/3)][y].blocked = True
       # map[int(MAP_WIDTH*2/3)][y].blocked = True
        map[0][y].blocked = True

    for x in range(MAP_WIDTH):
        map[x][MAP_HEIGHT-1].blocked = True
       # map[x][int(MAP_HEIGHT/3)].blocked = True
       # map[x][int(MAP_HEIGHT*2/3)].blocked = True
        map[x][0].blocked = True

 
 
def render_all():
    global color_light_wall
    global color_light_ground
 
    #go through all tiles, and set their background color

    render_score()

    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            if map[x][y].blocked:
                libtcod.console_set_char_background(con, x, y, color_dark_wall, libtcod.BKGND_SET )
            else:
                libtcod.console_set_char_background(con, x, y, color_dark_ground, libtcod.BKGND_SET )
 
    #draw all objects in the list
    for object in objects:
        
        if(object.move(*object.direction)):
            objects.remove(object)
        else:
            check_collide(object)

            object.draw()
 
    #blit the contents of "con" to the root console
    libtcod.console_blit(con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)
 
def handle_keys():
    key = libtcod.console_check_for_keypress()  #real-time
    #key = libtcod.console_wait_for_keypress(True)  #turn-based
 
    if key.vk == libtcod.KEY_ENTER and key.lalt:
        #Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
 
    elif key.vk == libtcod.KEY_ESCAPE:
        return True  #exit game
    
    if libtcod.console_is_key_pressed(libtcod.KEY_SPACE):
        shoot()
 
    #movement keys
    if libtcod.console_is_key_pressed(libtcod.KEY_UP):
        player.move(0, -1)
        player.char = '^'
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_DOWN):
        player.move(0, 1)
        player.char = 'v'
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_LEFT):
        player.move(-1, 0)
        player.char = '<'
 
    elif libtcod.console_is_key_pressed(libtcod.KEY_RIGHT):
        player.move(1, 0)
        player.char = '>'


def shoot():

    if player.char == '^':
        direction = (0,-1)

    elif player.char == 'v':
        direction = (0,1)

    elif player.char == '<':
        direction = (-1,0)

    elif player.char == '>':
        direction = (1,0)

    bullet = Object(player.x,player.y,'*',direction)
    
    bullet.move(*direction)
    bullet.move(*direction)

    objects.append(bullet)

def create_enemy():

    direction = (randint(-1,1),randint(-1,1))
    hp = randint(1,3)

    enemy = Object(randint(10, MAP_WIDTH -10), randint(10, MAP_HEIGHT -10), '@', direction,hp,True)
    objects.append(enemy)


def check_collide(object):
    for other_object in objects:

        if(object.objects_collide(other_object) and object!=other_object):
            object.hp-=1
            other_object.hp-=1
            object.check_hp()
            other_object.check_hp()


def gameover():
    make_map(True)

def render_score():
    global score

    libtcod.console_print(con, int(MAP_WIDTH/2), int(SCREEN_HEIGHT-(SCREEN_HEIGHT - MAP_HEIGHT)/2), str(score))





 
 
#############################################
# Initialization & Main Loop
#############################################
 
libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'test tutorial', False)
libtcod.sys_set_fps(LIMIT_FPS)
con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)

#intialize score
# score = 1

 
#create object representing the player
player = Object(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), '^')
player.isplayer()
 
#the list of objects with those two
objects = [player]
 
#generate map (at this point it's not drawn to the screen)
make_map()



 
 
while not libtcod.console_is_window_closed():
    
    #spawn rate
    if randint(1,100) <= 10:
        create_enemy()

    #render the screen
    render_all()
 
    libtcod.console_flush()
 
    #erase all objects at their old locations, before they move
    for object in objects:
        object.clear()
 
    #handle keys and exit game if needed
    exit = handle_keys()
    if exit:
        break