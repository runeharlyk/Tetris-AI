import pygame
from config import key_actions

class Controller:
    def __init__(self, actions) -> None:
        self.actions = actions

    def handleEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT+1:
                self.actions['down']()
            if event.type == pygame.QUIT:
                self.actions['quit']()
            if not event.type == pygame.KEYDOWN: 
                continue
            actions = [action for action, events in key_actions.items() if event.key in events]
            for action in actions:
                self.actions[action]()

    def addEvent(self, delay):
        pygame.time.set_timer(pygame.USEREVENT+1, delay)