# Importamos librerias
import sys
import pygame

from .config import *
from .platform import Platform
from .player import Player

class Game: # inicializamos
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((WIDTH, HEIGHT)) # Creamos ventana
        pygame.display.set_caption(TITLE)

        self.running = True

    def start(self):
        self.new()

    def new(self): # Genera nuevos elementos 
        self.generate_elements()
        self.run()

    def generate_elements(self): # Generamos los diferentes elementos
        self.platform = Platform()
        self.player = Player(100, self.platform.rect.top - 220)

        self.sprites = pygame.sprite.Group() # Agrupamos

        self.sprites.add(self.platform)
        self.sprites.add(self.player)

    def run(self):
        while self.running:
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
        pygame.display.flip() # Actualiza la superficie

        self.sprites.update()

        self.player.validate_platform(self.platform)

    def stop(self):
        pass