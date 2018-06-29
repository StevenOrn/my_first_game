from map_objects.tile import Tile


class GameMap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()



    def initialize_tiles(self):
        tiles = [[ Tile(False)
            for y in range(self.height) ]
                for x in range(self.width) ]


        for y in range(self.height):
            tiles[self.width-1][y].blocked = True
            tiles[int(self.width/3)][y].blocked = True
            tiles[int(self.width*2/3)][y].blocked = True
            tiles[0][y].blocked = True

        for x in range(self.width):
            tiles[x][self.height-1].blocked = True
            tiles[x][int(self.height/3)].blocked = True
            tiles[x][int(self.height*2/3)].blocked = True
            tiles[x][0].blocked = True

        return tiles

