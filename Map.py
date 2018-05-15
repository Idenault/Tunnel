from Config import *


class Map:

    def __init__(self, Path):
        self.data = []
        with open(Path, "rt") as file:
            for L in file:
                self.data.append(L)

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

