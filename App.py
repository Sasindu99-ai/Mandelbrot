import pygame as pg

from Global import res
from Mandelbrot import Mandelbrot

__all__ = ['App']


class App:
    """
    App class to run the mandelbrot set

    Attributes:
    -----------
    screen: Surface
        The screen surface
    clock: Clock
        The clock instance
    mandelbrot: Mandelbrot

    Methods:
    --------
    run():
        Runs the app
    """

    def __init__(self):
        """
        Initialize the app
        """
        self.screen = pg.display.set_mode(res, pg.SCALED)
        self.clock = pg.time.Clock()
        self.mandelbrot = Mandelbrot(self)

    def run(self) -> None:
        """
        Runs the app
        :return: None
        """
        while True:
            for i in pg.event.get():
                if i.type == pg.QUIT:
                    quit(1)

            self.screen.fill('black')
            self.mandelbrot.run()
            pg.display.flip()
            self.clock.tick()
            pg.display.set_caption(f'Mandelbrot - FPS: {self.clock.get_fps(): .2f}')
