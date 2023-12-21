import pygame
from config import game_actions, env_actions
import logging

class Controller:
    def __init__(self) -> None:
        pass

    def input(self):
        out = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                out.append(env_actions[0])
                break
            if not event.type == pygame.KEYDOWN: 
                continue

            match event.key:
                case pygame.K_ESCAPE:
                    out.append(env_actions[0])
                case pygame.K_LEFT:
                    out.append(game_actions[0])
                case pygame.K_RIGHT:
                    out.append(game_actions[1])
                case pygame.K_UP:
                    out.append(game_actions[2])
                case pygame.K_LCTRL:
                    out.append(game_actions[2])
                case pygame.K_DOWN:
                    out.append(game_actions[4])
                case pygame.K_SPACE:
                    out.append(game_actions[5])
                case pygame.K_c:
                    out.append(game_actions[6])
        if out:
            logging.debug('Inputs:%s', ''.join(list(set(out))))
        return list(set(out))