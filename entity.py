import libtcodpy as libtcod

from random import randint



class Thing:
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
        dx, dy = self.direction
        return(game_map.tiles[self.x + dx][self.y + dy].blocked)


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




class Player(Thing):

    def __init__(self,x,y,char='^'):
        super().__init__(x,y,char)

    def shoot(self,bullets,enemies):

        if self.char == '^':
            direction = (0,-1)

        elif self.char == 'v':
            direction = (0,1)

        elif self.char == '<':
            direction = (-1,0)

        elif self.char == '>':
            direction = (1,0)

        bullets.append(Bullet(self.x,self.y,'*',direction,enemies))      

    def nsz(self,x,y): #no spawn zone around player
        spacing = 2 #the amount of space around player where enemies can't spawn
        return( (x>self.x+spacing) and (x < self.x-spacing) and (y>self.y+spacing) and (y<self.y-spacing) ) #return true if no intersect
    



class Enemy(Thing):
    def __init__(self,x,y,char,hp,direction =(0,0)):
        super().__init__(x,y,char,libtcod.white,hp)
        self.direction = direction
        self.points = hp
        self.update_color()


    def update_color(self):
        colors_dict = {3:libtcod.green,2:libtcod.yellow,1:libtcod.red}
        if self.hp >0:
            self.color = colors_dict[self.hp]

    def move(self,player_list,bullet_list):
        super().move(*self.direction)
        return(self.list_collide(player_list) or self.list_collide(bullet_list))




class Bullet(Thing):
    def __init__(self,x,y,char,direction,enemies):
        super().__init__(x,y,char)
        self.direction = direction
        self.move(enemies)
       

    def move(self,enemy_list):
        super().move(*self.direction)
        return(self.list_collide(enemy_list))






def create_player(MAP_WIDTH,MAP_HEIGHT,players):
    #player locations
    # p1|p2|p3
    # p4|p5|p6
    # p7|p8|p9

    p1 = Player(int(MAP_WIDTH/6), int(MAP_HEIGHT/6), '^')
    p2 = Player(int(MAP_WIDTH/2), int(MAP_HEIGHT/6), '^')
    p3 = Player(int(MAP_WIDTH*5/6), int(MAP_HEIGHT/6), '^')
    p4 = Player(int(MAP_WIDTH/6), int(MAP_HEIGHT/2), '^')
    p5 = Player(int(MAP_WIDTH/2), int(MAP_HEIGHT/2), '^')
    p6 = Player(int(MAP_WIDTH*5/6), int(MAP_HEIGHT/2), '^')
    p7 = Player(int(MAP_WIDTH/6), int(MAP_HEIGHT*5/6), '^')
    p8 = Player(int(MAP_WIDTH/2), int(MAP_HEIGHT*5/6), '^')
    p9 = Player(int(MAP_WIDTH*5/6), int(MAP_HEIGHT*5/6), '^')

    players.append(p1)
    players.append(p2)
    players.append(p3)
    players.append(p4)
    players.append(p5)
    players.append(p6)
    players.append(p7)
    players.append(p8)
    players.append(p9)
    

def create_enemy(MAP_WIDTH,MAP_HEIGHT,objects):
    # import pdb; pdb.set_trace()

    direction = (randint(-1,1),randint(-1,1))
    hp = randint(1,3)
    x = randint(2, MAP_WIDTH -2)
    y = randint(2, MAP_HEIGHT -2)

    # for player in objects['players']:
    #     if not(player.nsz(x,y)):
    #         break
    # else:
    objects['enemies'].append(Enemy(x,y,'@',hp,direction))



    



