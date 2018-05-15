import pygame as pyG
from Config import *
import random
vec = pyG.math.Vector2


class Player(pyG.sprite.Sprite):
    def __init__(self, game,startX, startY):
        self.groups = game.allSprites
        pyG.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pyG.Surface((TILESIZE, TILESIZE*2))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.pos = vec(startX, startY)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.items = [0, 0, 0, 0, 0]
        self.craftedItems = [0, 0, 0]

    def update(self):

        self.acc = vec(0, 0.8)
        keys = pyG.key.get_pressed()
        if keys[pyG.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pyG.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.8 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
        self.rect.midbottom = self.pos

    def jump(self):
        colidefoorY = pyG.sprite.spritecollideany(self, self.game.Floors)
        colideMountainX = pyG.sprite.spritecollideany(self, self.game.MountainSprites)
        if colidefoorY:
            self.vel.y = - 15
        if colideMountainX:
            self.vel.y = - 15

    def harvest(self, CX, CY):
        i = 0
        if i == 0:
            for tile in self.game.MountainSprites:
                print(tile.x)
                if tile.x == CX and tile.y == CY:
                    if self.pos.x//32 < CX and self.pos.x // 32 + 2>= CX:
                        tile.HP -= 1
                        if tile.HP <=0:
                            self.score(tile)
                            self.game.MountainSprites.remove(tile)
                            self.game.allSprites.remove(tile)
                    elif self.pos.x//32 > CX and self.pos.x//32 -2<= CX:
                        tile.HP -= 1
                        if tile.HP <= 0:
                            self.score(tile)
                            self.game.MountainSprites.remove(tile)
                            self.game.allSprites.remove(tile)

    def score(self, tile):
        rand = random.randint(0, 100)
        if tile.ID == 0 and rand > 75:
            self.items[1] += 1
        elif tile.ID == 0 and rand < 75:
            self.items[0] += 2
        elif tile.ID == 1 and rand > 80:
            self.items[4] += 1
        elif tile.ID == 1 and rand < 41:
            self.items[2] += 1
        elif tile.ID == 1:
            self.items[3] += 2

    def craft(self, i):
        if i == 1:
            if self.items[1] >= 2 and self.items[2] >= 2 and self.items[3] >= 1:
                self.craftedItems[0] += 1
                self.items[1] -= 2
                self.items[2] -= 2
                self.items[3] -= 1
        elif i == 2:
            if self.items[2] >= 2 and self.items[3] >= 1 and self.items[4] >= 1:
                self.craftedItems[1] += 1
                self.items[2] -= 2
                self.items[3] -= 1
                self.items[4] -= 1
        elif i == 0:
            self.craftedItems[0] += 1
            self.craftedItems[1] += 1

    def shoot(self):
        print(self.pos.x + 10)
        if self.craftedItems[0] >= 1:
            Projectile(self.game, self.pos.x + 10, self.pos.y)
            self.craftedItems[0] -= 1

    def jetpack(self):
        if self.craftedItems[1] >= 1:
            colidefoorY = pyG.sprite.spritecollideany(self, self.game.Floors)
            colideMountainX = pyG.sprite.spritecollideany(self, self.game.MountainSprites)
            if colidefoorY:
                self.vel.y = - 30
                self.craftedItems[1] -= 1
            if colideMountainX:
                self.vel.y = - 30
                self.craftedItems[1] -= 1

class Floor (pyG.sprite.Sprite):
    def __init__(self, game, x, y, i):
        self.groups = game.allSprites, game.Floors
        pyG.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pyG.Surface((TILESIZE, TILESIZE))
        self.image = pyG.image.load(TILEPATH[i])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Stone (pyG.sprite.Sprite):
    def __init__(self, game, x, y, i):
        self.groups = game.allSprites, game.MountainSprites
        pyG.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pyG.Surface((TILESIZE, TILESIZE))
        self.image = pyG.image.load(TILEPATH[i])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.HP = 2
        self.amount = 1
        self.type = [STONE, DIAMOND]
        self.ID = 0

class Dirt (pyG.sprite.Sprite):
    def __init__(self, game, x, y, i):
        self.groups = game.allSprites, game.MountainSprites
        pyG.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pyG.Surface((TILESIZE, TILESIZE))
        self.image = pyG.image.load(TILEPATH[i])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.HP = 2
        self.amount = 2
        self.type = [IRON, SILVER, GOLD]
        self.ID = 1

class Projectile (pyG.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.allSprites,
        pyG.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pyG.Surface((TILESIZE/2, TILESIZE/2))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x + 5
        self.y = y - 36
        self.rect.x = x + 36
        self.rect.y = y - 36
        self.Damage = 5
        self.distance = 0

    def update(self):
        colideMountainX = pyG.sprite.spritecollideany(self, self.game.MountainSprites)
        if colideMountainX:
            self.game.allSprites.remove(self)
        else:
            self.rect.x += 10
            self.distance += 10
            if self.distance > 1000:
                self.game.allSprites.remove(self)

class Obstacle (pyG.sprite.Sprite):
    def __init__(self, game, x, y, i):
        self.groups = game.allSprites, game.Obstacle
        pyG.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pyG.Surface((TILESIZE, TILESIZE))
        self.image = pyG.image.load(TILEPATH[i])
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
