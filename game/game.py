# Importamos librerias
import sys
import pygame
import random

from .config import *
from .platform import Platform
from .player import Player
from .wall import Wall

class Game: # inicializamos
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((WIDTH, HEIGHT)) # Creamos ventana
        pygame.display.set_caption(TITLE)

        self.running = True
        self.playing = True

        self.clock = pygame.time.Clock()

    def start(self):
        self.new()

    def new(self): # Genera nuevos elementos 
        self.generate_elements()
        self.run()

    def generate_elements(self): # Generamos los diferentes elementos
        self.platform = Platform()
        self.player = Player(100, self.platform.rect.top - 220)

        self.sprites = pygame.sprite.Group() # Agrupamos
        self.walls = pygame.sprite.Group() # Almacenamos obstaculos

        self.sprites.add(self.platform)
        self.sprites.add(self.player)

        self.generate_walls()

    def generate_walls(self):

        last_position = WIDTH + 100

        if not len(self.walls) > 0:

            for w in range(0, MAX_WALLS):

                left = random.randrange(last_position + 200, last_position + 400)
                wall = Wall(left, self.platform.rect.top)

                last_position = wall.rect.right

                self.sprites.add(wall)
                self.walls.add(wall)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

        key = pygame.key.get_pressed()

        if key[pygame.K_SPACE]:
            self.player.jump()

    def draw(self):
        self.surface.fill(GREY) # Asignamos color

        self.sprites.draw(self.surface)

    def update(self):
        if self.playing:
            pygame.display.flip() # Actualiza la superficie

            wall = self.player.collide_with(self.walls)
            if wall:
                if self.player.collide_bottom(wall):
                    self.player.skid(wall)
                else:
                    self.stop()

        pygame.time.delay(20)

        self.sprites.update()

        self.player.validate_platform(self.platform)

        self.update_elements(self.walls)
        self.generate_walls()

    def update_elements(self, elements):
        for element in elements:
            if not element.rect.right > 0:
                element.kill()

    def stop(self):
        self.player.stop()
        self.stop_elements(self.walls)

        self.playing = False

    def stop_elements(self, elements):
        for element in elements:
            element.stop()