from environment.config import *
from environment.controls import Controller
from environment.tetris import Tetris
from environment.renderer import PyGameRenderer

class TetrisApp():
    def __init__(self, cols, rows) -> None:
        self.env = Tetris(cols, rows)
        
        self.key_actions = {
            "quit":     self.quit,
            "left":     lambda: self.env.move(-1),
            "right":    lambda: self.env.move(1),
            "rotate_cw":self.env.rotate,
            "soft_drop":self.env.soft_drop,
            "hard_drop":self.env.hard_drop,
            "hold":     self.env.hold,
            "reset":    self.env.reset,
            "pause":    self.pause,
            "down":     self.env.down,
        }

        self.renderer = PyGameRenderer(Config.cell_size)
        self.renderer.render(self.env) 
    
        self.controller = Controller(self.key_actions)
        self.controller.setEventTimer(Config.delay_id, Config.down_delay)

    def quit(self):
        self.exit_program = True

    def pause(self):
        self.env.paused = not self.env.paused
        if self.env.paused:
            self.controller.removeEventTimer(Config.delay_id)
        else:
            self.controller.setEventTimer(Config.delay_id, Config.down_delay)

    def start(self):
        self.exit_program = False
        while not self.exit_program:
            self.renderer.render(self.env) 
            self.controller.handleEvents()
            self.renderer.wait(1)


if __name__ == '__main__':
    app = TetrisApp(Config.cols, Config.rows)
    app.start()
