import pygame as pg
import sys
from Sprites import *
from Map import *
from Config import *
import time

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.image = pg.image.load("Assets/2d-game-background-1.png")
        self.rect = self.image.get_rect()
        self.clock = pg.time.Clock()
        self.allSprites = pg.sprite.Group()
        self.Floors = pg.sprite.Group()
        self.MountainSprites = pg.sprite.Group()
        self.Obstacle = pg.sprite.Group()
        pg.key.set_repeat(500, 10)
        self.dead = 10
        self.map = Map("Assets/Map")

    def new(self):
        #create Sprite Groups
        self.allSprites = pg.sprite.Group()
        self.Floors = pg.sprite.Group()
        self.MountainSprites = pg.sprite.Group()
        self.Obstacle = pg.sprite.Group()
        self.dead = 10
        # Create Sprites
        self.player = Player(self, 4*32, 21*32)
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Floor(self, col, row, 1)
                elif tile == '2':
                    Dirt(self, col, row, 4)
                elif tile == '3':
                    Stone(self, col, row, 3)
                elif tile == '4':
                    Floor(self, col, row, 2)
                elif tile == '5':
                    Obstacle(self, col, row, 5)

        self.run()

    def quit(self):
        pg.quit()
        sys.exit()

    def run(self):
        self.notClosed = True
        while self.notClosed:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.allSprites.update()
        dead = pg.sprite.spritecollide(self.player, self.Obstacle, False)
        if self.dead < 10:
            self.dead -= 1
            if self.dead == 0:
                self.new()
                self.run()
        elif dead:
            self.dead -= 1
        colidefoorY = pg.sprite.spritecollide(self.player, self.Floors, False)
        colideMountainX = pg.sprite.spritecollide(self.player, self.MountainSprites, False)
        if self.player.vel.y > 0:
            if colidefoorY:
                self.player.pos.y = colidefoorY[0].rect.top
                self.player.vel.y = 0
            if colideMountainX:
                self.player.pos.y = colideMountainX[0].rect.top
                self.player.vel.y = 0
        elif colideMountainX:
            self.player.pos.x = self.player.pos.x
            self.player.vel.x = 0

    def draw(self):
        self.screen.fill(WHITE)
        self.screen.blit(self.image, self.image.get_rect())
        self.allSprites.draw(self.screen)
        self.drawText(self.player.items, "Stone: ", 20, 20, 0)
        self.drawText(self.player.items, "Diamond: ", 20, 45, 1)
        self.drawText(self.player.items, "Iron: ", 20, 70, 2)
        self.drawText(self.player.items, "Silver: ", 20, 95, 3)
        self.drawText(self.player.items, "Gold: ", 20, 120, 4)
        self.drawText(self.player.craftedItems, "Fireballs: ", 20, 145, 0)
        self.drawText(self.player.craftedItems, "Jetpacks: ", 20, 170, 1)
        pg.display.flip()

    def drawText(self, loc, Text, x, y, i):
        font = pg.font.Font(FONT, 24)
        UI = font.render(Text + str(loc[i]), True, BLACK)
        UIRect = UI.get_rect()
        UIRect.topleft = (x, y)
        self.screen.blit(UI, UIRect)

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_1:
                    self.player.craft(1)
                if event.key == pg.K_2:
                    self.player.craft(2)
                if event.key == pg.K_0:
                    self.player.craft(0)
                if event.key == pg.K_f:
                    self.player.shoot()
                if event.key == pg.K_j:
                    self.player.jetpack()
            if event.type == pg.MOUSEBUTTONDOWN:
                tx = pg.mouse.get_pos()[0] // 32
                ty = pg.mouse.get_pos()[1] // 32
                print(tx)
                i = self.player.harvest(tx, ty)


g = Game()
while True:
    g.new()