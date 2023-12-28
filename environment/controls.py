import pygame
from environment.actions import key_actions

class Controller:
    def __init__(self, actions) -> None:
        self.actions = actions

    def isValidAction(self, action, events, event):
        return action in self.actions and (event.type in events or event.type == pygame.KEYDOWN and event.key in events)

    def getActions(self):
        for event in pygame.event.get():
            for action, events in key_actions.items():
                if self.isValidAction(action, events, event):
                    yield self.actions[action]

    def handleEvents(self):
        for action in self.getActions():
            action()

    def addEvent(self, event_id:int, ms:int):
        pygame.time.set_timer(pygame.USEREVENT+event_id, ms)