import libtcodpy as libtcod

from random import randint



class Object:
    #this is a generic object: the player, a monster, an item, the stairs...
    #it's always represented by a character on screen.


    def __init__(self, x, y, char ,color = libtcod.white,hp=1):

        self.x = x
        self.y = y
        self.char = char
        self.hp = hp
        self.color = color
 
    def move(self, dx, dy):
        #move by the given amount
        
        self.x += dx
        self.y += dy
        

    def wall_collide(self,game_map):
        return(game_map[self.x + dx][self.y + dy].blocked)


    def list_collide(self,object_list):
        for other in object_list[:]:
            if (self.objects_collide(other)):
                if (other.hp<1):
                    #score points

                    #remove object
                    other.char = ' '
                    object_list.remove(other)

                return True

        return False



    def objects_collide(self,other):
        if(self.x == other.x and self.y == other.y):
            self.hp-=1
            other.hp-=1
            return True
        else:
            return False




class Player(Object):

    def __init__(self,x,y,char='^'):
        super().__init__(self,x,y,char,libtcod.white)

    def shoot(self,bullets):

        if self.char == '^':
            direction = (0,-1)

        elif self.char == 'v':
            direction = (0,1)

        elif self.char == '<':
            direction = (-1,0)

        elif self.char == '>':
            direction = (1,0)

        bullets.append(Bullet(self.x,self.y,'*',direction))      

    def nsz(self,x,y): #no spawn zone around player
        spacing = 2 #the amount of space around player where enemies can't spawn
        return( (x>self.x+spacing) and (x < self.x-spacing) and (y>self.y+spacing) and (y<self.y-spacing) ) #return true if no intersect
    



class Enemy(Object):
    def __init__(self,x,y,char,hp,direction =(0,0)):
        super().__init__(self,x,y,char,libtcod.white,hp)
        self.direction = direction
        self.points = hp
        self.update_color()


    def update_color(self):
        colors_dict = {3:libtcod.green,2:libtcod.yellow,1:libtcod.red}
        self.color = colors_dict[self.hp]

    def move(self,player_list,bullet_list):
        super().move(*self.direction)
        return(self.list_collide(player_list) or self.list_collide(bullet_list))




class Bullet(Object):
    def __init__(self,x,y,char,direction):
        super().__init__(self,x,y,char)
        self.direction = direction
        self.move()

    def move(self,enemy_list):
        super().move(*self.direction)
        return(self.list_collide(enemy_list))






def create_player(SCREEN_WIDTH,SCREEN_HEIGHT,players):
    #player locations
    # p1|p2|p3
    # p4|p5|p6
    # p7|p8|p9

    p1 = Player(int(SCREEN_WIDTH/4), int(SCREEN_HEIGHT/4), '^')
    p2 = Player(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/4), '^')
    p3 = Player(int(SCREEN_WIDTH*3/4), int(SCREEN_HEIGHT/4), '^')
    p4 = Player(int(SCREEN_WIDTH/4), int(SCREEN_HEIGHT/2), '^')
    p5 = Player(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2), '^')
    p6 = Player(int(SCREEN_WIDTH*3/4), int(SCREEN_HEIGHT/2), '^')
    p7 = Player(int(SCREEN_WIDTH/4), int(SCREEN_HEIGHT*3/4), '^')
    p8 = Player(int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT*3/4), '^')
    p9 = Player(int(SCREEN_WIDTH*3/4), int(SCREEN_HEIGHT*3/4), '^')

    players.append([p1,p2,p3,p4,p5,p6,p7,p8,p9])
    

def create_enemy(MAP_WIDTH,MAP_HEIGHT,objects):

    direction = (randint(-1,1),randint(-1,1))
    hp = randint(1,3)
    x = randint(2, MAP_WIDTH -2)
    y = randint(2, MAP_HEIGHT -2)

    for player in objects['players']:
        if not(player.nsz(x,y)):
            break
    else:
        objects['enemies'].append(Enemy(x,y,'@',hp,direction))



    



